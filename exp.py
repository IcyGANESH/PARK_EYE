
import os
import django

# --- Setup Django Environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PARKEYE.settings")  # replace with your project name
django.setup()

from PARK_EYE.models import VehicleRecord
from django.utils import timezone

text=input("Enter no: ")
if text:
    existing_record = VehicleRecord.objects.filter(regs_no=text, in_parking=True).first()

    if existing_record:
        # Vehicle is already in parking — mark exit
        existing_record.out_date_time = timezone.now()
        existing_record.in_parking = False
        existing_record.save()
        print(f"🚗 Exit recorded for: {text} at {existing_record.out_date_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        # New vehicle entry
        VehicleRecord.objects.create(
            regs_no=text,
            in_parking=True,
            in_date_time=timezone.now()
        )
        print(f"✅ Entry recorded for: {text} at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}")      


    # if not VehicleRecord.objects.filter(regs_no=text, in_parking=True).exists():
    #     VehicleRecord.objects.create(
    #         regs_no=text,
    #         in_parking=True
    #     )
    #     print(f"✅ Detected & saved: {text}")
    # else:
    #     print(f"⚠️ Already parked: {text}")




   