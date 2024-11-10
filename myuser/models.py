from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import timedelta,datetime


# Create your models here.
class User(AbstractUser):
    email=models.EmailField( max_length=254,unique=True,verbose_name='Email Address')
    phone_number=models.CharField(max_length=10,blank=False)
    id_number=models.CharField(max_length=8,blank=False)
    
    REQUIRED_FIELDS=['email','phone_number','id_number']
    
    def __str__(self):
        return self.username

#parkingslots

class parkingslot(models.Model):
    VEHICLE_TYPE_CHOICES=[
        ('Car','Car'),
        ('Bike','Bike'),
        ('Truck','Truck'),
        ('Tuk Tuk','Tuk Tuk'),
        ('Van','Van'),
        ('Bus','Bus'),
    ]
    slot_number=models.PositiveIntegerField(unique=True)
    vehicle_type=models.CharField(max_length=10,choices=VEHICLE_TYPE_CHOICES,blank=True,null=True)
    number_plate=models.CharField(max_length=15,blank=True,null=True)
    rfid_card=models.CharField(max_length=20,blank=True,null=True)
    hours_parked=models.PositiveIntegerField(default=0)
    amount_paid=models.DecimalField(max_digits=8,decimal_places=2,default=0.00)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='parking_slots',blank=True,null=True)
    start_time=models.DateTimeField(null=True,blank=True)
    end_time=models.DateTimeField(null=True,blank=True)
    
    #method to assign slots
    def park_vehicle(self,user,vehicle_type,rfid_card,number_plate):
        if self.vehicle_type:
            raise ValueError(f"slot {self.slot_number} is already occupied.")
        self.vehicle_type=vehicle_type
        self.number_plate=number_plate
        self.rfid_card=rfid_card
        self.user=user
        self.start_time=datetime.now()
        self.save()
    #method to free the slot, calculate the amount paid, and mark it available
    def free_slot(self):
        if not self.start_time:
            raise ValueError(f"slot {self.slot_number}is not occcupied")
        #calculate hours parked and the amount paid
        self.end_time=datetime.now()
        hourly_rate=50
        total_hours=(self.end_time-self.start_time).total_seconds()//3600
        self.hours_parked=total_hours
        self.amount_paid=total_hours*hourly_rate
        self.save()
        #clear the slot for future use
        self.vehicle_type=None
        self.number_plate=None
        self.rfid_card=None
        self.user=None
        self.start_time=None
        self.end_time=None
        self.save()
        
    def __str__(self):
        return f"Slot{self.slot_number}-{self.number_plate}"