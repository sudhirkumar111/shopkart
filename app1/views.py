from django.shortcuts import render
from .models import Product, Category,Cart, ShippingDetail,OrderPlaced,STATUS_CHOICES
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
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .serializers import CategorySerializer, ProductSerializer
from rest_framework import generics


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

@login_required()
def add_to_cart(request,id):
        user= request.user
        product = Product.objects.get(id=id)
        item_exist = False
        item_exist = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
        if item_exist == False:
            product = Product.objects.get(id=product.id)
            Cart(user=user,product=product).save()
            print(item_exist)
            return HttpResponseRedirect('/show-cart')
        else:
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

def product_detail(request,id):
    product = Product.objects.get(id=id)
    item_exist = False
    if request.user.is_authenticated:
        item_exist = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
    return render(request,'product_detail.html',{'product':product,'item_exist':item_exist})


        


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
        print(product.quantity)
        if product.quantity==0:
                product.delete()
                return HttpResponseRedirect('/show-cart/')
        product.save()
        return HttpResponseRedirect('/show-cart/')
        
def order_summary(request):
    if request.user.is_authenticated:
        order = Cart.objects.filter(user=request.user)
        total_amount = 0
        for item in order:
            total_amount+=item.product.price*item.quantity
            
        address = ShippingDetail.objects.filter(user=request.user)
        return render(request,'order_summary.html',{'total_amount':total_amount,'order':order,'address':address})
    else:
        return render(request,'order_summary.html')

def payment_view(request):
    if request.user.is_authenticated:
        add_id = request.GET.get('cust_add')
        user=request.user
        cartid = Cart.objects.filter(user = user)
        ship_detail = ShippingDetail.objects.get(id=add_id)
        for cid in cartid:
            OrderPlaced(user=user, ship_add=ship_detail, product=cid.product, quantity=cid.quantity).save()
            cid.delete()
        return HttpResponseRedirect('/orders/')
	      

def orders(request):
    if request.user.is_authenticated:
        order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
        return render(request,'order_placed.html',{'order_placed':order_placed})

def cancel_order(request,id):
    if request.user.is_authenticated:
        get_order = OrderPlaced.objects.get(id=id)
        print(get_order)
        get_order.status=STATUS_CHOICES[4][0]
        print(STATUS_CHOICES[4][0])
        get_order.save()
        return HttpResponseRedirect('/orders/')

def return_order(request,id):
    if request.user.is_authenticated:
        get_order = OrderPlaced.objects.get(id=id)
        print(get_order)
        get_order.status=STATUS_CHOICES[5][0]
        print(STATUS_CHOICES)
        print(STATUS_CHOICES[5][0])
        get_order.save()
        return HttpResponseRedirect('/orders/')


def buynow(request,id):
    if request.user.is_authenticated:
        user= request.user
        product= Product.objects.get(id=id)
        product2= Product.objects.get(id=product.id)
        Cart(user=user,product=product).save()            
        return HttpResponseRedirect('/order-summary')
    else:
            return HttpResponseRedirect('/login/')


def order_success(request):
    return render(request,'order_placed_successfully.html')

class ProductListCreate(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryListCreate(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer