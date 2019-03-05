from multiprocessing.managers import BaseManager
from multiprocessing import Manager
from queue import Queue


class MyQueue(BaseManager):
    pass

class UniqueQueue(Queue):
    def __init__(self, maxsize=None):
        super().__init__(maxsize)
        self.queue = []
        
    def _put(self, item):
        if self.maxsize:
            while len(self.queue) >= self.maxsize:
                pass

        if item not in self.queue:
            self.queue.append(item)
        
    def _get(self):

        while not len(self.queue):
            pass

        return self.queue.pop()

class NormalQueue(Queue):
    def __init__(self):
        super().__init__()
        self.queue = []

    def _put(self, item):
        if self.maxsize:
            while len(self.queue) >= self.maxsize:
                pass

        if item not in self.queue:
            self.queue.append(item)
        
    def _get(self):

        while not len(self.queue):
            pass

        return self.queue.pop()
    
    def contains(self, ticket_id):
        for ticket in self.queue:
            if ticket.id == item:
                return True
        else:
            return False

biletler = UniqueQueue(20)
satilanlar = NormalQueue()
reserved = Manager().dict()


def get_biletler():
    return biletler

def get_satilanlar():
    return satilanlar

def get_reserved():
    return reserved

MyQueue.register('get_biletler', callable=get_biletler)
MyQueue.register('get_satilanlar', callable=get_satilanlar)
MyQueue.register('get_reserved', callable=get_reserved)


myqueue = MyQueue(address=('0.0.0.0', 5000), authkey=b'abc')


if __name__ == "__main__":
    myqueue.start()
    while True:
        pass