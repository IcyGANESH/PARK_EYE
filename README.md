# PARK_EYE – Smart Vehicle Surveillance & Parking System

PARK_EYE is an intelligent vehicle monitoring system that combines Computer Vision, OCR, and Django-based backend services to detect suspected or stolen vehicles and provide a smart parking management solution.

The system allows the public to register suspicious or stolen vehicles on a web portal. When a vehicle enters the parking area, PARK_EYE automatically detects the number plate, checks it against the database, and alerts authorities if the vehicle is flagged, while also managing parking slots efficiently.

KEY FEATURES
• Crime & Suspicious Vehicle Detection using OpenCV and Tesseract OCR
• Automatic number plate recognition
• Real-time comparison with suspected/stolen vehicle database
• Smart parking slot allocation (entry/exit tracking)
• Parking full alert system
• Django-based web portal and database

TECH STACK
Programming Language: Python
Computer Vision: OpenCV
OCR Engine: Tesseract OCR
Backend Framework: Django
Database: Django ORM (SQLite/MySQL)
Image Processing: NumPy, Imutils
Frontend: Basic HTML/CSS

SYSTEM WORKFLOW
1. Vehicle image is captured or uploaded.
2. OpenCV detects number plate using edge detection and contours.
3. Tesseract OCR extracts the registration number.
4. Django backend checks:
   - If vehicle is suspected/stolen
   - If vehicle already exists in parking
   - Parking availability
5. System takes action:
   - Alerts if suspected vehicle found
   - Assigns or frees parking slot
   - Logs entry and exit timestamps

PARKING SLOT LOGIC
• 2x3 grid (6 slots total)
• First empty slot is assigned
• Slot freed on vehicle exit
• Entry denied when parking is full

FUTURE ENHANCEMENTS
• Live CCTV integration
• Police alert via SMS/Email
• Cloud database integration
• AI-based detection (YOLO)
• Mobile application

AUTHOR
Ganesh
GitHub: https://github.com/IcyGANESH

LICENSE
This project is intended for educational and research purposes.
