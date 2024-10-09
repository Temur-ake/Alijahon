from django.urls import path

from apps.views import (
    ProductListView,
    ProductDetailView,
    AllProductListView,
    CustomLoginView,
    CustomLogoutView,
    ProfileView,
    ProfileUpdateView, DistrictListView, OrderDetailView, OrderListView, PasswordUpdateView, MarketView, StreamListview,
    StreamCreateView, StreamDetailView, StatisticProductDetailView, AdminPageTemplateView,
    RequestListView, ConcursTemplateView, StreamStatisticsListView,
    TransactionCreateView, TransactionListView, OperatorListView, OperatorDetailView
)

urlpatterns = [
    # Shop Urls
    path('', AllProductListView.as_view(), name='all_products'),
    path('category/', ProductListView.as_view(), name='all_category'),
    path('category/<slug:slug>/', ProductListView.as_view(), name='category_products'),
    path('product-detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('success-product/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('ordered-products/', OrderListView.as_view(), name='order_list'),

    # User Urls
    path('login/', CustomLoginView.as_view(), name='login_page'),
    path('logout/', CustomLogoutView.as_view(), name='logout_page'),
    path('profile/', ProfileView.as_view(), name='profile_page'),
    path('profile/settings/', ProfileUpdateView.as_view(fields=(
        'image', 'first_name', 'last_name', 'address', 'telegram_id', 'district', 'about')),
         name='profile_settings_page'),
    path('profile/update-password/', PasswordUpdateView.as_view(), name='update_password'),
    path('districts/', DistrictListView.as_view(), name='districts'),

    # Admin Page Urls
    path('admin_page/', AdminPageTemplateView.as_view(), name='admin_page'),
    path('admin_page/market/', MarketView.as_view(), name='market_page'),
    path('admin_page/market/category=<slug:slug>', MarketView.as_view(), name='market_category_page'),
    path('admin_page/urls/', StreamListview.as_view(), name='stream_list'),
    path('admin_page/product/<int:pk>', StatisticProductDetailView.as_view(), name='product_statistics'),
    path('admin_page/requests', RequestListView.as_view(), name='request_page'),
    path('admin_page/competition', ConcursTemplateView.as_view(), name='competition_page'),
    path('admin_page/withdraw/create', TransactionCreateView.as_view(), name='tolov_create_page'),
    path('admin_page/withdraw', TransactionListView.as_view(), name='tolov_page'),
    path('stream/create/', StreamCreateView.as_view(), name='stream_create'),
    path('stream/<int:pk>', StreamDetailView.as_view(), name='stream_detail'),
    path('stream/stats', StreamStatisticsListView.as_view(), name='stream_statistics'),
    path('operators', OperatorListView.as_view(), name='operators_list'),
    path('operators-detail', OperatorDetailView.as_view(), name='operators_detail')

]
