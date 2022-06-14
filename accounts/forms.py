from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password',
    'class': 'form-control',

    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = Account
        fields  = ['first_name','last_name','mobile','email','password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Adress'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Enter Mobile Number'
        self.fields['mobile'].widget.attrs['placeholder'] = 'Enter Mobile Number'
      

        for field  in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
