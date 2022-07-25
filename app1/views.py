from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib import messages
from django.template.loader import render_to_string

# Create your views here.
def home(request):
    categories = Category.objects.all()

    categoryid = request.GET.get('category')
    if categoryid:
        products=Product.objects.filter(category=categoryid)
    else:
        products = Product.objects.all()


    return render(request,'home.html',{'products':products,'categories':categories})


def about(request):
    return render(request,'about.html')

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email'] 
            username = form.cleaned_data['username'] 
            

            if User.objects.filter(email = email).first():      
                messages.info(request, 'Email already exist, Please try different !')
                return HttpResponseRedirect("/signup")

            form.save()
            messages.success(request, 'Congratulation, Registration is Successful')
            html_template = 'welcome.html'
            mydict = {'fname':fname,'lname':lname,'email':email}
            html_message = render_to_string(html_template, context=mydict)
            subject = 'Congratulation, Your Account has been created with Shopkart'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            message = EmailMessage(subject, html_message,
                                   email_from, recipient_list)
            message.content_subtype = 'html'
            message.send()
            return HttpResponseRedirect("/login/")
    form = SignUpForm()
    return render(request, 'signup.html',{'form':form})

def user_login(request):
    if request.method=='POST':
        form = AuthenticationForm(request=request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                print("login successful")
                return HttpResponseRedirect('/')
    form = AuthenticationForm()
    return render(request,'signin.html',{'form':form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')