#!/usr/bin/env python
# -*- coding: utf-8 -*-#

# Copyright (c) 2021 Pim Witlox
#
# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.
 
import asyncio
import logging
import json
import os

from os.path import join, exists

import aiofiles


class Storage(object):
    """
    Our storage abstraction
    """

    logger = logging.getLogger(__name__)

    def __init__(self, path_prefix=None):
        """
        our storage class
        :param path_prefix: directory where to save our storage
        """
        self.path_prefix = path_prefix

    async def save(self):
        """
        save our cache to disk
        """
        self.logger.debug("auto-save")

    def prune(self):
        """
        clean up our memory when it exceeds a given amount of values
        """
        pass
