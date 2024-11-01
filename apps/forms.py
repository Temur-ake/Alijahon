import re

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.forms import CharField, PasswordInput, Form, ModelForm
from django.utils.translation import gettext_lazy as _

from apps.models import User, Order, Stream, Product, Transaction


class CustomAuthenticationForm(Form):
    phone = CharField()
    password = CharField(
        label=_("Password"),
        strip=False,
        widget=PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(phone)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        phone = self.data.get('phone')
        return re.sub(r'[^\d]', '', phone)

    def clean(self):
        phone = self.cleaned_data.get("phone")
        password = self.cleaned_data.get("password")

        if phone is not None and password:
            if not User.objects.filter(phone=phone).exists():
                self.user_cache = User.objects.create_user(phone=phone, password=password)
            else:
                self.user_cache = authenticate(
                    self.request, phone=phone, password=password
                )
            if self.user_cache is None:
                raise ValidationError(self.error_messages["inactive"],
                                      code="inactive")
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache


class ChangePasswordModelForm(ModelForm):
    new_password1 = CharField(max_length=255)
    new_password2 = CharField(max_length=255)

    class Meta:
        model = User
        fields = 'password', 'new_password1', 'new_password2'

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if not self.instance.check_password(password):
            raise ValidationError('Password xato')
        return password

    def clean(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 != new_password2:
            raise ValidationError('Password xato')

        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user


class CreateOrderForm(ModelForm):
    phone = CharField(max_length=18)

    class Meta:
        model = Order
        exclude = 'quantity', 'status', 'region', 'district','courier',

    def clean_phone(self):
        phone = self.data.get('phone')
        return re.sub(r'[^\d]', '', phone)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'about', 'address', 'telegram_id', 'district', 'image']


class StreamCreateForm(ModelForm):
    class Meta:
        model = Stream
        exclude = 'tashrif',

    def clean_discount(self):
        discount = int(self.data.get('discount'))
        pay_r = Product.objects.get(id=self.data['product']).payment_referral

        if discount > pay_r:
            raise ValidationError('chegirma ko`payib ketdi')
        return discount


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['card_number', 'amount', 'status']

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if len(card_number) != 16:
            raise ValidationError("Card number must be 16 digits long.")
        return card_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return amount
