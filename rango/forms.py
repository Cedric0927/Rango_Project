"""
@Author: Cedric
@Time: 2021.03,10
"""
from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Page, Userprofile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="please input category name")
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    slug = forms.CharField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="please enter the title")
    url = forms.URLField(max_length=200, help_text="please enter the url")
    views = forms.IntegerField(widget=forms.HiddenInput, initial=0)

    # category = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data

        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
            return cleaned_data


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"id": "user_name",
                                                             'class': 'form-control',
                                                             'placeholder': "Name Input",
                                                             'label': 'Name label'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "id": "user_mail",
        "class": "form-control",
        "placeholder": 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "user_password",
        "class": "form-control",
        "placeholder": 'Password'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ('website', 'picture')


class BootUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password')
