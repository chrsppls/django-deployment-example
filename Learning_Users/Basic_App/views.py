from django.shortcuts import render
from Basic_App.forms import UserForm, UserProfileInfoForm

# Login Requirements
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'Basic_App/index.html')

@login_required
def special(request):
    return HttpResponse("Your are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Do not save at first to avoid data collisions, first add a user to profile object, then check for pic and save after
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {
    'user_form': user_form,
    'profile_form':profile_form,
    'registered':registered,
    }

    return render(request, 'Basic_App/registration.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            print("This was a failed login attempt")
            print("Username {} and password {}".format(username,password))
            return HttpResponse("Invalid Login Details Provided")
    else:
        return render(request, 'Basic_App/login.html', {})