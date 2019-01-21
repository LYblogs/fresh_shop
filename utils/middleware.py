import re

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from cart.models import ShoppingCart
from goods.models import Goods
from user.models import User, UserLook


class SessionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            path = request.path
            detail_path = '/goods/detail/.*/'
            if re.match(detail_path, path):
                detail_id = path.split('detail/')[1].split('/')[0]
                detail = Goods.objects.filter(pk=detail_id).first()
                looks = UserLook.objects.filter(user_id=user_id, goods_id=detail_id).first()
                # 如果不是第一次存储,就直接向里面添加id
                if looks:
                    count = looks.count
                    looks.count = count + 1
                    looks.save()
                # 如果是第一次存储就创建一个列表并把id保存进去
                else:
                    UserLook.objects.create(user_id=user_id, count=1,
                                            goods_id=detail)
        # 2.需要区分哪些地址需要做登录校验，哪些地址不需要做登录界面
        path = request.path
        if path == '/':
            return None
        not_need_check = ['/user/register', '/user/login/',
                          '/goods/index/', '/goods/detail/.*/',
                          '/cart/.*/', '/cart/add_cart/',
                          '/user/logout/', '/media/.*/', '/static/.*/']
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path不需要登录校验
                return None
        # 需要校验时，判断是否登录，没有登录就跳转到登录
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionToDbMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 同步session中商品信息和数据库中购物车表的数据
        # 1. 判断是否登录，登录了才做数据同步操作

        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            # 2.1判断session中商品是否存在于数据库中，存在就更新
            # 2.2 如果不存在就创建
            # 2.3同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=se_goods[0]).first()

                    if cart:
                        # 更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2]
                                                    )

            # 同步数据库中的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            # 组装多个商品格式[[goods_id,nums,is_select],[goods_id,nums,is_select]]
            if db_carts:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods

                # result =[]
                # for cart in db_carts:
                #     data = [cart.goods_id,cart.nums,cart.is_select]
                #     result.append(data)
        return response
