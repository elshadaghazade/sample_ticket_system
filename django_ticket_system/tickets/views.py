from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib import messages
from .models import Tickets
from .worker_ticket_reserver import TicketReserver

class BuyTicketView(TemplateView):
    model = Tickets
    template_name = 'buy_ticket.html'

    def post(self, request):
        try:

            if request.POST.get('buy_btn'):
                TicketReserver.reserve_ticket(request)
                return render(request, 'confirm_order.html', self.get_context_data())
            elif request.POST.get('confirm_btn'):
                TicketReserver.confirm_reserve(request)
                return redirect('buy_ticket')

        except (TicketReserver.BiletQurtarib, TicketReserver.VaxtBitdi) as err:

            messages.add_message(request, messages.ERROR, str(err))
            return redirect('buy_ticket')

    def get_context_data(self):
        context = super().get_context_data()
        context['messages'] = messages.get_messages(self.request)
        return context