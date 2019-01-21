from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import GoodsCategory, Goods
from user.models import User


def index(request):
    # 如果访问首页，返回渲染的首页index.html页面
    if request.method == 'GET':
        # 方式一
        # categorys = GoodsCategory.objects.all()
        # result =[]
        # for category in categorys:
        #     data = []
        #     goods = category.goods_set.all()[:4]
        #     data = [category,goods]
        #     result.append(data)
        # 方式二
        categorys = GoodsCategory.objects.all()
        return render(request, 'index.html', {'categorys': categorys})


def detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html', {'goods': goods})


def my_list(request, id):
    if request.method == 'GET':
        page = int(request.GET.get('page', 1))
        all_goods = Goods.objects.filter(category_id=id)
        cate = Goods.objects.filter(category_id=id).first()
        cate = cate.category
        pg = Paginator(all_goods, 5)
        all_goods = pg.page(page)
        return render(request, 'list.html', {'all_goods': all_goods, 'my_id': id, 'cate': cate})


def goods_search(request):
    if request.method == 'GET':
        word = request.GET.get('word')
        all_goods = Goods.objects.filter(name__contains=word)
        return render(request, 'list.html', {'all_goods': all_goods})
