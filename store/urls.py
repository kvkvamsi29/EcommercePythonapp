from django.urls import path
from django.contrib.auth import views as auth_views

# ===== CORE VIEWS =====
from store.views.home import store
from store.views.product_detail import product_detail
from store.views.orders import order_invoice, orders
from store.views.checkout import checkout

# ===== AUTH =====
from store.views.signup import Signup
from store.views.login import Login
from store.views.forgot_password import (
    forgot_password,
    forgot_password_verify,
    reset_password_new,
)

from store.views.complete_account import (
    complete_account,
    complete_account_verify,
)

# ===== CART =====
from store.views.cart import cart, add_to_cart, cart_count, cart_count_api
from store.views.cart_api import mini_cart
from store.views.cart_api import api_cart_add
from store.views.cart_api import api_cart_update
from store.views.otp import  verify_otp, send_otp
from store.views.logout import custom_logout
from store.views.order_success import order_success
from store.views.saved_address import edit_address, delete_address
from store.views.payments import payment_page,place_order_cod
# ===== PAYMENT (OTP) ===

# ===== WISHLIST =====



urlpatterns = [
    # ===== STORE =====
    path("", store, name="store"),
    path("store/", store, name="store"),

    # ===== PRODUCTS =====
   
    path("product/<int:id>/", product_detail, name="product_detail"),

    # path("product/<int:id>/", product_detail, name="product_detail_by_id"),

    # ===== CART =====
    path("cart/", cart, name="cart"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("api/cart/count/", cart_count_api, name="cart_count_api"),
    path("api/cart/mini/", mini_cart, name="mini_cart"),
    path("api/cart/add/<int:product_id>/", api_cart_add, name="api_cart_add"),
    path("api/cart/update/<int:product_id>/", api_cart_update, name="api_cart_update"),
    # path("api/cart/add/<int:product_id>/", api_cart_add, name="api_cart_add"),


    # ===== CHECKOUT & ORDERS =====
    path("checkout/", checkout, name="checkout"),
    path("orders/", orders, name="orders"),
    path("order-success/", order_success, name="order_success"),
    path("edit_address/<int:id>/", edit_address, name="edit_address"),
    path("delete_address/<int:id>/", delete_address, name="delete_address"),
    path(
    "forgot-password/verify/",
    forgot_password_verify,
    name="forgot_password_verify"
),

path(
    "reset-password/new/",
    reset_password_new,
    name="reset_password_new"
),

path(
    "complete-account/",
    complete_account,
    name="complete_account"
),

path(
    "complete-account/verify/",
    complete_account_verify,
    name="complete_account_verify"
),
    # ===== PAYMENT (OTP APIs) =====
    path("send-otp/", send_otp, name="send_otp"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("payment/", payment_page, name="payment"),
    path("place_order_cod/", place_order_cod, name="place_order_cod"),
   
    # ===== WISHLIST =====
    # path("wishlist/", wishlist_view, name="wishlist"),
    # path("api/wishlist/toggle/<int:product_id>/", toggle_wishlist, name="toggle_wishlist"),
    path("orders/invoice/<str:order_id>/", order_invoice, name="order_invoice"),

    # ===== AUTH =====
    path("signup/", Signup.as_view(), name="signup"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", custom_logout, name="logout"),

    path("forgot-password/", forgot_password, name="forgot_password"),

    # ===== PASSWORD RESET =====
   
    path(
        "reset-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
