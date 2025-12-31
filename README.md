# 🚗 PARK_EYE – Smart Vehicle Surveillance & Parking System

PARK_EYE is an intelligent vehicle monitoring and smart parking system that uses Computer Vision, OCR, and a Django-based backend to detect suspected or stolen vehicles and manage parking automatically.

The system allows the public to register stolen or suspicious vehicles on a web portal. When a vehicle enters the parking area, the system detects its number plate using OpenCV, extracts the registration number using Tesseract OCR, checks it against the database, and alerts authorities if the vehicle is flagged.

🔍 Features
🚨 Suspicious / Stolen Vehicle Detection

Automatic number plate detection using OpenCV

OCR-based plate recognition using Tesseract

Cross-checking with suspected vehicle database

Automatic update of found location for suspected vehicles

🅿️ Smart Parking Management

Automatic parking slot allocation

Entry and exit time logging

Parking full detection with alert

Slot-wise vehicle tracking

🌐 Django Web Portal

Public registration of suspected/stolen vehicles

Admin vehicle monitoring

Secure database handling using Django ORM

🛠️ Tech Stack
Technology	Usage
Python	Core programming
OpenCV	Image processing & number plate detection
Tesseract OCR	Number plate text extraction
Django	Backend framework
Django ORM	Database management
NumPy & Imutils	Image preprocessing
HTML / CSS	Basic frontend
⚙️ System Workflow

Vehicle image is captured or uploaded.

Image is converted to grayscale and processed using filters.

Edges and contours are detected to locate the number plate.

Tesseract OCR extracts the vehicle registration number.

Django backend checks:

If the vehicle is suspected/stolen

If the vehicle is already inside parking

If parking space is available

System response:

🚨 Alert if suspected vehicle is detected

🅿️ Assign or free parking slot

⏱️ Log entry and exit time

🧠 Parking Slot Logic

Parking layout: 2 × 3 grid (6 slots)

First available slot is assigned automatically

Slot is freed when vehicle exits

Entry denied when parking is full

📂 Project Structure
PARK_EYE/
│
├── images/                  # Vehicle images
├── PARK_EYE/
│   ├── models.py            # VehicleRecord & Suspected models
│   ├── settings.py
│   └── urls.py
│
├── manage.py
├── detection.py             # OpenCV + OCR logic
└── README.md

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/IcyGANESH/PARK_EYE.git
cd PARK_EYE

2️⃣ Install Dependencies
pip install opencv-python numpy imutils pytesseract django pandas

3️⃣ Install Tesseract OCR

Download from: https://github.com/UB-Mannheim/tesseract/wiki

Update the path in code:

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

4️⃣ Run Django Server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

5️⃣ Run Detection Script
python detection.py

🧪 Sample Outputs

✅ Vehicle entry recorded with slot number

🚗 Vehicle exit logged with timestamp

🚨 Alert displayed for suspected vehicle

❌ Parking full warning message

🔮 Future Enhancements

Live CCTV camera integration

Police alerts via SMS / Email

Cloud database integration (Firebase / AWS)

AI-based plate detection (YOLO)

Mobile application support

Admin analytics dashboard

📜 License

This project is developed for educational and research purposes.
