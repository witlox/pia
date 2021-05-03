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

import argparse
import asyncio
import logging
import time
import os
import math

from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

from pyaml_env import parse_config

from polo.utils import hash_file
from polo.storage import Storage


log_format = "%(asctime)s [%(levelname)-8.8s] %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger('polo')


def main():
    """
    entry point
    """
    parser = argparse.ArgumentParser(description="Polo Information Collector")

    half_cores = math.ceil(os.cpu_count() / 2)

    parser.add_argument('-t', '--thread-count', default=half_cores, help="number of threads to assign to polo")
    parser.add_argument('-c', '--config-file', default=None, help="path to locate the config file")
    parser.add_argument('-l', '--log-file', default=None, help="path to store logfile")
    parser.add_argument('-p', '--storage-path', default=None, help="directory where to store data")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="verbose logging")

    args = parser.parse_args()

    root_logger = logging.getLogger()
    if args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        root_logger.addHandler(file_handler)            
    if args.verbose:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    storage = Storage(args.storage_path)

    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    with ThreadPoolExecutor(args.thread_count) as pool:
        running = True
        config = None
            
        # refresh our configuration every 60 seconds
        def refresh_config(file_name):
            config_hash = None
            while running:
                if not file_name:
                    if os.path.exists('polo.conf'):
                        file_name = 'polo.conf'
                    elif os.path.exists(os.path.join(os.path.expanduser, 'polo.conf')):
                        file_name = os.path.join(os.path.expanduser, 'polo.conf')
                    elif os.path.exists(os.path.join('etc', 'polo', 'polo.conf')):
                        file_name = os.path.join('etc', 'polo', 'polo.conf')
                    elif 'POLO_CONF' in os.environ:
                        file_name = os.environ['POLO_CONF']
                    else:
                        logger.error('no valid configuration file found')
                if not os.path.exists(file_name):
                    logger.error('could not locate configuration at {0}'.format(file_name))
                else:
                    current_hash = hash_file(file_name)
                    if config_hash != current_hash:
                        logger.debug("config file changed, reloading")
                        config_hash = current_hash
                        config = parse_config(file_name)
                time.sleep(60)
        async def scheduled_configuration_refresh():
            await loop.run_in_executor(pool, refresh_config, args.config_file)
        loop.create_task(scheduled_configuration_refresh())

        # spawn tasks in queue for regularly check sources and enhancing graph (make sure the tasks respawn themselves at the back of the queue)
        result = await loop.run_in_executor(pool, listener(queue))
        
        try:
            loop.run_forever()
        except:
            logger.info("interrupt received")

        running = False

    if args.storage_path:
        loop.create_task(storage.save())

    logger.debug("waiting for background tasks to finish")
    pending_tasks = [task for task in asyncio.Task.all_tasks() if not task.done()]
    loop.run_until_complete(asyncio.gather(*pending_tasks))

    logger.info("elvis has left the building")


if __name__ == "__main__":
    main()
