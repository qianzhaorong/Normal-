TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLE = True
GETTER_ENABLE = True
API_ENABLED = True

import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.db import RedisClient

class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        tester = Tester()
        while True:
            print("test machine is running")
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        getter = Getter()
        while True:
            print("start to get proxy")
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        app.run()

    def run(self):
        print("The Proxy Pool is running")
        if TESTER_ENABLE:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLE:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
