import numpy as np
import cv2
import imutils
import pytesseract
import pandas as pd
import time
import os
import django

# --- Setup Django Environment ---
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PARKEYE.settings")  # replace with your project name
django.setup()

from PARK_EYE.models import VehicleRecord
from django.utils import timezone

# Path to tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Function defining :-
def database(text):
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
    

# variable which takes cars image input name
car_nam = input("Enter the name of the image file (with extension): ")
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

#     

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