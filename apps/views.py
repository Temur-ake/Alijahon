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
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from apps.forms import CustomAuthenticationForm, CreateOrderForm, ChangePasswordModelForm, StreamCreateForm
from apps.models import Product, Category, User, Region, District, Order, Stream, Concurs

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
        order = form.save()
        if len(form.cleaned_data['phone']) != 12:
            raise ValidationError('number must be 12 in length')
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
            qs = qs.filter(orders__created_at__exact=now().date())
        elif period == 'last_day':
            qs = qs.filter(orders__created_at__exact=now().date() - timedelta(1))
        elif period == 'weekly':
            qs = qs.filter(orders__created_at__gte=now() - timedelta(7))
        elif period == 'monthly':
            qs = qs.filter(orders__created_at__gte=now() - timedelta(30))

        qs = qs.annotate(
            yangi=Count('orders', Q(orders__status='yangi') & Q(orders__stream_id=F('id'))),
            tayyor=Count('orders', Q(orders__status='tayyor') & Q(orders__stream_id=F('id'))),
            yetkazilmoqda=Count('orders', Q(orders__status='yetkazilmoqda') & Q(orders__stream_id=F('id'))),
            yetkazib_berildi=Count('orders', Q(orders__status='yetkazib_berildi') & Q(orders__stream_id=F('id'))),
            telefon_kotarmadi=Count('orders', Q(orders__status='telefon_kotarmadi') & Q(orders__stream_id=F('id'))),
            bekor_qilindi=Count('orders', Q(orders__status='bekor_qilindi') & Q(orders__stream_id=F('id'))),
            arxivlandi=Count('orders', Q(orders__status='arxivlandi') & Q(orders__stream_id=F('id'))),
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


class RequestTemplateView(TemplateView):
    template_name = "apps/admin_page/so'rovlar.html"


class ConcursTemplateView(TemplateView):
    template_name = 'apps/admin_page/concurs.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['concurs'] = Concurs.objects.filter(is_started=True)
        ctx['users'] = User.objects.filter(orders__status='yetkazib_berildi').annotate(count=Count('orders')).values(
            'first_name', 'last_name', 'count').order_by('-count')
        return ctx


class TolovTemplateView(TemplateView):
    template_name = 'apps/admin_page/tolov.html'


class DiagramsView(View):
    print('Diagram ishladi')
    template_name = 'apps/admin_page/diagrams.html'

    def get(self, request):
        count_order = Order.objects.count()
        product_count = Product.objects.count()

        status_data_order = (
            Order.objects.values('status').annotate(count=Count('id'))
        )

        region_data = (
            Order.objects.values('region__name').annotate(count=Count('id'))
        )

        product_data = (
            Order.objects.values('product__name').annotate(count=Count('id'))
        )

        context = {
            'order_count': count_order,
            'product_count': product_count,
            'order_status_data': status_data_order,
            'region_data': region_data,
            'product_data': product_data

        }

        return render(request, 'apps/admin_page/diagrams.html', context)
