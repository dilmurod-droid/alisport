from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse

from user.models import BotUser
from .models import  Tariff, OrderedTariffs, Payment
import datetime

@login_required

def home_view(request):
    return render(request, 'admin/home.html')

@login_required
def choice_tariff_view(request):
    tariffs = Tariff.objects.all()
    users = BotUser.objects.all()  # Fetch all users

    if request.method == 'POST':
        tariff_id = request.POST.get('tariff')
        user_id = request.POST.get('user')

        if tariff_id and user_id:
            try:
                tariff = Tariff.objects.get(id=tariff_id)
                user = BotUser.objects.get(id=user_id)

                # Create or update OrderedTariffs entry
                ordered_tariff, created = OrderedTariffs.objects.get_or_create(
                    user=user,
                    tariff=tariff,
                    defaults={
                        'days': tariff.days,
                        'end_date': datetime.datetime.now().date() + datetime.timedelta(days=tariff.days),
                        'is_active': True
                    }
                )

                if not created:
                    # If entry already exists, you might want to update it
                    ordered_tariff.days = tariff.days
                    ordered_tariff.end_date = datetime.datetime.now().date() + datetime.timedelta(days=tariff.days)
                    ordered_tariff.is_active = True
                    ordered_tariff.save()

                return redirect('home')  # Redirect to a success page or another view
            except (Tariff.DoesNotExist, BotUser.DoesNotExist):
                # Handle the case where the tariff or user does not exist
                pass

    return render(request, 'admin/choice_tariff.html', {'tariffs': tariffs, 'users': users})
@login_required
def admin_panel_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                bot_user = BotUser.objects.filter(username=username).first()
                if bot_user:
                    bot_user.delete()
                user.delete()
                return HttpResponse(f'User {username} deleted')
        phone_number = request.POST.get('phone_number')
        if phone_number:
            # Kod yuborish logikasi
            return HttpResponse(f'Code sent to {phone_number}')
    return render(request, 'admin/admin_panel.html')