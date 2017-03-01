from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
	return render(request, "LoginReg/index.html")

def register(request):
	print "REGISTER"
	if request.method == "POST":
		response = User.objects.register(request.POST)
		if response['status'] == False:
			for error in response['errors']:
				messages.error(request, error)
			return redirect("LoginReg:index")
		else:

			this_user = response['user']
			print "THIS USER ", this_user.id
			request.session['user_id'] = this_user.id
			request.session['name'] = this_user.name
			return redirect("Appointment:dashboard")
	else:
		return redirect("LoginReg:index")

def login(request):
	print "LOGIN"
	if request.method == "POST":
		response = User.objects.login(request.POST)
		if response['status'] == False:
			for error in response['errors']:
				messages.error(request, error)
			return redirect("LoginReg:index")
		else:
			this_user = response['user']
			print "THIS USER ", this_user.id
			request.session['user_id'] = this_user.id
			request.session['name'] = this_user.name
			return redirect("Appointment:dashboard")
	else:
		return redirect("LoginReg:index")

def logout(request):
	print "LOGOUT"
	if not 'user_id' in request.session:
		messages.error(request, "Not logged in, please login or register")
		return redirect("LoginReg:index")
	if request.method == "POST":
		request.session.clear()
	return redirect("LoginReg:index")
