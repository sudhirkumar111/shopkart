from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm,SetPasswordForm
from .models import ShippingDetail

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name', 'last_name':'Last Name', 'email':'Email'}
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.EmailInput({'class':'form-control'}),
        }


class MyPasswordResetForm(PasswordResetForm):
 email = forms.EmailField(label=("Email"), max_length=254, widget=forms.EmailInput(attrs={'placeholder':'Enter Your Email','autocomplete': 'email', 'class':'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=("New Password"), strip=False, widget=forms.PasswordInput(attrs={'placeholder':'Username','autocomplete': 'new-password', 'class':'form-control'})),
    new_password2 = forms.CharField(label=("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'placeholder':'Password','autocomplete': 'new-password','class':'form-control'}))

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingDetail
        fields = ['fname','lname','contact','locality','city','pincode','state','landmark']
        labels={'fname':"First Name",'lname':"Last Name"}
        widgets = {
        'fname':forms.TextInput(attrs={'class':'form-control'}),
        'contact':forms.TextInput(attrs={'class':'form-control'}),
        'lname':forms.TextInput(attrs={'class':'form-control'}),
        'locality':forms.TextInput(attrs={'class':'form-control'}),
        'city':forms.TextInput(attrs={'class':'form-control'}), 
        'state':forms.Select(attrs={'class':'form-control'}),
        'pincode':forms.NumberInput(attrs={'class':'form-control'}),
        'landmark':forms.TextInput(attrs={'class':'form-control'})}