"""dstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from carts.views.addtocart import AddToCart
from carts.views.cartitemsshow import CartItemsShow
from carts.views.removefromcart import RemoveFromCart
from orders.views.createinvoice import InvoiceCreate
from orders.views.manageselectedpayment import ManageSelectedPaymentView
from orders.views.order import AddShippingToOrderView, CreateOrderView, ShowOrderView
from orders.views.payment import  CallbackPaymentView, ProcessPaymentView
from orders.views.paymentgateway import CreatePaymentGatewayView, PaymentGatewayListView, UpdatePaymentGatewayView
from orders.views.paymentmethod import CreatePaymentMethodView, PaymentMethodListView, UpdatePaymentMethodView
from orders.views.shippingmethod import CreateShippingMethodView, ShippingMethodListView, UpdateShippingMethodView
from products.views import CategoriesListView, CategoryCreateView, CategoryDeleteView, CategoryShowView, CategoryUpdateView, ProductAddView, ProductCreateView, ProductDeleteView, ProductDislikeView, ProductLikeView, ProductReviewView, ProductShowView,ProductUpdateView, ProductsListView
from users.views.addresslist import UserAddressListView
from users.views.mycoupons import MyCouponsView
from users.views.myscores import MyScoresView
from users.views.mywallet import MyWalletView
from users.views.myorders import MyOrdersView
from users.views.useraddupdateaddress import UserAddAddressView,UserUpdateAddressView
from users.views.usercreate import UserCreateView
from users.views.userdelete import UserDeleteView
from users.views.userlogin import UserLoginView
from users.views.userlogout import UserLogoutView
from users.views.userprofile import UserProfileView
from users.views.userlist import UserListView
from users.views.usershow import UserShowView
from users.views.userupdate import UserUpdateView


urlpatterns = [
    path('admin/', admin.site.urls),

    ####################     USER  API    ##################
    # Routes without middleware
    path('api/user/create', UserCreateView.as_view(), name='create_user'),
    path('api/user/login', UserLoginView.as_view(), name='login_user'),

    # Routes with middleware (authentication required)
    path('api/user/profile', UserProfileView.as_view(), name='profile_user'),
    path('api/user/logout', UserLogoutView.as_view(), name='logout_user'),
    path('api/user/users', UserListView.as_view(), name='list_users'),
    path('api/user/show/<int:id>', UserShowView.as_view(), name='show_user'),
    path('api/user/update/<int:id>', UserUpdateView.as_view(), name='update_user'),
    path('api/user/delete/<int:id>', UserDeleteView.as_view(), name='delete_user'),
    ####address
    path('api/user/add/address', UserAddAddressView.as_view(), name='add_address_user'),
    path('api/user/edit/address/<int:id>', UserUpdateAddressView.as_view(), name='update_address_user'),
    path('api/user/addresses', UserAddressListView.as_view(), name='list_address_user'),

    #########
    path('api/user/my/scores', MyScoresView.as_view(), name='scores_user'),
    path('api/user/my/coupons', MyCouponsView.as_view(), name='coupons_user'),
    path('api/user/my/orders', MyOrdersView.as_view(), name='orders_user'),
    path('api/user/my/wallet', MyWalletView.as_view(), name='wallet_user'),
    #payment
    path('api/user/manageSelectedPayment/<int:payment_method_id>', ManageSelectedPaymentView.as_view(), name='manage_selected_payment'),
     ###################   PAYMENT PROCCESS  #################
    path('api/user/processPayment/<str:order_number>/<int:gateway_id>', ProcessPaymentView.as_view(), name='list_onlineMethod'),   
    

    ################# CALLBACK PAYMENT ######################
    path('api/callback/payment/', CallbackPaymentView.as_view(), name='callback_payment'),   


    # JWT routes for token handling
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    ####################     PRODUCT  API    ##################
    # Routes without middleware
    path('api/product/create', ProductCreateView.as_view(), name='create_product'),
    path('api/product/list', ProductsListView.as_view(), name='list_product'),
    path('api/product/show/<int:id>', ProductShowView.as_view(), name='show_product'),
    path('api/product/update/<int:id>', ProductUpdateView.as_view(), name='update_product'),
    path('api/product/delete/<int:id>', ProductDeleteView.as_view(), name='delete_product'),
    ###
    path('api/product/view/<int:id>', ProductAddView.as_view(), name='add_view_product'),
    path('api/product/like/<int:id>', ProductLikeView.as_view(), name='add_like_product'),
    path('api/product/dislike/<int:id>', ProductDislikeView.as_view(), name='remove_like_product'),
    path('api/product/review/<int:id>', ProductReviewView.as_view(), name='review_product'),


   
    ####################    CATEGORY  API    ##################
    # Routes without middleware
    path('api/category/create', CategoryCreateView.as_view(), name='create_category'),
    path('api/category/list', CategoriesListView.as_view(), name='list_category'),
    path('api/category/show/<int:id>', CategoryShowView.as_view(), name='show_category'),
    path('api/category/update/<int:id>', CategoryUpdateView.as_view(), name='update_category'),
    path('api/category/delete/<int:id>', CategoryDeleteView.as_view(), name='delete_category'),


    ####################     CART  API    ##################
    # Routes without middleware
    path('api/cart/items/show', CartItemsShow.as_view(), name='cart_items_show'),
    path('api/cart/item/add/<int:product_id>', AddToCart.as_view(), name='add_item_to_cart'),
    path('api/cart/item/remove/<int:product_id>', RemoveFromCart.as_view(), name='remove_item_from_cart'),

     ####################     INVOICE  API    ##################
    # Routes without middleware
    path('api/invoice/create/<str:order_number>', InvoiceCreate.as_view(), name='invoice_create'),
    path('api/cart/item/add/<int:product_id>', AddToCart.as_view(), name='add_item_to_cart'),
    path('api/cart/item/remove/<int:product_id>', RemoveFromCart.as_view(), name='remove_item_from_cart'),


     ####################     ORDER  API    ##################
    # Routes without middleware
    path('api/user/create/order/<int:address_id>', CreateOrderView.as_view(), name='order_create'),
    path('api/user/myOrders', MyOrdersView.as_view(), name='my_orders'),
    path('api/user/order/<int:order_id>', ShowOrderView.as_view(), name='show_order'),
    path('api/user/addShipping/<int:shipping_id>/order/<str:order_number>', AddShippingToOrderView.as_view(), name='add_shipping_to_order'),

    ####################     SHIPPINGMETHOD  API    ##################
    path('api/shippingMethod/create', CreateShippingMethodView.as_view(), name='create_shippingMethod'),
    path('api/shippingMethod/update/<int:id>', UpdateShippingMethodView.as_view(), name='update_shippingMethod'),
    path('api/shippingMethod/list', ShippingMethodListView.as_view(), name='list_shippingMethod'),


    ####################     PAYMENTMETHOD  API    ##################
    path('api/paymentMethod/create', CreatePaymentMethodView.as_view(), name='create_paymentMethod'),
    path('api/paymentMethod/update/<int:id>', UpdatePaymentMethodView.as_view(), name='update_paymentMethod'),
    path('api/paymentMethod/list', PaymentMethodListView.as_view(), name='list_paymentMethod'),  

    ####################     ONLINEGATEWAY  API    ##################
    path('api/onlineMethodGateway/create', CreatePaymentGatewayView.as_view(), name='create_onlineMethod'),
    path('api/onlineMethodGateway/update/<int:id>', UpdatePaymentGatewayView.as_view(), name='update_onlineMethod'),
    path('api/onlineMethodGateway/list', PaymentGatewayListView.as_view(), name='list_onlineMethod'),


]

##################
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

