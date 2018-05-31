'''

@author: hectorz
'''
from django import forms  
from django.contrib.auth.models import User  
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput  
  
class LoginForm(forms.Form):  
    username = forms.CharField(  
        required=True,  
        label=u"UserName",  
        error_messages={'required': 'Please input your UserName'},  
        widget=forms.TextInput(  
            attrs={  
                'placeholder':u"UserName",  
            }  
        ),  
    )      
    password = forms.CharField(  
        required=True,  
        label=u"Password",  
        error_messages={'required': u'Please input your password'},  
        widget=forms.PasswordInput(  
            attrs={  
                'placeholder':u"Password",  
            }  
        ),  
    )     
    def clean(self):  
        if not self.is_valid():  
            raise forms.ValidationError(u"UserName and Password are Mandatory.")  
        else:  
            cleaned_data = super(LoginForm, self).clean()
