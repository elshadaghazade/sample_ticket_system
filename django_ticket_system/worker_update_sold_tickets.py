import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ticket_system.settings')

import django
django.setup()

from multiprocessing.managers import BaseManager
import datetime
from tickets.models import Tickets


class MyBaseManager(BaseManager):
    pass


class UpdateSolvedTickets:
    
    def __init__(self):
        MyBaseManager.register('get_reserved')
        MyBaseManager.register('get_satilanlar')
        MyBaseManager.register('get_biletler')



        self.manager = MyBaseManager(address=('0.0.0.0', 5000), authkey=b'abc')
        self.manager.connect()

        self.satilanlar_queue = self.manager.get_satilanlar()

    def start(self):
        while True:
            ticket = self.satilanlar_queue.get()
            ticket_obj = Tickets.objects.get(pk=ticket.get('ticket'))
            ticket_obj.alici=ticket.get('fullname')
            ticket_obj.satilib=True
            ticket_obj.save()


if __name__ == "__main__":
    UpdateSolvedTickets().start()