"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app1 import views
from app1.forms import MyPasswordResetForm, MySetPasswordForm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('about/',views.about, name='about'),
    path('signup/',views.user_signup, name='signup'),
    path('login/',views.user_login, name='login'),
    path('logout/',views.user_logout, name='logout'),

    # form to enter email
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),

    # display message
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name="password_reset_done"),

    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),

    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name="password_reset_complete"),

    path('add-to-cart/<id>/', views.add_to_cart, name='add-to-cart'),
    path('show-cart/', views.show_cart, name='show-cart'),
    path('shipping-address/', views.shipping_view, name='shipping-detail'),
    path('payment/', views.payment_view,name='payment'),
    path('address/', views.address_view,name='address'),
    path('delete/<id>/', views.delet_address,name='delete'),
    path('delete-cart-product/<id>/', views.delete_cart_product,name='delete_cart_product'),
    path('profile/<id>/', views.user_profile,name='profile'),
    path('product-detail/<id>/', views.product_detail,name='product-detail'),
    path('plus_quantity/<id>/', views.plus_quantity,name='plus_quantity'),
    path('minus_quantity/<id>/', views.minus_quantity,name='minus_quantity'),
    path('order-summary/', views.order_summary,name='order_summary'),
    path('orders/', views.orders,name='orders'),
    path('cancel/<id>/', views.cancel_order,name='cancel'),
    path('return-order/<id>/', views.return_order,name='return-order'),
    path('buy/<id>/', views.buynow,name='buy'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
