from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q, Count, F, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from apps.forms import CustomAuthenticationForm, CreateOrderForm, ChangePasswordModelForm, StreamCreateForm, \
    TransactionForm, CurrierProfileForm
from apps.models import Product, Category, User, Region, District, Order, Stream, Concurs, SiteDeliveryPrices, \
    Transaction, CurrierProfile

# ==================================================================================================================================================
'''User View'''


class CustomLoginView(LoginView):
    template_name = 'apps/auth/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        u = form.get_user()
        login(self.request, u)
        return redirect('all_products')


class CustomLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('all_products'))


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'apps/auth/profile.html'
    context_object_name = 'user'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(UpdateView):
    model = User
    template_name = 'apps/auth/profile_setting.html'
    success_url = reverse_lazy('all_products')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        context['districts'] = District.objects.all()
        return context


class PasswordUpdateView(UpdateView):
    form_class = ChangePasswordModelForm
    template_name = 'apps/auth/profile_setting.html'
    success_url = reverse_lazy('all_products')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DistrictListView(View):
    def get(self, request, *args, **kwargs):
        region_id = request.GET.get('region_id')
        if region_id:
            districts = District.objects.filter(region_id=region_id).values('id', 'name')
            return JsonResponse(list(districts), safe=False)
        return JsonResponse([], safe=False)


# ==================================================================================================================================================
'''Shop View'''


class AllProductListView(ListView):
    template_name = 'apps/shop/all_products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        ctx = Product.objects.all()
        slug = self.kwargs.get('slug')
        name = self.request.GET.get('name')

        if name:
            ctx = ctx.filter(Q(name__icontains=name) | Q(description__icontains=name))
        if slug:
            ctx = ctx.filter(category__slug=slug)
        return ctx

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    template_name = 'apps/shop/product-list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        ctx = Product.objects.all()

        slug = self.kwargs.get('slug')

        if slug:
            ctx = ctx.filter(category__slug=slug)

        return ctx

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView, CreateView):
    model = Product
    form_class = CreateOrderForm
    template_name = 'apps/shop/product-detail.html'
    context_object_name = 'product'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        if len(form.cleaned_data['phone']) != 12:
            raise ValidationError('number must be 12 in length')
        order = form.save()
        return redirect('order_detail', pk=order.pk)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'apps/order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset().filter(phone=self.request.user.phone)
        return qs


class OrderDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/order/success.html'

    # context_object_name = 'order'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['yetkazish'] = SiteDeliveryPrices.objects.first()
        return ctx

    # ==================================================================================================================================================


'''Admin Page View'''


class AdminPageTemplateView(TemplateView):
    template_name = 'apps/admin_page/admin_page.html'


class MarketView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/admin_page/market.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.GET.get('name')
        slug = self.kwargs.get('slug')
        top = self.request.GET.get('category')

        if top:
            qs = Product.objects.filter(order__status=Order.Type.YETKAZIB_BERILDI).annotate(
                count=Count('order')).order_by('-count')

        if slug:
            qs = qs.filter(category__slug=slug)

        if name:
            qs = Product.objects.filter(Q(name__icontains=name) | Q(description__icontains=name))
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Category.objects.all()
        return ctx


class StreamCreateView(CreateView):
    template_name = 'apps/admin_page/market.html'
    form_class = StreamCreateForm
    success_url = reverse_lazy('stream_list')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        text = 'Chegirma summasi oshib ketdi!'
        messages.add_message(self.request, messages.WARNING, text)
        return redirect('market_page')


class StreamListview(ListView):
    model = Stream
    template_name = 'apps/admin_page/stream-list.html'
    context_object_name = 'streams'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner=self.request.user)
        return qs


class StreamDetailView(DetailView, CreateView):
    model = Stream
    template_name = 'apps/shop/product-detail.html'
    form_class = CreateOrderForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        ctx['product'] = Product.objects.filter(pk=kwargs['object'].product.id).first()
        ctx['stream'].tashrif += 1
        ctx['stream'].save()

        return ctx

    def form_valid(self, form):
        order = form.save()
        if len(form.cleaned_data['phone']) != 9:
            raise ValidationError('number must be 12 in length')
        return redirect('order_detail', pk=order.pk)


class StatisticProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/admin_page/product_statics.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        product = self.get_object()
        ctx = super().get_context_data(**kwargs)
        ctx['streams_count'] = product.streams.count()
        ctx['your_streams'] = product.streams.filter(owner=self.request.user).count()

        return ctx


class StreamStatisticsListView(ListView):
    model = Stream
    template_name = 'apps/admin_page/stream_statics.html'
    context_object_name = 'streams'

    def get_queryset(self):
        qs = super().get_queryset().filter(owner=self.request.user)
        period = self.request.GET.get('period')

        if period == 'today':
            qs = qs.filter(orders__created_at__date=timezone.now().date())

        elif period == 'last_day':
            start_date = timezone.now() - timedelta(days=1)
            end_date = timezone.now()
            qs = qs.filter(orders__created_at__range=(start_date, end_date))

        elif period == 'weekly':
            start_date = timezone.now() - timedelta(days=7)
            end_date = timezone.now()
            qs = qs.filter(orders__created_at__range=(start_date, end_date))

        elif period == 'monthly':
            start_date = timezone.now() - timedelta(days=30)
            end_date = timezone.now()
            qs = qs.filter(orders__created_at__range=(start_date, end_date))

        qs = qs.annotate(
            yangi=Count('orders', Q(orders__status='yangi')),
            tayyor=Count('orders', Q(orders__status='tayyor')),
            yetkazilmoqda=Count('orders', Q(orders__status='yetkazilmoqda')),
            yetkazib_berildi=Count('orders', Q(orders__status='yetkazib_berildi')),
            telefon_kotarmadi=Count('orders', Q(orders__status='telefon_kotarmadi')),
            bekor_qilindi=Count('orders', Q(orders__status='bekor_qilindi')),
            arxivlandi=Count('orders', Q(orders__status='arxivlandi')),
        )
        qs.aggregates = qs.aggregate(
            total_tashrif=Sum('tashrif'),
            total_yangi=Sum('yangi'),
            total_tayyor=Sum('tayyor'),
            total_yetkazilmoqda=Sum('yetkazilmoqda'),
            total_yetkazib_berildi=Sum('yetkazib_berildi'),
            total_telefon_kotarmadi=Sum('telefon_kotarmadi'),
            total_bekor_qilindi=Sum('bekor_qilindi'),
            total_arxivlandi=Sum('arxivlandi')

        )

        return qs


class RequestListView(ListView):
    model = Order
    template_name = "apps/admin_page/so'rovlar.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(stream__isnull=False, owner=self.request.user)


class ConcursTemplateView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/admin_page/concurs.html'
    context_object_name = 'users'

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(stream__owner=self.request.user)
        qs = qs.filter(orders__status='yetkazib_berildi', orders__stream__isnull=False).annotate(
            count=Sum('orders__quantity')).values(
            'first_name', 'last_name', 'count').order_by('-count')
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['concurs'] = Concurs.objects.filter(is_started=True)

        return ctx


# views.py
class TransactionListView(ListView):
    queryset = Transaction.objects.all()
    template_name = 'apps/admin_page/tolov.html'
    context_object_name = 'transactions'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(owner_id=self.request.user)
        return qs


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'apps/admin_page/tolov.html'
    success_url = reverse_lazy('tolov_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        entered_amount = form.cleaned_data['amount']

        if self.request.user.balance < entered_amount:
            form.add_error('amount', "Buncha mablag' mavjud emas.")
            return self.form_invalid(form)

        # Save the transaction
        transaction = form.save(commit=False)

        transaction_status = form.cleaned_data['status']
        if transaction_status == 'PAID':
            self.request.user.balance -= entered_amount
            self.request.user.save()

        transaction.save()

        print(f"New Balance: {self.request.user.balance}")

        return super().form_valid(form)


class OperatorListView(ListView):
    model = User
    template_name = 'apps/operators/operator-list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')

        # if status == 'new':


class OperatorDeliveredView(TemplateView):
    template_name = 'apps/operators/operator-detail.html'


class CurrierListView(ListView):
    model = CurrierProfile
    template_name = 'apps/operators/currier-list.html'
    context_object_name = 'curriers'


class CurrierDetailView(DetailView):
    model = CurrierProfile
    template_name = 'apps/operators/currier-detail.html'
    context_object_name = 'currier'
