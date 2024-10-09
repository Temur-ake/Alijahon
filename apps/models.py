from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, TextField, ImageField, ForeignKey, CASCADE, Model, SlugField, \
    PositiveSmallIntegerField, DateTimeField, SET_NULL, PositiveIntegerField, DateField, BooleanField, FileField
from django.utils.text import slugify

from managers import CustomUserManager

# ==================================================================================================================================================
'''Base Model'''


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True, verbose_name="Yaratilgan Vaqti")
    updated_at = DateTimeField(auto_now=True, verbose_name="Yangilangan Vaqti")

    class Meta:
        abstract = True


class SlugBaseModel(Model):
    name = CharField(max_length=255, verbose_name="Nomi")
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


# ==================================================================================================================================================
'''User Model'''


class User(AbstractUser):
    class Type(TextChoices):
        OPERATOR = 'operator', 'Operator'
        MANAGER = 'manager', 'Manager'
        ADMIN = 'admin_side', 'Admin_side'
        DRIVER = 'currier', "Currier"
        USER = 'user', 'User'

    email = None
    username = None
    phone = CharField(max_length=12, unique=True, verbose_name="User Telefon Raqami")
    about = TextField(null=True, blank=True, verbose_name="User Haqida")
    address = CharField(max_length=255, null=True, blank=True, verbose_name="User Manzili")
    telegram_id = CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="User Telegram Id si")
    image = ImageField(upload_to='users/', null=True, blank=True, verbose_name="User Rasmi")
    district = ForeignKey('apps.District', CASCADE, null=True, blank=True, verbose_name="User Tumani")
    type = CharField(max_length=25, choices=Type.choices, default=Type.USER, verbose_name="Userning turi")
    balance = PositiveIntegerField(db_default=0, verbose_name="Userning balansi")

    objects = CustomUserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class Region(Model):
    name = CharField(max_length=255, verbose_name="Viloyat Nomi")

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255, verbose_name="Tuman Nomi")
    region = ForeignKey('apps.Region', CASCADE)

    def __str__(self):
        return self.name


class SiteDeliveryPrices(Model):
    price_for_all_regions = PositiveIntegerField(db_default=0,
                                                 verbose_name="Barcha Viloyatlar Uchun Yetkazib Berish Narxi")
    price_for_tashkent_region = PositiveIntegerField(db_default=0,
                                                     verbose_name="Toshkent Viloyati Uchun Yetkazib Berish Narxi")
    price_for_inside_of_tashkent = PositiveIntegerField(db_default=0,
                                                        verbose_name="Toshkent Shahar Ichiga Yetkazish Narxi")


# ==================================================================================================================================================
'''Shop Model'''


class Category(SlugBaseModel):
    image = ImageField(upload_to='categories/%Y/%m/%d', verbose_name="Kategoriya rasmi")

    def __str__(self):
        return self.name


class Product(SlugBaseModel, BaseModel):
    image = ImageField(upload_to='products/%Y/%m/%d', verbose_name="Mahsulot Rasmi")
    description = CharField(max_length=255, verbose_name="Mahsulot haqida")
    price = PositiveSmallIntegerField(verbose_name="Mahsulot narxi")
    quantity = PositiveSmallIntegerField(verbose_name="Mahsulot Soni")
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products',
                          verbose_name="Mahsulot Kategoriyasi")
    payment_referral = PositiveIntegerField(help_text="so'mda", default=0,
                                            null=True,
                                            blank=True, verbose_name="Oqim egasiga beriladigan pul")
    discount_market = TextField(null=True, blank=True, verbose_name="Market Page Uchun Chegrima")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Stream(BaseModel):
    name = CharField(max_length=255, verbose_name="Oqim Nomi (link ko'rinishida) ")
    discount = PositiveSmallIntegerField(db_default=0, verbose_name="Oqim Chegirmasi")
    product = ForeignKey(Product, CASCADE, related_name='streams', verbose_name="Oqimning Mahsuloti")
    owner = ForeignKey(User, CASCADE, verbose_name="Oqimnning Egasi")
    tashrif = PositiveSmallIntegerField(default=0, verbose_name="Oqimning Tashriflar Soni")

    def __str__(self):
        return self.name


class Order(BaseModel):
    class Type(TextChoices):
        YANGI = 'yangi', 'YANGI'
        TAYYOR = 'Dastavkaga tayyor', 'DASTAVKAGA TAYYOR'
        YETKAZILMOQDA = 'yetkazilmoqda', 'YETKAZILMOQDA'
        YETKAZIB_BERILDI = 'yetkazib_berildi', 'YETKAZIB_BERILDI'
        TELEFON_KOTARMADI = "telefon_kotarmadi", "TELEFON_KOTARMADI"
        BEKOR_QILINDI = 'bekor_qilindi', 'BEKOR_QILINDI'
        ARXIVLANDI = 'arxivlandi', 'ARXIVLANDI'

    quantity = PositiveSmallIntegerField(db_default=1, verbose_name="Buyurtma soni")
    product = ForeignKey(Product, CASCADE, verbose_name="Buyurtma mahsuloti")
    owner = ForeignKey(User, SET_NULL, related_name='orders', null=True, blank=True, verbose_name="Mahsulot Beruvchi")
    phone = CharField(max_length=12, verbose_name="Buyurtma qilganing raqami")
    full_name = CharField(max_length=255, verbose_name="Buyurtmani Qabul qiluvchi")
    status = CharField(max_length=255, choices=Type.choices, default=Type.YANGI, verbose_name="Buyurtma holati")
    region = ForeignKey(Region, CASCADE, null=True, blank=True, verbose_name="Buyurtma boradigan shahar")
    district = ForeignKey(District, CASCADE, null=True, blank=True, verbose_name="Buyurtma boradigan tuman")
    stream = ForeignKey(Stream, SET_NULL, null=True, blank=True, related_name='orders',
                        verbose_name="Buyurtmaning oqimi")

    @property
    def price(self):
        if self.stream:
            order_price = self.product.price - self.stream.discount
        else:
            order_price = self.product.price
        return order_price

    def __str__(self):
        return self.full_name


class Concurs(BaseModel):
    name = CharField(max_length=255, verbose_name="Musobaqa Nomi")
    about = TextField(verbose_name="Musobaqa haqida")
    image = ImageField(upload_to='images/%Y/%m/%d', verbose_name="Musobaqa Rasmi")
    start_date = DateField(null=True, blank=True, verbose_name="Musobaqa Boshlanish Vaqti")
    end_date = DateField(null=True, blank=True, verbose_name="Musobaqa Tugash Vaqti")
    is_started = BooleanField(default=False, verbose_name="Musobaqa holati")

    def __str__(self):
        return self.name


class Transaction(BaseModel):
    class TYPES(TextChoices):
        PENDING = 'pending', 'PENDING'
        CANCELED = 'canceled', 'CANCELED'
        PAID = 'paid', 'PAID'
        ERROR = 'error', 'ERROR'

    owner = ForeignKey(User, CASCADE, verbose_name="Mablag'gning egasi")
    amount = PositiveIntegerField(db_default=0, verbose_name="Userning beriladigan pul miqdori")
    card_number = CharField(max_length=16, verbose_name="Userning Karta Raqami")
    message = TextField(null=True, blank=True, verbose_name="Tolov xabari")
    image = ImageField(upload_to='transactons/%Y/%m/%d', null=True, blank=True, verbose_name="Tolov rasmi")
    status = CharField(max_length=10, choices=TYPES.choices, default=TYPES.PENDING, verbose_name="Tolov Statusi")

    def __str__(self):
        return self.owner.type
