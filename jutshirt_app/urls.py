from django.urls import path, include , re_path
from . import views , admin_views , customer_views

urlpatterns = [
    path('', views.signup_page, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('doSignup/', views.do_signup, name="doSignup"),
    path('logout_user/', views.logout_user, name="logout_user"),
    #path('',views.index, name='index'),

    #===================== Admin Views============================
    path('admin_home/', admin_views.Admin_home.as_view(), name="admin_home"),
    path('admin_profile/', admin_views.AdminProfileView.as_view(), name="admin_profile"),
    path('admin_profile_edit/', admin_views.AdminProfileEditView.as_view(), name="admin_profile_edit"),
    path('admin_add_products/', admin_views.Admin_add_products.as_view(),name="admin_add_products"),
    path('admin_manage_products/', admin_views.Manage_products.as_view(),name="admin_manage_products"),
    path('admin_view_prod/<prod_uuid>/', admin_views.View_products.as_view(), name="admin_view_prod"),
    path('admin_edit_prod/<prod_uuid>/', admin_views.Edit_products.as_view(), name="admin_edit_prod"),
    path('admin_delete_prod/<prod_uuid>', admin_views.Delete_prod.as_view(),name="admin_delete_prod"),
    path('admin_manage_customers/', admin_views.Manage_customers.as_view(),name="admin_manage_customers"),
    path('admin_view_customer/<uuid>', admin_views.View_customers.as_view(),name="admin_view_customer"),
    path('admin_edit_customer/<uuid>', admin_views.View_customers.as_view(),name="admin_edit_customer"),


    path('home/', customer_views.Customer_home.as_view(),name="customer_home"),
    path('products/', customer_views.Customer_product.as_view(),name="customer_product"),
    path('product_view/<uuid>/', customer_views.Customer_product_view.as_view(), name="customer_product_view"),
    path('add_to_cart/', customer_views.Add_to_cart.as_view(), name="add_to_cart"),
    path('cart/', customer_views.Customer_cart.as_view(), name="customer_cart"),
    path('delete_cart_item/<uuid>/<size>/', customer_views.Delete_from_cart.as_view(), name="delete_cart_item"),
    path('checkout/', customer_views.Customer_checkout.as_view(), name="customer_checkout"),
    
    #===================== Form Validation Views============================
    path('admin_email_check/', admin_views.Email_check.as_view(), name="admin_email_check"),
    path('admin_username_check/', admin_views.Username_check.as_view(), name="admin_username_check"),
]
