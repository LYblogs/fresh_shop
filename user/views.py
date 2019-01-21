from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from goods.models import Goods
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress, UserLook


def register(request, ):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 使用表单form校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号不存在与数据库，并且密码一直，邮箱格式正确
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                                password=password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # errors =
            return render(request, 'register.html', {'errors': form.errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 用户存在并且密码正确
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(request, 'login.html', {'errors': errors})


def logout(request):
    if request.method == 'GET':
        del request.session['user_id']
        if request.session.get('goods'):
            del request.session['goods']
        return HttpResponseRedirect(reverse('user:login'))


def user_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        return render(request, 'user_center_site.html', {'user_address': user_address})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            tel = form.cleaned_data['tel']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=tel,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})

        pass


def user_info(request):
    if request.method == 'GET':
        user_id = request.session['user_id']
        recent_goods = UserLook.objects.filter(user_id=user_id).order_by('-last_time')[:5]
        return render(request, 'user_center_info.html', {'recent_goods': recent_goods})
