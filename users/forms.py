from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django import forms
from users.models import OtpCode


class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=256, widget=forms.TextInput(
        attrs={'class': 'form-control w-100', 'placeholder': 'Phone or Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control w-100', 'placeholder': 'Password'}))

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        if "@" in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        else:
            data = {'username': username_or_email}
        try:
            get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                _('This {} does not exist'.format(list(data.keys())[0])))
        else:
            return username_or_email


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        print(self.fields)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "Phone", "class": "form-control"})
        self.fields['full_name'].widget = widgets.TextInput(
            attrs={'placeholder': "Full Name", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
        self.fields['address'].widget = widgets.TextInput(
            attrs={'placeholder': "Address", "class": "form-control"})
        self.fields['pincode'].widget = widgets.TextInput(
            attrs={'placeholder': "Pincode", "class": "form-control"})
        self.fields['password1'].widget = widgets.PasswordInput(
            attrs={'placeholder': "password", "class": "form-control"})
        self.fields['password2'].widget = widgets.PasswordInput(
            attrs={'placeholder': "repeat password", "class": "form-control"})

    def clean_email(self):
        username = self.cleaned_data['username']
        if not isinstance(username, int) or len(username) != 10:
            raise ValidationError("Note a valid Phone number")
        return email

    def clean_username(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError("This email address is already exists.")
        return email

    class Meta:
        model = get_user_model()
        fields = ("full_name", "username", "email", "address" , "pincode")


class UpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = widgets.TextInput(
            attrs={'placeholder': "username", "class": "form-control"})
        self.fields['email'].widget = widgets.EmailInput(
            attrs={'placeholder': "email", "class": "form-control"})
        self.fields['address'].widget = widgets.TextInput(
            attrs={'placeholder': "Address", "class": "form-control"})
        self.fields['pincode'].widget = widgets.TextInput(
            attrs={'placeholder': "Pincode", "class": "form-control"})
        self.fields['full_name'].widget = widgets.TextInput(
            attrs={'placeholder': "Full Name", "class": "form-control"})

    class Meta:
        model = get_user_model()
        fields = ("full_name", "username", "email", "address" , "pincode")


class ForgetPasswordEmailCodeForm(forms.Form):
    username_or_email = forms.CharField(max_length=256,
                                        widget=forms.TextInput(
                                            attrs={'class': 'form-control',
                                                   'placeholder': 'Type your username or email'}
                                        )
                                        )

    def clean_username_or_email(self):
        username_or_email = self.cleaned_data['username_or_email']
        data = {'username': username_or_email}

        if '@' in username_or_email:
            validate_email(username_or_email)
            data = {'email': username_or_email}
        try:
            get_user_model().objects.get(**data)
        except get_user_model().DoesNotExist:
            raise ValidationError(
                'There is no account with this {}'.format(list(data.keys())[0]))

        if not get_user_model().objects.get(**data).is_active:
            raise ValidationError(_('This account is not active.'))

        return data


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password'
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
            }
        ),
    )

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Passwords are not match'))
        password_validation.validate_password(password2)
        return password2


class OtpForm(forms.Form):
    otp = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter code',
            }
        )
    )

    def clean_otp(self):
        otp_code = self.cleaned_data['otp']
        try:
            OtpCode.objects.get(code=otp_code)
        except OtpCode.DoesNotExist:
            raise ValidationError(
                _('You have entered incorrect code!')
            )
        else:
            return otp_code
