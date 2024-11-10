from django import forms
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,AuthenticationForm
from .models import User,parkingslot

class myusercreationform(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model=User
        fields=('username','email','first_name','last_name','id_number','phone_number',)
        
        def clean_email(self):
            email=self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError('email is already registered')
            return email
        def clean_id_number(self):
            id_number=self.cleaned_data.get('id_number')
            if User.objects.filter(id_number=id_number).exists():
                raise forms.ValidationError('id_number aready exists')
            return id_number
        
class myuserauthenticationform(AuthenticationForm):
    class Meta:
        model=User
            

#form for booking a slot
class SlotBookingForm(forms.ModelForm):
    class Meta:       
        model=parkingslot
        fields= ['slot_number','vehicle_type','number_plate','rfid_card']    #fields in the form
        
        def __init__ (self,*args,**kwargs):
            super(SlotBookingForm,self).__init__(*args,**kwargs)
            #only show available slots (those without a vehicle)
            self.fields['slot_number'].queryset=parkingslot.objects.filter(vehicle_type_isnull=True)
        
        def clean_slot_number(self):
            #custom validation to ensure slot number is still available
            slot=self.cleaned_data['slot_number']
            if slot.vehicle_type:
                raise forms.ValidationError(f"slot {slot.slot_number} is already occupied. ")
            return slot
    
    