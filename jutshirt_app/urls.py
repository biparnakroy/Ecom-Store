from django.urls import path, include , re_path
from . import views , admin_views

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

    #===================== Form Validation Views============================
    path('admin_email_check/', admin_views.Email_check.as_view(), name="admin_email_check"),
    path('admin_username_check/', admin_views.Username_check.as_view(), name="admin_username_check"),
]
