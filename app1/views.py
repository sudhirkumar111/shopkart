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
from django.views.generic.detail import DetailView

# Create your views here.
def home(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
         cart=Cart.objects.filter(user=request.user)
         
    else:
        cart=None

    categoryid = request.GET.get('category')
    if categoryid:
        products=Product.objects.filter(category=categoryid)
    else:
        products = Product.objects.all()


    return render(request,'home.html',{'products':products,'cart':cart,'categories':categories})


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

def add_to_cart(request,id):
        user= request.user
        product = Product.objects.get(id=id)
        Cart(product=product,user=user).save()
        messages.success(request,"Product Added Successfully")
        return HttpResponseRedirect('/show-cart/')

def show_cart(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        total_amount = 0
        for item in cart:
            total_amount+=item.product.price*item.quantity
            
        
        return render(request,'cart.html',{'cart':cart,'total_amount':total_amount})
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

def address_view(request):
    if request.user.is_authenticated:
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
                return HttpResponseRedirect('/address/')
    
        else:
            form = ShippingForm()
            address = ShippingDetail.objects.filter(user=request.user)
            return render(request, 'show_address.html',{'address':address,'form':form})
    


def delet_address(request,id):
    if request.user.is_authenticated:
        add = ShippingDetail.objects.filter(user=request.user).get(id=id)
        print(add.city)
        add.delete()
        messages.error(request, "Address Deleted Successfully")
        return HttpResponseRedirect('/address/')

def delete_cart_product(request,id):
    if request.user.is_authenticated:
        product = Cart.objects.filter(user=request.user).get(id=id)
       
        product.delete()
        # messages.error(request, "Address Deleted Successfully")
        return HttpResponseRedirect('/show-cart/')
 

def user_profile(request,id):
    user = User.objects.get(id=id)
    return render(request,'profile.html',{'user':user})

class product_detail(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'


def payment_view(request):
    return render(request, 'payment.html')

def plus_quantity(request,id):
    if request.user.is_authenticated:
        product = Cart.objects.filter(user=request.user).get(id=id)
        plus = 1
        plus+=product.quantity
        print(plus) 
        product.quantity=plus
        product.save()
        return HttpResponseRedirect('/show-cart/')

def minus_quantity(request,id):
    if request.user.is_authenticated:
        product = Cart.objects.filter(user=request.user).get(id=id)
        minus = 1
        minus=product.quantity - minus
        product.quantity=minus
        if product.quantity==0:
                product.delete()
        product.save()
        return HttpResponseRedirect('/show-cart/')
        