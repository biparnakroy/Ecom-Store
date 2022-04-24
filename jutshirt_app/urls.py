from django.urls import path, include , re_path
from . import views , admin_views

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('doSignup/', views.do_signup, name="doSignup"),
    path('logout_user/', views.logout_user, name="logout_user"),
    #path('',views.index, name='index'),

    #===================== Admin Views============================
    path('admin_home/', admin_views.Admin_home.as_view(), name="admin_home"),
]
