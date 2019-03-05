from multiprocessing.managers import BaseManager
import datetime, time

class MyBaseManager(BaseManager):
    pass

MyBaseManager.register('get_reserved')

class Cleaner:

    def __init__(self):
        self.manager = MyBaseManager(address=('0.0.0.0', 5000), authkey=b'abc')
        self.manager.connect()

        self.reserved_dict = self.manager.get_reserved()

    def start(self):
        while True:
            for key, value in self.reserved_dict.items():
                print(key, value)
                expire_time = value.get('expire_time')
                if not expire_time or expire_time < datetime.datetime.now().timestamp():
                    self.reserved_dict.pop(key)
                    break
            else:
                time.sleep(10)



if __name__ == "__main__":
    Cleaner().start()