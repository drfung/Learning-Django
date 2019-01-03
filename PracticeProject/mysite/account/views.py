from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .froms import LoginForm,RegistrationForm,UserProfileForm,UserForm,UserInfoForm
from . models import UserInfo,UserProfile
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# Create your views here.

def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username = cd.get("username"),
                                password = cd.get("password"))

            if user:
                login(request, user)
                return HttpResponse("Wellcome You. You have been authenticated successfully.")
            else:
                return HttpResponse("Sorry. Your username or password is not right.")

    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form": login_form})

def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid()*userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            UserInfo.objects.create(user=new_user)
            return HttpResponseRedirect(reverse("account:user_login"))
        else:
            return HttpResponse("sorry,your can not register")
    else:
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form": user_form,"profile": userprofile_form})

@login_required(login_url='/account/login/')
def myself(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)
    return render(request,'account/myself.html',{"user": user, "userinfo": userinfo, "userprofile": userprofile})

@login_required(login_url='/account/login/')
def myself_edit(request):
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=user)
    userinfo = UserInfo.objects.get(user=user)

    if request.method == "POST":
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form = UserInfoForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            user.email = user_cd.get("email")
            userprofile.birth = userprofile_cd.get("birth")
            userprofile.phone = userprofile_cd.get("phone")
            userinfo.school = userinfo_cd.get("school")
            userinfo.profession = userinfo_cd.get("profession")
            userinfo.address = userinfo_cd.get("address")
            userinfo.company = userinfo_cd.get("company")
            userinfo.aboutme = userinfo_cd.get("aboutme")
            user.save()
            userprofile.save()
            userinfo.save()
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={
            'birth': userprofile.birth,
            'phone': userprofile.phone
        })
        userinfo_form = UserInfoForm(initial={
            'school': userinfo.school,
            'profession': userinfo.profession,
            'address': userinfo.address,
            'company': userinfo.company,
            'aboutme': userinfo.aboutme
        })
        return render(request,'account/myself_edit.html',{
            'user_form': user_form,
            'userprofile_form': userprofile_form,
            'userinfo_form': userinfo_form
        })


def my_image(request):
    if request.method == "POST":
        # img = request.POST.get('img')
        img = request.POST['img']
        print(img)
        print('bbbb')
        userinfo = UserInfo.objects.get(user=request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse('1')
    return render(request, 'account/imagecrop.html')