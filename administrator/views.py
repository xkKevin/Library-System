from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse

from administrator.models import Administrator
from administrator.models import LibRoot
def login_adminRoot(request):
    '''
    超管denglu
    :param request:
    :return:
    '''

    if request.method == "GET":
        try:
            admin = request.GET["username"]
            password = request.GET["psw"]
            temp = LibRoot.objects.get(root_name=admin)

            if temp:
                if admin ==temp.root_name and password ==temp.password:
                    response = JsonResponse({'result': True})
            else:
                response = JsonResponse({'result': False})
            return response
        except Exception as e:
            return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


def update_lib(request):
    '''
    管理员修改图书馆员
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == 'admin':
        if request.method == "GET":
            try:
                admin = request.GET["username"]
                password = request.GET["psw"]
                temp = Administrator.objects.get(administrator_name=username)

                if temp:
                    if not password is "":
                        temp.password = password
                    temp.save()
                    response = JsonResponse({'result': True})
                else:
                    response = JsonResponse({'result': False})
                return response
            except Exception as e:
                return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


def update_adminPsw(request):
    '''
    超管修改超管功能
    :param request:
    :return:
    '''

    if request.method == "GET":
        try:
            admin = request.GET["username"]
            password = request.GET["psw"]
            temp = LibRoot.objects.get(root_name=admin)

            if temp:
                if not password is "":
                    temp.password = password
                temp.save()
                response = JsonResponse({'result': True})
            else:
                response = JsonResponse({'result': False})
            return response
        except Exception as e:
            return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


def get_adminPsw(request):
    '''
    超管获取图书管理员密码
    :param request:
    :return:
    '''

    if request.method == "GET":
        try:
            admin = request.GET["username"]
            temp = Administrator.objects.get(administrator_name=admin)
            response = JsonResponse({'result': True, "psw": temp.password})
            return response
        except Exception as e:
                return JsonResponse({'result': False, "psw": ""})
    else:
        return HttpResponseRedirect(reverse("index"))
