from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage, send_mail
from webproject import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from .tokens import generate_token
import random
from .models import signup
from .forms import SignupForm
import random
from django.contrib.auth.hashers import make_password,check_password
from .encrypt_util import *
from cryptography.fernet import Fernet
from .encrypt import *
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_list_or_404, get_object_or_404
# from django.contrib.auth.context_processors.auth

Global_code = random.randrange(1, 10**5)



def home(request):
    return render(request, "first.html")

def signup_page(request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user_name = request.POST["UserName"]
            # request.POST["ConfirmationCode"] = random.randrange(1, 10**5)
            saveform = form.save()
            saveform.Password = encrypt(saveform.Password)
            print("saveformPassword",saveform.Password)
            saveform.ConfirmPassword = encrypt(saveform.ConfirmPassword)
            # saveform.Password = cryptocode.encrypt(saveform.Password, "password")
            # saveform.ConfirmPassword = cryptocode.encrypt(saveform.ConfirmPassword, "password")
            saveform.save()
            print("saveform",saveform)
            User = signup.objects.get(UserName = user_name)
            print("User",User)
            messages.success(request, "Your Account has been created succesfully!! We have sent welcome message to your email.")
            subject = "Welcome to Digital Library - Django Login!!"
            message = "Hello " + User.FirstName + "!! \n" + "Welcome to Digital Library Search Engine With Wiki-Cards!! \nThank you for visiting my website\n. This is welcome mail. \n\n Thanking You\n BinduPriya Bondalapati"        
            from_email = settings.EMAIL_HOST_USER
            to_list = [User.Email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
        
            return redirect('signin')

            
    else:
        form = SignupForm()
    return render(request, 'signup.html',{'form':form})

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    username = ""
    if request.method == 'POST':
        data = request.POST.dict()
        email = data.get("Email")
        password = data.get("Password")
        User = signup.objects.get(Email = email)
        username = User.UserName
        dp = decrypt(User.Password)
        print("dp",dp)
        # checkpassword = check_password(password,User.Password)
        if email == User.Email and password == dp:
            msg_html = "Please copy and paste this code to login to the dashboard   " + str(Global_code)
            user_email = [email]
            send_mail('Confirmation Code', msg_html, settings.EMAIL_HOST_USER, user_email, fail_silently=True)
            return redirect('confirm_code/'+str(User.id))
            # return render(request, "confirm_code.html")
            
        else:
            messages.error(request,"Invalid credentials") 
    
    return render(request, "signin.html",{'uname':username})

def send_mail_forget_pw(request,uname):
    if uname:
        print(uname)
        User = signup.objects.get(UserName = uname)
        email = User.Email
        print(email)
        msg_html = "Please click on link to reset password   " + str("http://127.0.0.1:8000/reset_password/")+str(uname)
        user_email = ["bbond010@odu.edu"]
        send_mail('django test mail', msg_html, settings.EMAIL_HOST_USER, user_email, fail_silently=True)
        return HttpResponseRedirect("/reset_password/"+str(uname))
    return render(request, "signin.html",{'uname':username})
            
def send_email_to_reset_pw(request):
    if request.method == "POST":
        data = request.POST.dict()
        user_email = data.get('Email')
        User = signup.objects.get(Email = user_email)
        messages.success(request, "Email sent to reset password")
        msg_html = "Please click on link to reset password   " + str("http://127.0.0.1:8000/reset_password/")+str(User.UserName)
        user_email = [user_email]
        send_mail('django test mail', msg_html, settings.EMAIL_HOST_USER, user_email, fail_silently=True)
    return render(request, "forget_password.html")

def reset_password(request,uname):
    User = signup.objects.get(UserName = uname)
    email = User.Email
    print(email)
    if request.method == "POST":
        data = request.POST.dict()
        pw = data.get('Password')
        cpw = data.get('ConfirmPassword')
        print(pw)
        print(cpw)
        if pw == cpw:
            User.Password = encrypt(pw)
            User.ConfirmPassword = encrypt(pw)
            User.save()
            messages.success(request,"Your password is succesfully reset")
    return render(request, "reset_password.html",{'email':email,'uname':uname})





def signout(request,id):
    print("pk",id)
    return render(request, "signout.html",{'id':id})


def confirm_code(request,id):
    print("id",id)
    if request.method == 'POST':
        print("Global_code",Global_code)
        confirm_code = request.POST['Confirmation']
        if (str(Global_code) == str(confirm_code)):
            print("yes")
            return redirect('/signout/'+str(id))
    return render(request, "confirm_code.html",{'id':id})

def signout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def base(request,id):
    return redirect('/signout/'+str(id))
    # enter_the_dashboard = True
    # return render(request, "index.html", {'enter_the_dashboard':enter_the_dashboard})




def view_profile(request,id):
    User = signup.objects.get(pk = int(id))
    print(User)
    return render (request,"view_profile.html", {'User':User})

def change_profile(request):
    pass



def updateinfo(request,id):
    return render (request,"updateinfo.html",{'id':id})

def updateuserinfo(request,id):
    User = signup.objects.get(pk = int(id))
    if request.method == "POST":
        data = request.POST.dict()
        FName = data.get('FirstName')
        LName = data.get('LastName')
        PNum = data.get('PhoneNumber')
        User.FirstName = FName
        User.LastName = LName
        User.PhoneNumber = PNum
        User.save()
        messages.success(request, "Updated succesfully")
    return render (request,"userupdateinfo.html")





# def ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
def ChangePasswordView(request,id):
    User = signup.objects.get(pk = int(id))
    if request.method == "POST":
        data = request.POST.dict()
        Old_pw = data.get('OldPassword')
        New_pw = data.get('NewPassword')
        Confirm_pw = data.get('ConfirmPassword')
        print(decrypt(User.Password))
        print((Old_pw))
        print(New_pw)
        print(Confirm_pw)
        if decrypt(User.Password) == (Old_pw):
            if New_pw == Confirm_pw:
                User.Password = encrypt(New_pw)
                User.ConfirmPassword = encrypt(New_pw)
                User.save()
                messages.success(request,"Updated successfully")
            else:
                messages.error(request, "Your password and Confirm Password didnot match")
        else:
            messages.error(request, "Please enter the correct password to update")
    return render (request,"change_password.html")

    # template_name = 'change_password.html'
    # success_message = "Successfully Changed Your Password"
    # success_url = reverse_lazy('base')
    
 








