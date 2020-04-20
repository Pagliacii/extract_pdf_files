#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

"""
Created Date:       2020-04-17 15:38:32
Author:             Pagliacii
Last Modified By:   Pagliacii
Last Modified Date: 2020-04-17 23:35:48
Copyright © 2020-Pagliacii-MIT License
"""

import queue
import sys
from threading import Event, Thread


class Worker(Thread):
    def __init__(self, worker_id, stop_event, channel, timeout, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__id = worker_id
        self.__stop = stop_event
        self.__channel = channel
        self.__timeout = timeout
        self.__can_stop = True
        self.running = Event()
        self.work = None

    def can_stop(self):
        return self.__can_stop

    def run(self):
        while not self.__stop.is_set():
            try:
                item = self.__channel.get_nowait()
            except queue.Empty:
                self.__stop.wait(self.__timeout)
                continue

            work = item["work"]
            args = item["args"]
            kwargs = item["kwargs"]
            self.__can_stop = False
            try:
                work(*args, **kwargs)
            except Exception as e:
                print(
                    f"[Worker {self.__id}, {work}, {args}, {kwargs}]: Failed, caused by {e}",
                    file=sys.stderr
                )
            self.__can_stop = True


class Pool:
    def __init__(self, worker_num=10, timeout=2):
        self.__stop = Event()
        self.__queue = queue.Queue()
        self.__timeout = timeout
        self.__delay = Event()
        self.__workers = [
            Worker(i, self.__stop, self.__queue, self.__timeout) for i in range(worker_num)
        ]

    def submit(self, work, *args, **kwargs):
        assert callable(work)
        self.__queue.put({"args": args, "kwargs": kwargs, "work": work})

    def run(self):
        for worker in self.__workers:
            worker.start()

    def join(self):
        while not self.__done():
            self.__delay.wait(1)
        self.__stop.set()

    def __done(self):
        can_stop = all([worker.can_stop() for worker in self.__workers])
        return self.__queue.empty() and can_stop
