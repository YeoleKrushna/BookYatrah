from django import forms
from django.contrib.auth.models import User
from .models import Profile, Genre
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'required': True})
    )
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'required': True}),
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'required': True})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'required': True
        })
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
            'required': True
        })
    )

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    city = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    pincode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'required': True})
    )
    profile_pic = forms.ImageField(required=False)  # Optional

    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),  # Removed attrs={'required': True}
        required=True
    )

    class Meta:
        model = Profile
        fields = ['phone', 'city', 'pincode', 'profile_pic', 'preferred_genres']

    def clean_preferred_genres(self):
        data = self.cleaned_data.get('preferred_genres')
        if not data or data.count() == 0:
            raise forms.ValidationError("Please select at least one genre.")
        return data
    
from .models import Book

class BookUploadForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    preferred_genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    condition = forms.ChoiceField(
        choices=Book.CONDITION_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    image = forms.ImageField(required=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'language', 'genres', 'condition', 'description', 'image']

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 2 or len(title) > 255:
            raise forms.ValidationError("Title must be between 2 and 255 characters.")
        return title

    def clean_author(self):
        author = self.cleaned_data['author']
        if len(author) < 2 or len(author) > 255:
            raise forms.ValidationError("Author name must be between 2 and 255 characters.")
        return author

    def clean_language(self):
        language = self.cleaned_data['language']
        if len(language) < 2 or len(language) > 100:
            raise forms.ValidationError("Language must be between 2 and 100 characters.")
        return language
