from django.contrib import admin

from sport.models import Tariff,OrderedTariffs
from user.models import BotUser
admin.site.register(Tariff)
admin.site.register(BotUser)
admin.site.register(OrderedTariffs)