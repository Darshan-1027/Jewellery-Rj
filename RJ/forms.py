from django import forms

class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'})
    )
    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your state'})
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your city'})
    )
    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your pincode'})
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter your full address'})
    )


