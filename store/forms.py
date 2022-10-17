from django import forms
from .models import Customer

class UserInfo(forms.ModelForm):
    #photo = forms.ImageField(label='Image',widget=forms.ClearableFileInput(attrs={'class': 'fileinput'}), required=False)
    
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.TextInput(attrs={'class': 'input'}),
        }

