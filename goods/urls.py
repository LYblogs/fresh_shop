from django.urls import path

from goods import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('detail/<int:id>/', views.detail, name='detail'),
    # 查看更多
    path('my_list/<int:id>/', views.my_list, name='my_list'),
    # 搜索
    path('goods_search/', views.goods_search, name='goods_search')
]
