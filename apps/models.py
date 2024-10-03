from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, TextField, ImageField, ForeignKey, CASCADE, Model, SlugField, \
    PositiveSmallIntegerField, DateTimeField, SET_NULL, PositiveIntegerField
from django.utils.text import slugify

from managers import CustomUserManager


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        original_slug = self.slug
        count = 1
        while self.__class__.objects.filter(slug=self.slug).exists():
            self.slug = f"{original_slug}-{count}"
            count += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(SlugBaseModel):
    image = ImageField(upload_to='categories/%Y/%m/%d')


class Product(SlugBaseModel, BaseModel):
    image = ImageField(upload_to='products/%Y/%m/%d')
    description = CharField(max_length=255)
    price = PositiveSmallIntegerField()
    quantity = PositiveSmallIntegerField()
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')
    payment_referral = PositiveIntegerField(verbose_name="Chegirma", help_text="so'mda", default=0,
                                            null=True,
                                            blank=True)

    class Meta:
        ordering = ['-created_at']


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin_side', 'Admin_side'
        DRIVER = 'currier', "Currier"
        USER = 'user', 'User'

    email = None
    username = None
    phone = CharField(max_length=12, unique=True)
    about = TextField(null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    telegram_id = CharField(max_length=255, unique=True, null=True, blank=True)
    image = ImageField(upload_to='users/', null=True, blank=True)
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True)
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []


class Region(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', CASCADE)

    def __str__(self):
        return self.name


class Stream(BaseModel):
    discount = PositiveSmallIntegerField()
    name = CharField(max_length=255)
    product = ForeignKey(Product, CASCADE, related_name='streams')
    owner = ForeignKey(User, CASCADE)
    tashrif = PositiveSmallIntegerField(default=0)


class Order(BaseModel):
    class Type(TextChoices):
        YANGI = 'yangi', 'YANGI'
        TAYYOR = 'Dastavaga tayyor', 'DASTAVKAGA TAYYOR'
        YETKAZILMOQDA = 'yetkazilmoqda', 'YETKAZILMOQDA'
        YETKAZIB_BERILDI = 'yetkazib_berildi', 'YETKAZIB_BERILDI'
        TELEFON_KOTARMADI = 'telefon_kotarmadi', 'TELEFON_KOTARMADI'
        BEKOR_QILINDI = 'bekor_qilindi', 'BEKOR_QILINDI'
        ARXIVLANDI = 'arxivlandi', 'ARXIVLANDI'

    quantity = PositiveSmallIntegerField(db_default=1)
    product = ForeignKey(Product, CASCADE)
    owner = ForeignKey(User, SET_NULL, related_name='owner', null=True, blank=True)
    phone = CharField(max_length=12)
    full_name = CharField(max_length=255)
    status = CharField(max_length=255, choices=Type.choices, default=Type.YANGI)
    region = ForeignKey(Region, CASCADE, null=True, blank=True)
    district = ForeignKey(District, CASCADE, null=True, blank=True)
    stream = ForeignKey(Stream, SET_NULL, null=True, blank=True, related_name='orders')

    @property
    def price(self):
        if self.stream:
            order_price = self.product.price - self.stream.discount
        else:
            order_price = self.product.price
        return order_price
