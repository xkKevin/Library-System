import random

from django.shortcuts import render
from django.http import JsonResponse

from administrator.models import Administrator
from tool.changePsw import SendEmail
from reader.models import User
import time
from django.http import HttpResponseRedirect
from django.urls import reverse
from librarian.models import ReserveOrder, BorrowOrder, MoneyOrder, Role


def forget_passwd_page(request):
    return render(request, 'forget_passwd.html')


def change_passwd_page(request):
    '''
    修改密码
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'change_passwd.html')


def change_passwd_page(request):
    '''
    修改密码
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return HttpResponseRedirect(reverse("login"))
    return render(request, 'change_passwd.html')


def login(request):
    '''
    登陆
    :param request:
    :return:
    '''
    return render(request, 'login.html')


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    return render(request, 'register.html')


def user_name_is_available(request):
    '''
    测试用户名是否可用
    :param request:
    :return:
    '''

    if request.method == "POST":
        flag = False
        try:
            user_name = request.POST["username"]
            temp = User.objects.get(user_name=user_name)
            if temp:
                flag = True
        except Exception as e:
            pass
        if flag:
            return JsonResponse({'result': False})
        else:
            return JsonResponse({'result': True})


def register_post(request):
    '''
    注册api
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            password = request.POST["password"]
            username = request.POST["username"]
            email = request.POST["email"]
            libraian_name = request.session["admin_name"]
            libraian = Administrator.objects.get(administrator_name=libraian_name)
            user = User(user_name=username, password=password, email=email)
            user.save()

            # 押金数目
            deposit = Role.objects.first().deposit

            temp = User.objects.get(user_name=username)

            if temp:
                # 添加押金记录

                temp1 = MoneyOrder.objects.create(user=temp, order_type='D', num=deposit, librarian=libraian)
                if temp1:
                    response = JsonResponse({'result': True})
                else:
                    response = JsonResponse({'result': False})
            else:
                response = JsonResponse({'result': False})

            return response
        except:
            return JsonResponse({'result': False})


def login_post(request):
    '''
    登陆api
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            password = request.POST["password"]
            username = request.POST["username"]
            remember = request.POST['remember']
            temp = User.objects.get(user_name=username, password=password)
            if temp:
                user_id = temp.user_id
                response = JsonResponse({'result': True})
                if not remember:
                    request.session.set_expiry(0)
                request.session['username'] = username
                request.session['user_id'] = user_id
                request.session['login_time'] = time.time()
            else:
                response = JsonResponse({'result': False})
            return response
        except:
            return JsonResponse({'result': False})


def user_message(request):
    '''
    用户信息
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return HttpResponseRedirect(reverse("login"))
    try:
        user = User.objects.get(user_name=username)
        if user:
            borrow_order_list = BorrowOrder.objects.filter(user_id=user.user_id)
            reserve_order_list = ReserveOrder.objects.filter(user_id=user.user_id)
            money_order_list = MoneyOrder.objects.filter(user=user)

            # 计算全部罚金
            all_fine = 0
            for borrow_order in borrow_order_list:
                all_fine += borrow_order.debt

            return render(request, 'user_message.html', {'user_id': user.user_id,
                                                         'user_email': user.email,
                                                         'user_name': user.user_name,
                                                         'reserve_order_list': reserve_order_list,
                                                         'borrow_order_list': borrow_order_list,
                                                         'all_fine': all_fine,
                                                         'money_order_list': money_order_list
                                                         }
                          )
        else:
            return HttpResponseRedirect(reverse("login"))
    except:
        return HttpResponseRedirect(reverse("login"))


def sendEmailToChangePsw(request):
    if request.method == "GET":
        try:
            username = request.GET["username"]
            temp = User.objects.get(user_name=username)
            if temp:
                email = temp.email
                seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
                sa = []
                for i in range(8):
                    sa.append(random.choice(seed))
                salt = ''.join(sa)
                code = salt
                s = SendEmail()
                s.send("图书管理系统密码修改", temp.password, temp.email)
                s.close_smtp()
                response = JsonResponse({'result': True, "code": code})
            else:
                response = JsonResponse({'result': False})
            return response
        except:
            return JsonResponse({'result': False})


def update_psw(request):
    '''
    更新密码
    :param request:
    :return:
    '''
    if request.method == "GET":
        try:
            username = request.GET["username"]
            email = request.GET["email"]
            password = request.GET["psw"]
            temp = User.objects.get(user_name=username)

            if temp:
                if not email is "":
                    temp.email = email
                if not password is "":
                    temp.password = password
                temp.save()
                response = JsonResponse({'result': True})
            else:
                response = JsonResponse({'result': False})
            return response
        except Exception as e:
            return JsonResponse({'result': False})


if __name__ == "__main__":
    print(User.objects.get(user_name="15130120136"))
