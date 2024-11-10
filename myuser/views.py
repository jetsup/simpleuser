from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .forms import myusercreationform,myuserauthenticationform,SlotBookingForm
from django.contrib.auth.decorators import login_required
from .models import parkingslot
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail
from django.http import HttpRequest, JsonResponse

# Create your views here.
def register_view(request):
    form=myusercreationform()
    if request.method=="POST":
        form=myusercreationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('welcome')
    else:
        form=myusercreationform()
    return render(request,"register.html",{'form': form})

def login_view(request):
    if request.method=="POST":
        form=myuserauthenticationform(request,data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('welcome')
    else:
        form=myuserauthenticationform()
    return render(request,'login.html',{'form':form})
#logout_view
def logout_view(request):
    logout(request)
    return redirect('login')

#booking_view
@login_required
def booking_view(request):
    return render(request,'booking.html')


#home_view
#@login_required
def welcome_view(request):
    return render(request,'welcome.html')

#profile_view
@login_required
def profile_view(request):
    active_slot=parkingslot.objects.filter(user=request.user)
    return render(request,'profile.html',{'active_slot':active_slot})
    
#About_view
@login_required
def about_view(request):
    return render(request,'about.html')

def base_view(request):
    return render(request,'base.html')

#booking_view
@login_required
def booking_view(request: HttpRequest):
    if request.method=='POST':
        form = SlotBookingForm(request.POST)

        print("form is valid: ", form.is_valid())

        if form.is_valid():
            slot=form.save(commit=False)  #save the form data without commiting to the db yet
            slot.user=request.user #Assign the current user to the parking slot
            slot.start_time=datetime.now() #set the start time to the current time
            slot.save()                     #now save the slot to the db
            
            messages.success(request, f"vehicle {slot.number_plate} parked in slot.slot_number,")
            return redirect('booking')    #redirect to avoid form resubmision
    else:
        form=SlotBookingForm()
    #fetch all slots to show their current status
    parking_slots=parkingslot.objects.all().order_by('slot_number')
    return render(request,'booking.html', {'form':form, 'parking_slots':parking_slots})

#view for ending a booking session
def end_booking(request,slot_id):
    #get the booking slot
    slot=get_object_or_404(parkingslot,id=slot_id)
    if request.method=='POST':
        slot.delete()
        return redirect('booking')
    return render(request,'profile.html',{'slot':slot})
    
    # if slot.end_time is not None:
    #     messages.erro(request,"this booking has alread been ended")
    #     return redirect('booking')
    # hours_parked,amount_paid=slot.free_slot()
    # #set end time to the current time
    # slot.end_time=datetime.now()
    
    # #calculate the total hours parked
    # duration =slot.end_time-slot.start_time
    # total_hours=duration.total_seconds()/3600
    
    # #rate of 100 bob per hour
    # rate_per_hour=100
    # total_amount=total_hours*rate_per_hour
    # #save the changes to the booking
    # slot.save()
    # #send the email to the user with payment details
    # send_mail(
    #     'your parking session summary',
    #     f'thank you for using our parking system. you have parked for {hours_parked:.2f}hours'
    #     f'your total amount to be paid is Ksh{amount_paid:.2f}.',
    #     'smartpark@gmail.com' #from email address
    #     [request.user.email], #to the email address
    #     fail_silently=False,
    # )
    # messages.success(request,f'your booking has beeb ended . you have parked for{hours_parked:.2f}hours an email with payment details has been sent')
    # return redirect('booking')# redirect to the booking page after ending the session

def search_user(request: HttpRequest):
    if request.method == "POST":
        pass
    elif request.method == "GET":
        card_info = request.GET.dict()
        user_card = card_info.get("user-card")
        try:
            user = parkingslot.objects.get(rfid_card=user_card)
        except Exception as e:
            print("User does not exist:", e)
            return JsonResponse(
                {
                    "status": "error",
                    "message": "User does not exist. Consult the admin",
                }
            )
        print("Card Details: ", user, user_card)
        print("IN USER:", user)
        slot = user #parkingslot.objects.get(user=user)
        if slot:
            print("SLOT:", slot, user)
            msg = "Allocated " + str(slot.slot_number) + " is_occupied: " + str(slot.user!=None)
            return JsonResponse(
                {
                    "status": "success",
                    "message": msg,
                }
            )
        else:
            print("SLOT:", slot, user)
            return JsonResponse(
                {
                    "status": "warning",
                    "message": "You should book your slot from our website",
                }
            )
