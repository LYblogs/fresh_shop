from django.urls import path

from user import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # 收货地址
    path('user_site/', views.user_site, name='user_site'),

    # 个人中心
    path('user_info/',views.user_info,name='user_info')
]
