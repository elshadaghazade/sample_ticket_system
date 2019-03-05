import os

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_ticket_system.settings')

import django
django.setup()

from tickets.models import Tickets
from django.contrib.auth.models import User

print(User.objects.all())