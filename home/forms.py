from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UploadDocument, SubOrganisation

from home.models import Organisation, UserExtend


class UploadDocumentForm(forms.ModelForm):
    jurisdiction = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "text-field w-input",
                'placeholder': 'Jurisdiction',
            }
        )
    )
    type_of_doc = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': "text-field w-input",
                'placeholder': 'Type of Document',
            }
        )
    )
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'class': "text-field w-input"
            }
        )
    )
    class Meta:
        model = UploadDocument
        fields = [
            'jurisdiction',
            'type_of_doc',
            'file'
        ]


class PasswordResetform(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "text-field w-input"
            }
        ))

    class Meta:
        model = User
        fields = [
            'email',
        ]


class PasswordResetConfirm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "text-field w-input"
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm New Password",
                "class": "text-field w-input"
            }
        ))

    class Meta:
        model = User
        fields = [
            'new_password1',
            'new_password2',
        ]


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old Password",
                "class": "text-field w-input"
            }
        ))
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password",
                "class": "text-field w-input"
            }
        ))
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New Password again",
                "class": "text-field w-input"
            }
        ))

    class Meta:
        model = User
        fields = [
            'old_password',
            'new_password1',
            'new_password2',
        ]


class OrgDetailForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    address_1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address Line 1",
                "class": "text-field w-input"
            }
        ),
        required=False,
        label='Address Line 2'
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address Line 2",
                "class": "text-field w-input"
            }
        ),
        required=False,
        label='Address Line 2'
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "City",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "State",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "text-field w-input"
            }
        ),
        required=False
    )

    class Meta:
        model = Organisation
        exclude = ['name_of_mission', 'entity', 'read_notification']


class UserExtendForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    account_type = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Account Type",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    admin_access = forms.TypedChoiceField(
        choices=((False, 'No'), (True, 'Yes')),
        widget=forms.RadioSelect,
        required=False,
    )

    class Meta:
        model = UserExtend
        exclude = ['user', 'organisation']


class SubOrgDetailForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "text-field w-input"
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    address_1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address Line 1",
                "class": "text-field w-input"
            }
        ),
        required=False,
        label='Address Line 2'
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Address Line 2",
                "class": "text-field w-input"
            }
        ),
        required=False,
        label='Address Line 2'
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "City",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "State",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Phone",
                "class": "text-field w-input"
            }
        ),
        required=False
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "text-field w-input"
            }
        ),
        required=False
    )

    class Meta:
        model = SubOrganisation
        exclude = ['organisation', 'entity']
