from django.db import models

# Create your models here.
class Suspected(models.Model):
    regs_no = models.CharField(max_length=20)  # Registration number (text type)
    date = models.DateField()                  # Date field (can auto capture date)
    charges = models.TextField()               # Description of charges (can be long)

    def __str__(self):
        return f"{self.regs_no} ------------------------------------------------------- {self.date} ---------------{self.charges}"


class VehicleRecord(models.Model):
    regs_no = models.CharField(max_length=20)                     # Vehicle registration number
    in_date_time = models.DateTimeField(null=True, blank=True)         # Entry date & time (captured automatically when created)
    out_date_time = models.DateTimeField(null=True, blank=True)    # Exit date & time (can be empty initially)
    in_parking = models.BooleanField(default=True)                 # Checkbox to indicate if vehicle is currently inside

    def __str__(self):
        return f"{self.regs_no} - {'Inside' if self.in_parking else 'Exited'}"
