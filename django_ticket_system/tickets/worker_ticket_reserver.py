from multiprocessing.managers import BaseManager
import datetime

class MyBaseManager(BaseManager):
    pass

MyBaseManager.register('get_reserved')
MyBaseManager.register('get_satilanlar')
MyBaseManager.register('get_biletler')



manager = MyBaseManager(address=('0.0.0.0', 5000), authkey=b'abc')
manager.connect()


class BiletQurtarib(Exception):
    pass

class VaxtBitdi(Exception):
    pass


class TicketReserver:
    BiletQurtarib = BiletQurtarib
    VaxtBitdi = VaxtBitdi

    @staticmethod
    def reserve_ticket(request):

        reserved_dict = manager.get_reserved()
        biletler_queue = manager.get_biletler()

        if biletler_queue.empty():
            raise BiletQurtarib("Bilet qurtarib")

        ticket = biletler_queue.get()
        reserve_time = datetime.datetime.now()
        expire_time = (reserve_time + datetime.timedelta(0, 10, 0, 0, 0)).timestamp()
        reserve_time = reserve_time.timestamp()
        session_key = request.session.session_key

        data = {
            'ticket': ticket,
            'reserve_time': reserve_time,
            'expire_time': expire_time,
            'fullname': '',
        }

        reserved_dict.setdefault(session_key, data)

    @staticmethod
    def confirm_reserve(request):

        reserved_dict = manager.get_reserved()
        biletler_queue = manager.get_biletler()
        satilanlar_queue = manager.get_satilanlar()

        ticket = reserved_dict.get(request.session.session_key)

        if not ticket:
            raise VaxtBitdi("Bileti almaq üçün sizə ayrılan vaxt bitdi")

        ticket.update({
            'fullname': request.POST.get('fullname')
        })

        satilanlar_queue.put(ticket)
        reserved_dict.pop(request.session.session_key)