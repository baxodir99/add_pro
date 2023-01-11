from django.shortcuts import  render, redirect

from apps.authentication.models import User
from .forms import RegisterUserForm
from django.contrib.auth import login, authenticate , logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, 'home.html')

def register_request(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = RegisterUserForm()
	return render (request=request, template_name="registration/signup.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        form.is_valid()
        if form:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.is_superuser == True:
                    return redirect("vc")
                else:
                    return redirect("index")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("home")