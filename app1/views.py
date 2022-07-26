from django.shortcuts import render
from .models import Product, Category,Cart, ShippingDetail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from .forms import SignUpForm, ShippingForm
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
    return HttpResponseRedirect('/login/')

def add_to_cart(request):
        user= request.user
        product_id =  request.GET.get('pid')
        product = Product.objects.get(id=product_id)
        Cart(product=product,user=user).save()
        message.success(request,"Product Added Successfully")
        return HttpResponseRedirect('/show-cart/')

def show_cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        print(cart)
        return render(request,'cart.html',{'cart':cart})
    else:
        return render(request,'cart.html')


def shipping_view(request):
    if request.method=='POST':
        form=ShippingForm(request.POST)
        if form.is_valid():
                user=request.user
                fname = form.cleaned_data['fname']
                lname = form.cleaned_data['lname']
                pincode = form.cleaned_data['pincode']
                city = form.cleaned_data['city']
                locality = form.cleaned_data['locality']
                state = form.cleaned_data['state']
                contact = form.cleaned_data['contact']
                landmark =form.cleaned_data['landmark']
                user_save=ShippingDetail(user=user,fname=fname,lname=lname,contact=contact,pincode=pincode,locality=locality,city=city,state=state,landmark=landmark)
                user_save.save()
                messages.success(request, "Shipping Detail Added Successfully")
                return HttpResponseRedirect('/payment/')
    form = ShippingForm()
    return render(request, 'shipping.html',{'form':form})


def payment_view(request):
    return render(request, 'payment.html')