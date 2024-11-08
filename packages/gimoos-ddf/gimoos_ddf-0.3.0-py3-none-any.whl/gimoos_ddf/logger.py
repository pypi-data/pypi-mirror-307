#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger('gimoos_ddf')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)7s : %(message)s'))

logger.addHandler(handler)
