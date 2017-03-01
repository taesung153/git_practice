from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
import time
import datetime
from datetime import datetime
from datetime import date
from datetime import time
from django.utils import timezone
from .models import Appt
from ..LoginReg.models import User

def dashboard(request):
	print "DASHBOARD"
	if not 'user_id' in request.session:
		messages.error(request, "Not logged in, please login or register")
		return redirect("LoginReg:index")

	this_date = datetime.now().date()
	this_time = datetime.now().time()
	today_appts = Appt.objects.filter(date=this_date)
	future_appts = Appt.objects.filter(date__gt=this_date)
	context = {
		'this_date': this_date,
		'this_time': this_time,
		'today_appts': today_appts,
		'future_appts': future_appts
	}
	return render(request, "Appointment/dashboard.html", context)

def create_appt(request):
	print "CREATE_APPT"
	if request.method != "POST":
		return redirect("Appointment:dashboard")
	errors=[]
	appt_date = request.POST['appt_date']
	appt_time = request.POST['appt_time']
	appt_task = request.POST['appt_task']
	this_date = str(datetime.now().date())
	print "Dates:", appt_date, this_date
	if appt_date < this_date:
		errors.append('Must enter a current or future date')
	if str(appt_time) == "":
		errors.append('Must enter a time')
	if appt_task == "":
		errors.append('Must enter a task')
	if errors:
		for error in errors:
			messages.error(request, error)
		print "Failed"
	else:
		response = Appt.objects.create(task=appt_task, date=appt_date, time=appt_time, status="Pending")
		print "Done"
	return redirect("Appointment:dashboard")

def edit_appt(request, appt_id):
	print "EDIT_APPT"
	context = {
		'this_date': datetime.now().date(),
		'this_time': datetime.now().time(),
		'appt': Appt.objects.get(id=appt_id)
	}
	return render(request, "Appointment/edit.html", context)

def update_appt(request, appt_id):
	print "UPDATE_APPT"
	if request.method != "POST":
		return redirect("Appointment:dashboard")
	appt_date = request.POST['appt_date']
	appt_time = request.POST['appt_time']
	appt_task = request.POST['appt_task']
	appt_status = request.POST['appt_status']
	errors=[]
	this_date = str(datetime.now().date())
	print "Dates:", appt_date, this_date
	if appt_date < this_date:
		errors.append('Must enter a current or future date')
	if str(appt_time) == "":
		errors.append('Must enter a time')
	if appt_task == "":
		errors.append('Must enter a task')
	if errors:
		for error in errors:
			messages.error(request, error)
		print "Failed"
	else:
		appt = Appt.objects.get(id=appt_id)
		appt.date = appt_date
		appt.time = appt_time
		appt.task = appt_task
		appt.status = appt_status
		appt.save()
		print "Done"
	return redirect("Appointment:dashboard")

def delete_appt(request, appt_id):
	print "DELETE_APPT"
	appt = Appt.objects.get(id=appt_id)
	appt.delete()
	return redirect("Appointment:dashboard")

def logout(request):
    request.session.flush()
    return redirect('/')

def logout2(request):
	request.session.flush()
	return render(request, "loginreg:index")
