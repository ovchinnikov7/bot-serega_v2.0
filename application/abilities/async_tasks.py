import random
import threading
import time
from datetime import datetime


class JobsConfiguration:
    __is_running = True

    def getStatus(self):
        return self.__is_running

    def setStatus(self, is_running):
        self.__is_running = is_running

class Jobs:

    __reminder_job = None
    __jobs_config = None

    def __init__(self):
        self.__jobs_config = JobsConfiguration()
        self.__reminder_job = threading.Thread(target=job, args=(self.__jobs_config,), daemon=True)

    def run_job(self):
        self.__is_running = True
        self.__reminder_job.start()
    def stop_job(self):
        self.__is_running = False


def job(jobs_states):
    try:
        while jobs_states.getStatus():
            print("Job rabotaet !")

            time.sleep(1)
            # time.sleep(check_time())
    except InterruptedError as e:
        print("Warning! Job interrupted")
    except Exception as e:
        print(f'ERROR! Job failed with exception {e}')



def check_time():
    time_interval = 3600 * random.randint(2, 8)

    evening = datetime(hour=22)
    morning = datetime(hour=10)

    time = datetime.now().time()
    if(time.hour + time_interval) >= evening.hour \
        and (time.hour + time_interval) <= morning.hour:
        next_time = morning(min=random.randint(10, 59))
        time_interval = next_time
    return time_interval