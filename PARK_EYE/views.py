from django.shortcuts import render, redirect
from .models import Suspected,Police,VehicleRecord
from django.contrib import messages
from django.utils.timezone import now
# Create your views here.

def register(request):
    records = VehicleRecord.objects.all().order_by('-in_date_time')  # latest first
    return render(request, 'register.html', {'records': records})


def complain(request):
    return render(request, 'complain.html')

def add_suspected_vehicle(request):
    if request.method == 'POST':
        regs_no = request.POST.get('regs_no')
        crime_attempted = request.POST.get('crime_attempted')
        spotted_location = request.POST.get('spotted_location')

        Suspected.objects.create(
            regs_no=regs_no,
            crime_attempted=crime_attempted,
            spotted_location=spotted_location,
            is_founded=False,
            date_time= now()
        )

        return redirect('thanks')  # name of the url pattern for thank you page

    return render(request, 'add_suspect.html')    
def thanks(request):
    return render(request, 'thanks.html')   

def policelogin(request):
    return render(request, 'policelogin.html')

def police_login_check(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            police = Police.objects.get(username=username, password=password)
            request.session['police_id'] = police.id
            return redirect('police_dashboard')  # Redirect to dashboard if login success
        except Police.DoesNotExist:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'police_login.html')


def policedashboard(request):
    police_id = request.session.get('police_id')
    if not police_id:
        return redirect('police_login')

    police = Police.objects.get(id=police_id)
    police_locations = police.locations.values_list('name', flat=True)

    suspected_vehicles = Suspected.objects.filter(found_location__in=police_locations)

    return render(request, 'policedashboard.html', {
        'police': police,
        'suspected_vehicles': suspected_vehicles
    })
