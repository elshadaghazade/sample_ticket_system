import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ticket_system.settings')

import django
django.setup()

from multiprocessing.managers import BaseManager
from tickets.models import Tickets
import time

class Collector:

    def __init__(self):
        BaseManager.register('get_biletler')
        BaseManager.register('get_satilanlar')
        BaseManager.register('get_reserved')

        self.manager = BaseManager(address=('0.0.0.0', 5000), authkey=b'abc')
        self.manager.connect()

        self.biletler_queue = self.manager.get_biletler()
        self.satilanlar_queue = self.manager.get_satilanlar()
        self.reserved_dict = self.manager.get_reserved()

    def start(self):
        while True:
            try:
                qs = Tickets.objects.filter(satilib=0)
                for ticket in qs:
                    print(ticket)
                    if not self.check_ticket_existance(ticket.id):
                        self.biletler_queue.put(ticket.id)
            except Exception as err:
                print(err)
                continue
            time.sleep(10)

    def check_ticket_existance(self, ticket_id):
        # searching in reserved dictionary
        for reserved_ticket in self.reserved_dict.values():

            if reserved_ticket and reserved_ticket.get('ticket') and ticket_id == reserved_ticket.get('ticket'):
                return True
        
        # check in satilanlar_queue
        return self.satilanlar_queue.contains(ticket_id)

if __name__ == "__main__":
    Collector().start()