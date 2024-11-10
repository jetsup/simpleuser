from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User,parkingslot

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=User
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('username','email','phone_number','id_number','password1','password2','is_staff','is_active')
        }),
    )
    
class parkingslotadmin(admin.ModelAdmin):
    #display these fields in the list view
    list_display=('slot_number','user','vehicle_type','number_plate','rfid_card','amount_paid','start_time','end_time') 
    #add search functionality (based on user and slot number)
    search_fields=('user','slot_number')
    
    #add filters based on the vehicle type  and slot number
    list_filter=('vehicle_type','slot_number')  
    
    #make this fields read-only in the admin interface(if needed)
    readonly_fields=['start_time']
    
    #organie fields into sections
    fieldsets=(
        ('Slot Information',{
            'fields':('slot_number','rfid_card')
        }),
        ('Vehicle Information',{
            'fields':('vehicle_type','number_plate')
        }),
        ('Time Information',{
            'fields':('start_time','end_time')
        }),
        ('Payment Information',{
            'fields':['amount_paid']
        })
    )
    add_fieldsets=(
        (None,{
            'classes':('wide',),
            'fields':('slot_number','user','vehicle_type','number_plate','rfid_card','amount_paid','start_time','end_time')
        }),
    )
    #register the customuseradmin
admin.site.register(User,CustomUserAdmin)
    #register parkingslot admin
admin.site.register(parkingslot,parkingslotadmin)