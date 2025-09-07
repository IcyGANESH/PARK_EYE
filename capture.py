import numpy as np
import cv2
import imutils
import pytesseract
import pandas as pd
import time
import os
import django
import re

# --- Setup Django Environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PARKEYE.settings")  # replace with your project name
django.setup()

from PARK_EYE.models import VehicleRecord,Suspected
from django.utils import timezone

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import cv2
from django.utils import timezone
from PARK_EYE.models import VehicleRecord, Suspected

# Load active vehicles into memory and initialize slot grid
slots = [['' for _ in range(3)] for _ in range(2)]
active_vehicles = VehicleRecord.objects.filter(in_parking=True)

for vehicle in active_vehicles:
    if vehicle.slot_position:
        i, j = int(vehicle.slot_position[0]), int(vehicle.slot_position[1])
        slots[i][j] = vehicle.regs_no

def database(text):
    global slots

    if not text:
        return

    # Step 1: Check suspected list
    suspected = Suspected.objects.filter(regs_no=text).exists()
    if suspected:
        print(f"🚨 ALERT: Suspected vehicle detected: {text}\n")
        Suspected.objects.filter(found_location__isnull=True).update(found_location="KIET Group Of Institutions, Muradnager, Ghaziabad")

    # Step 2: Check if vehicle is already inside
    existing_record = VehicleRecord.objects.filter(regs_no=text, in_parking=True).first()

    if existing_record:
        # Mark exit
        pos = existing_record.slot_position
        if pos:
            i, j = int(pos[0]), int(pos[1])
            slots[i][j] = ''

        existing_record.out_date_time = timezone.now()
        existing_record.in_parking = False
        existing_record.save()
        print(f"🚗 Exit recorded for: {text} at {existing_record.out_date_time.strftime('%Y-%m-%d %H:%M:%S')} from slot '{pos}'")

    else:
        # Step 3: Check if parking is full
        total_filled = sum(1 for row in slots for val in row if val)
        if total_filled >= 6:
            print("❌ Parking Full — Cannot allow new vehicle.")
            msg_img = np.zeros((100, 400), dtype=np.uint8)
            cv2.putText(msg_img, "Parking Full! Entry Denied.", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 255, 2)
            cv2.imshow("❌ ALERT", msg_img)
            cv2.waitKey(0)
            cv2.destroyWindow("❌ ALERT")
            return

        # Step 4: Assign to first empty slot
        found = False
        for i in range(2):
            for j in range(3):
                if slots[i][j] == '':
                    slots[i][j] = text
                    slot_pos = f"{i}{j}"
                    found = True
                    break
            if found:
                break

        # Step 5: Save to DB
        VehicleRecord.objects.create(
            regs_no=text,
            in_parking=True,
            in_date_time=timezone.now(),
            slot_position=slot_pos
        )
        print(f"✅ Entry recorded for: {text} at {timezone.now().strftime('%Y-%m-%d %H:%M:%S')} at slot '{slot_pos}'")

    # Step 6: Show slot status
    print("\nCurrent Parking Slots:")
    for i in range(2):
        for j in range(3):
            print(f"Slot {i}{j}: {slots[i][j] if slots[i][j] else 'Empty'}")

# variable which takes cars image input name
car_nam = input("\nEnter the name of the image file (with extension): ")
# Load and resize the image
img = cv2.imread('images\\' + car_nam)
img = imutils.resize(img, width=500)
cv2.imshow("ORIGINAL IMAGE", img)

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply bilateral filter to reduce noise while keeping edges sharp
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Detect edges
edged = cv2.Canny(gray, 170, 200)

# Find contours and sort by area
cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
NumberPlateCnt = None

# Try to find a rectangular contour (number plate)
for c in cnts:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        NumberPlateCnt = approx
        break

# If number plate is detected
if NumberPlateCnt is not None:
    # Create a mask and extract the region of interest (ROI)
    mask = np.zeros(gray.shape, np.uint8)
    cv2.drawContours(mask, [NumberPlateCnt], 0, 255, -1)
    masked_img = cv2.bitwise_and(img, img, mask=mask)

    # Crop the region of interest
    x, y, w, h = cv2.boundingRect(NumberPlateCnt)
    plate_img = gray[y:y+h, x:x+w]

    # Preprocess for OCR
    plate_img = cv2.resize(plate_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    plate_img = cv2.bilateralFilter(plate_img, 11, 17, 17)
    plate_img = cv2.threshold(plate_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cv2.imshow("Final Plate", plate_img)

    # Run OCR
    config = '-l eng --oem 1 --psm 7'
    text = pytesseract.image_to_string(plate_img, config=config).strip()
    text = re.sub(r'[^A-Za-z0-9]', '', text)  # Remove unwanted characters
    text = text.replace(" ", "")  # Remove spaces  

    print("\nDetected Number Plate:", text)
    # for admin django update 
    database(text)



else:
    print("Number plate contour not detected.")

# Interactive close loop
print("\nPress 'q' to exit the image windows.")
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()