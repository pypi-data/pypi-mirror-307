#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import json
import asyncio
from pathlib import Path
from datetime import datetime

from aiohttp import ClientSession, FormData, ClientConnectorError, ClientError
from tqdm import tqdm

from .logger import logger


class DriverUpdater():
    def __init__(self, path: str, host: str, username: str, password: str):
        self.host     = host
        self.url      = f'http://{host}/interface/db/selector'
        self.username = username
        self.password = password

        self.token              = None
        self.encoding           = 'utf-8'
        self.work_path          = Path(path)
        self.temp_path          = self.work_path / '.temp'
        self.update_record_file = self.temp_path / '.record'
        self.update_record      = {host: {}}
        self.tq                 = None
        self.suc_list           = []
        self.fail_list          = []
        self.fail_msg_list      = []

    def __repr__(self):
        return f"DriverUpdater({self.host})"

    def read_update_record(self):
        if not self.temp_path.exists():
            self.temp_path.mkdir()

        if not self.update_record_file.exists():
            return None

        with open(self.update_record_file, 'r', encoding=self.encoding) as f:
            try:
                self.update_record = json.load(f)
            except:
                self.update_record = {}

    def write_update_record(self):
        with open(self.update_record_file, 'w', encoding=self.encoding) as f:
            json.dump(self.update_record, f, ensure_ascii=False, indent=4)

    def is_need_update(self, path: Path) -> bool:
        driver_py_file  = path / 'driver.py'
        driver_xml_file = path / 'driver.xml'
        driver_py_mtime  = driver_py_file.stat().st_mtime
        driver_xml_mtime = driver_xml_file.stat().st_mtime

        mtime = self.update_record.get(self.host, {}).get(path.name, {})
        if mtime.get('driver.py', None) == driver_py_mtime and mtime.get('driver.xml', None) == driver_xml_mtime:
            return False
        else:
            self.update_record.setdefault(self.host, {})[path.name] = {
                'driver.py': driver_py_mtime,
                'driver.xml': driver_xml_mtime,
            }
            return True

    def get_update_list(self):
        work_path = Path(self.work_path)

        list = []
        for item in work_path.iterdir():
                # 包含 driver.py 和 driver.xml
            if (item.is_dir()
                and (item / 'driver.py').exists()
                and (item / 'driver.xml').exists()
                and self.is_need_update(item)
            ):
                list.append(item)

        return list

    async def login(self):
        async with ClientSession() as session:
            async with session.post(self.url, json={
                "project": "items",
                "type": "im-function",
                "id": "login",
                "param": {
                    "data": {
                        "username": self.username,
                        "password": self.password,
                    },
                },
            }) as response:
                if response.status == 200:
                    self.token = (await response.json()).get('data', {}).get('token', None)
                else:
                    logger.error(f'登录失败，状态码：{response.status}')

    async def upload_file(self, path: Path):
        zip_file = self.temp_path / f'{path.name}.zip'

        # 构建 zip 文件
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(str(path / 'driver.py'), 'driver.py')
            zf.write(str(path / 'driver.xml'), 'driver.xml')

        # 上传 zip 文件
        with open(zip_file, 'rb') as f:
            data = FormData(quote_fields=False, charset=self.encoding)
            data.add_field('param', '{"project":"items","type":"im-function","id":"upload_driver","param":{}}', content_type='application/json')
            data.add_field('file', f, filename=f'{path.name}.zip', content_type='application/zip')

            headers = {'Authorization': f'Basic {self.token}',}

            async with ClientSession() as session:
                async with session.post(self.url, data=data, headers=headers) as response:
                    if response.status == 200:
                        self.suc_list.append(path.name)
                    else:
                        self.fail_list.append(path.name)
                        self.fail_msg_list.append((path.name, (await response.json()).get('message', '')))
                self.tq and self.tq.update(1)

    async def update_async(self):
        self.read_update_record()

        list = self.get_update_list()
        if not list:
            logger.info('没有需要更新的驱动程序')
            return

        await self.login()
        if not self.token:
            return

        tasks = [asyncio.ensure_future(self.upload_file(item)) for item in list]

        self.tq = tqdm(total=len(tasks), desc=f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]}] 上传进度')

        await asyncio.gather(*tasks)

        self.tq.close()

        logger.info(f'更新完成, 成功：{len(self.suc_list)}, 失败：{len(self.fail_list)}')
        for name, message in self.fail_msg_list:
            self.update_record.setdefault(self.host, {}).pop(name, None)
            logger.warning(f'上传 "{name}" 失败, 原因: "{message}"')

        self.write_update_record()

    def update(self):
        try:
            asyncio.get_event_loop().run_until_complete(self.update_async())
        except ClientConnectorError:
            logger.error(f'连接 {self.host} 失败')
        except ClientError as e:
            logger.error(f'请求失败，错误信息：{e}')
