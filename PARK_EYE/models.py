from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class Suspected(models.Model):
    regs_no = models.CharField(max_length=20)
    date_time = models.DateTimeField(default=now)
    crime_attempted = models.CharField(max_length=255,null=True)
    spotted_location = models.CharField(max_length=255,null=True)
    found_location = models.CharField(max_length=255, blank=True, null=True)
    is_founded = models.BooleanField(default=False)               # Description of charges (can be long)

    def __str__(self):
        return f"{self.regs_no} ------------- {self.date_time} ---------------{self.crime_attempted} ------------- {self.is_founded}"


class VehicleRecord(models.Model):
    regs_no = models.CharField(max_length=20)                     # Vehicle registration number
    in_date_time = models.DateTimeField(null=True, blank=True)         # Entry date & time (captured automatically when created)
    out_date_time = models.DateTimeField(null=True, blank=True)    # Exit date & time (can be empty initially)
    in_parking = models.BooleanField(default=True)                 # Checkbox to indicate if vehicle is currently inside

    def __str__(self):
        return f"{self.regs_no} - {'Inside' if self.in_parking else 'Exited'}"

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Police(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)  # hashed password
    locations = models.ManyToManyField(Location)  # can select multiple locations

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.username} ({self.locations})"        
