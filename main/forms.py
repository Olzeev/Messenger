from django import forms
from .models import *

class SignInForm(forms.Form):
    class Meta:
        fields = ["email", "password"]

        
        widgets = {
            "email": forms.TextInput(attrs={
                "class": "sign_in_input", 
                "placeholder": "Эл. почта", 
                "type": "email", 
                "maxlength": "30"
            }), 
            "password": forms.TextInput(attrs={
                "class": "sign_in_input",
                "placeholder": "Пароль",
                "type": "password",
                "maxlength": "30",
                "size": "30"
            })
        }


class SignUpForm(forms.Form):
    class Meta:
        fields = ["email", "password", "password_check"]

        widgets = {
            "email": forms.TextInput(attrs={
                "class": "sign_in_input", 
                "placeholder": "Эл. почта", 
                "type": "email", 
                "maxlength": "30"
            }), 
            "password": forms.TextInput(attrs={
                "class": "sign_in_input",
                "placeholder": "Пароль",
                "type": "password",
                "maxlength": "30"
            }), 
            "password_check": forms.TextInput(attrs={
                "class": "sign_in_input",
                "placeholder": "Пароль",
                "type": "password",
                "maxlength": "30"
            })
        }
        
        
class EditInfoForm(forms.Form):
    class Meta:
        fields = ["username", "avatar", "status"]
