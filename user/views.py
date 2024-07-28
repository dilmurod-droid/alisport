from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required,PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from sport.models import OrderedTariffs
from user.form import UserRegisterForm
from user.models import BotUser
import http.client
import json

class Create_user(LoginRequiredMixin,CreateView):
    model = BotUser
    form_class = UserRegisterForm
    template_name = 'admin/add_user.html'
    success_url = reverse_lazy('home')
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
import requests

def send_sms(phone_number,message):
    conn = http.client.HTTPSConnection("rgnxwl.api.infobip.com")
    payload = json.dumps({
        "messages": [
            {
                "destinations": [{"to": f"{phone_number}"}],
                "from": "ServiceSMS",
                "text": f"{message}"
            }
        ]
    })
    headers = {
        'Authorization': '761e44e68b5a44c4b9fd8f67560de352-64c15892-2691-4123-aaf8-92fec105814c',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

# ServiceSMS
@login_required
def user_list_view(request):
    users = BotUser.objects.all()
    for user in users:
        current_tariffs = OrderedTariffs.objects.filter(user=user, is_active=True)
        user.current_tariffs = current_tariffs
    query = request.GET.get('q')
    if query:
        users = users.filter(phone_number__endswith=query)
        for user in users:
            current_tariffs = OrderedTariffs.objects.filter(user=user, is_active=True)
            user.current_tariffs = current_tariffs
        print(users)
    return render(request, 'admin/user_list.html', {'users': users, 'query': query})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('choice_tariff')
        else:
            return HttpResponse('Invalid login')
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})
@login_required
def delete_user_view(request, user_id):
    user = get_object_or_404(BotUser, id=user_id)
    if request.method == 'POST':
        send_sms(user.phone_number, f"\
Hurmatli {user.username},\n\n\
Sizning hisobingiz o'chirildi.\n\n\
Rahmat,\n\
Ali Fitness Zali jamoasi")
        user.delete()
        return redirect('user_list')
    return render(request, 'admin/confirm_delete.html', {'user': user})

@login_required
def send_sms_to_user_view(request, user_id):
    user = get_object_or_404(BotUser, id=user_id)
    if request.method == 'POST':
        resp=send_sms(user.phone_number, f"\
                Hurmatli {user.username},\n\n\
                Sizni Ali Fitness Zali jamoasidan bezovta qilayotgan edik. Sizning abonement to'lovingiz muddati tugaganligini bildirmoqchimiz. Iltimos, keyingi trenirovka uchun to'lovni amalga oshirishingizni so'raymiz.\n\n\
                Rahmat,\n\
                Ali Fitness Zali jamoasi")
        if resp:
            print(resp)

        return redirect('user_list')
    return render(request, 'admin/send_sms.html', {'user': user})