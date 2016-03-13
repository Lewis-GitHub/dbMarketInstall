from django import forms

__all__ = ['LoginForm', 'LockoutForm']


class LoginForm(forms.Form):

    username = forms.CharField(label='username', max_length=30,
                               widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Username'}))

    password = forms.CharField(label='password', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password'}))


class LockoutForm(forms.Form):

    username = forms.CharField(label='username', max_length=30,
                               widget=forms.TextInput(attrs={'class': "form-control"}))

    password = forms.CharField(label='password', max_length=256,
                               widget=forms.PasswordInput(attrs={'class': "form-control"}))

