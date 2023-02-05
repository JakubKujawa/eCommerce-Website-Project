from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserProfileForm, UpdateUserForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofileform = UserProfileForm(request.POST)

        if form.is_valid() and userprofileform.is_valid():
            user = form.save()

            userprofile = userprofileform.save(commit=False)
            userprofile.user = user
            userprofile.save()

            login(request, user)

            return redirect('frontpage')
    else:
        form = SignUpForm()
        userprofileform = UserProfileForm()

    return render(request, 'signup.html', {'form': form, 'userprofileform': userprofileform})


@login_required
def myaccount(request):
    return render(request, 'myaccount.html', {"changed": False})


@login_required
def password_change_done(request):
    return render(request, 'myaccount.html', {"changed": True})


@login_required
def update_user(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        userprofileform = UserProfileForm(request.POST, instance=request.user.userprofile)

        if form.is_valid() and userprofileform.is_valid():
            form.save()
            userprofileform.save()
            
            return redirect("myaccount")
    else:
        form = UpdateUserForm(instance=request.user)
        userprofileform = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'update_user.html', {'form': form, 'userprofileform': userprofileform})
