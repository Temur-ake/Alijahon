from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.db.models import Q, Count, F, Sum
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.timezone import now
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView

from apps.forms import CustomAuthenticationForm, CreateOrderForm, ChangePasswordModelForm, StreamCreateForm, \
    TransactionForm
from apps.models import Product, Category, User, Region, District, Order, Stream, Concurs, SiteDeliveryPrices, \
    Transaction

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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'apps/shop/product-detail.html'
    context_object_name = 'product'
    # success_url = reverse_lazy('order_list')

    # def form_valid(self, form):
    #     form.instance.owner = self.request.user
    #     if len(form.cleaned_data['phone']) != 12:
    #         raise ValidationError('number must be 12 in length')
    #     order = form.save()
    #     return redirect('order_detail', pk=order.pk)


class OrderCreateView(CreateView):
    model = Order
    form_class = CreateOrderForm

    # success_url = reverse_lazy('order_detail')

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        order = form.save()
        return redirect('order_detail', pk=order.pk)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'apps/order/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset().order_by('-created_at')
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
        name = self.request.GET.get('search')
        slug = self.request.GET.get('category')

        if slug:
            qs = qs.filter(category__slug=slug)

        if name:
            qs = qs.filter(Q(name__icontains=name) | Q(description__icontains=name))

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
        qs = qs.order_by('-created_at')
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

        now = timezone.now()

        if period == 'today':
            qs = qs.filter(orders__created_at__date=now.date())
        elif period == 'last_day':
            start_date = now - timedelta(days=1)
            qs = qs.filter(orders__created_at__range=(start_date, now))
        elif period == 'weekly':
            start_date = now - timedelta(weeks=1)
            qs = qs.filter(orders__created_at__range=(start_date, now))
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
            qs = qs.filter(orders__created_at__range=(start_date, now))

        qs = qs.annotate(
            yangi=Count('orders', Q(orders__status='yangi')),
            tayyor=Count('orders', Q(orders__status='tayyor')),
            yetkazilmoqda=Count('orders', Q(orders__status='yetkazilmoqda')),
            yetkazib_berildi=Count('orders', Q(orders__status='yetkazib_berildi')),
            telefon_kotarmadi=Count('orders', Q(orders__status='telefon_kotarmadi')),
            bekor_qilindi=Count('orders', Q(orders__status='bekor_qilindi')),
            arxivlandi=Count('orders', Q(orders__status='arxivlandi')),
        )

        # Aggregate totals
        aggregates = qs.aggregate(
            total_tashrif=Sum('tashrif'),
            total_yangi=Sum('yangi'),
            total_tayyor=Sum('tayyor'),
            total_yetkazilmoqda=Sum('yetkazilmoqda'),
            total_yetkazib_berildi=Sum('yetkazib_berildi'),
            total_telefon_kotarmadi=Sum('telefon_kotarmadi'),
            total_bekor_qilindi=Sum('bekor_qilindi'),
            total_arxivlandi=Sum('arxivlandi'),
        )

        # Attach aggregates to the queryset
        qs.aggregates = aggregates

        return qs


class RequestListView(ListView):
    model = Order
    template_name = "apps/admin_page/so'rovlar.html"
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(stream__owner=self.request.user,
                                             status=Order.Type.YETKAZIB_BERILDI).select_related('owner', 'product',
                                                                                                'stream', 'region')


class ConcursListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/admin_page/concurs.html'
    context_object_name = 'users'

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(stream__owner=self.request.user)
        active_concurs = Concurs.objects.filter(is_started=True).first()
        start_date = active_concurs.start_date
        end_date = active_concurs.end_date
        qs = qs.filter(orders__status='yetkazib_berildi', orders__stream__isnull=False,
                       orders__created_at__range=(start_date, end_date)).annotate(
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
        qs = qs.filter(owner=self.request.user).order_by('-created_at')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data()
        ctx['tolangan_sum'] = self.get_queryset().filter(status='paid').aggregate(Sum('amount'))['amount__sum'] or 0
        return ctx


class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'apps/admin_page/tolov.html'
    success_url = reverse_lazy('tolov_page')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        entered_amount = form.cleaned_data['amount']

        if entered_amount < 100000:
            form.add_error('amount', "Kiritilgan mablag' 100 000 mingdan kam bo'lmasligi kerak !")
            return self.form_invalid(form)

        if self.request.user.balance < entered_amount:
            form.add_error('amount', "Mablag' yetarli emas")
            return self.form_invalid(form)

        transaction = form.save(commit=False)

        self.request.user.balance -= entered_amount
        self.request.user.save()

        transaction.save()

        print(f"New Balance: {self.request.user.balance}")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = Transaction.objects.filter(owner=self.request.user)
        context['tolangan_sum'] = context['transactions'].filter(status='paid').aggregate(Sum('amount'))[
                                      'amount__sum'] or 0
        return context


class OperatorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.type == User.Type.OPERATOR


class OperatorListView(OperatorRequiredMixin, ListView):
    queryset = Order.objects.order_by('-created_at')
    template_name = 'apps/operators/operator-list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')

        if status:
            qs = qs.filter(status=status)

        if search:
            qs = qs.filter(
                Q(phone__icontains=search) |
                Q(product__name__icontains=search) |
                Q(full_name__icontains=search) |
                Q(stream__name__icontains=search)
            )
        return qs.select_related('product', 'courier')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['regions'] = Region.objects.all()
        ctx['districts'] = District.objects.all()
        ctx['products'] = Product.objects.all()
        ctx['streams'] = Stream.objects.all()
        ctx['couriers'] = User.objects.filter(type=User.Type.DRIVER)
        ctx['users'] = User.objects.all()
        return ctx


class OperatorCreateView(OperatorRequiredMixin, View):
    model = Order
    template_name = 'apps/operators/operator-list.html'
    success_url = reverse_lazy('operator_list')

    def get(self, request):
        # Render the form for creating a new order
        products = Product.objects.all()
        regions = Region.objects.all()
        streams = Stream.objects.all()
        users = User.objects.all()
        couriers = User.objects.filter(type=User.Type.DRIVER)

        return render(request, self.template_name, {
            'products': products,
            'regions': regions,
            'streams': streams,
            'users': users,
            'couriers': couriers,
        })

    def post(self, request):
        order = Order()
        order.product_id = request.POST.get('product')
        order.full_name = request.POST.get('full_name')
        order.phone = request.POST.get('phone')
        order.quantity = request.POST.get('quantity')
        order.region_id = request.POST.get('region')
        order.district_id = request.POST.get('district')
        order.stream_id = request.POST.get('stream')
        order.owner_id = request.POST.get('owner')
        order.courier_id = request.POST.get('courier')
        order.save()
        return redirect(self.success_url)


class OperatorDetailView(OperatorRequiredMixin, View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        products = Product.objects.all()
        regions = Region.objects.all()
        streams = Stream.objects.all()
        districts = District.objects.filter(region=order.region)
        users = User.objects.all()
        couriers = User.objects.filter(type=User.Type.DRIVER)

        status_choices = Order.Type.choices

        return render(request, 'apps/operators/operator-detail.html', {
            'order': order,
            'products': products,
            'regions': regions,
            'streams': streams,
            'districts': districts,
            'status_choices': status_choices,
            'users': users,
            'couriers': couriers,
        })

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.product_id = request.POST.get('product')
        order.full_name = request.POST.get('full_name')
        order.phone = request.POST.get('phone')
        order.quantity = request.POST.get('quantity')
        order.region_id = request.POST.get('region')
        order.district_id = request.POST.get('district')
        order.stream_id = request.POST.get('stream')
        order.status = request.POST.get('status')
        order.owner_id = request.POST.get('owner')
        order.courier_id = request.POST.get('courier')
        order.save()
        return redirect('operator_list')


class DeleteOrderView(OperatorRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.delete()
        return redirect('operator_list')
