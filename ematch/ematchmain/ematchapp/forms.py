from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Qualities, Payment

CHECK_CHOICE = (
    ('True', 'True'),
    ('False', 'False')
)


class CreateUserForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Enter Your Username',
        'class': 'my-form-control',
        'id': 'Username',
        'onfocus': 'pass_collapse()'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Your Email',
        'class': 'my-form-control',
        'id': 'Email Address',
        'onfocus': 'pass_collapse()'
    }))

    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password',
        'class': 'my-form-control',
        'id': 'Password1',
        'onfocus': 'pass_detail()'
    }))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Your Password',
        'class': 'my-form-control',
        'id': 'Password2',
        'onfocus': 'pass_detail1()'
    }))
    checkbox = forms.ChoiceField(required=True, widget=forms.CheckboxInput({'class': 'agree-term', 'id': 'checkbox', 'onfocus': 'pass_collapse()'}), choices=CHECK_CHOICE)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


GENDER_CHOICE = (
    ('M', 'Male'),
    ('F', 'Female')
)


class ProfileForm(forms.ModelForm):
    Profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('Date_of_Birth',)


class QualityForm(forms.ModelForm):
    class Meta:
        model = Qualities
        fields = '__all__'


class PaymentForm(forms.ModelForm):

    Email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control',
        'id': 'email',
        'name': 'email'
    }))
    class Meta:
        model = Payment
        fields = '__all__'