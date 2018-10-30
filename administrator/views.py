from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
# Create your views here.
from django.urls import reverse
import time
from administrator.models import Administrator
from administrator.models import LibRoot
from librarian.models import Role


def admin_change_password(request):
    '''
    管理员修改密码
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if not username == 'anti_man':
        return render(request, 'index.html')
    return render(request, 'admin_change_passwd.html')


def login(request):
    return render(request, 'Adminlogin.html')


def Adminlogin(request):
    username = request.session.get('username', "None")
    if not username == 'anti_man':
        return render(request, 'index.html')

    rule = Role.objects.first()
    all_librarian = Administrator.objects.all()
    return render(request, 'admin2.html', {'rule': rule, 'all_librarian': all_librarian})


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
                if admin == temp.root_name and password == temp.password:

                    request.session.set_expiry(0)
                    request.session['username'] = 'anti_man'
                    request.session['login_time'] = time.time()
                    return JsonResponse({'result': True})
                else:
                    return JsonResponse({'result': False})
            else:
                return JsonResponse({'result': False})
        except:
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
            newPaw = ""
            oldPsw = ""
            try:
                oldPsw = request.GET["oldPsw"]
                newPaw = request.GET["newPaw"]
                confirPsw = request.GET["confirPsw"]
            except:
                pass
            admin = "admin"
            temp = LibRoot.objects.get(root_name=admin)

            if temp:
                if not newPaw is "":
                    if oldPsw == temp.password:
                        temp.password = newPaw
                    else:
                        return JsonResponse({"result": False})
                temp.save()
                response = JsonResponse({'result': True})
            else:
                response = JsonResponse({'result': False})
            return response
        except Exception as e:
            return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


def create_lib(request):
    username = request.session.get('username', "None")
    if username == 'anti_man':
        if request.method == "GET":
            libname = request.GET["name"]
            psw = request.GET["psw"]
            lib = Administrator()
            lib.administrator_name = libname
            lib.password = psw
            lib.authority = 1
            lib.save()
            return JsonResponse({'result': True})
    else:
        return JsonResponse({'result': False, "msg": "数据库保存错误"})


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
            request.session["current_operated_lib_name"] = admin
            response = JsonResponse({'result': True, "account": temp.administrator_name, "psw": temp.password})
            return response
        except Exception as e:
                return JsonResponse({'result': False,  "account": "", "psw": ""})
    else:
        return HttpResponseRedirect(reverse("index"))


# 系统管理员界面编辑图书馆管理员信息
def edit_librarian(request, librarian_name):
    # lib_name = request.session["current_operated_lib_name"]
    librarian = Administrator.objects.get(administrator_name=librarian_name)

    return render(request, 'edit_librarian.html', {'librarian': librarian})


def manager_edit_librarian(request):
    if request.method == "GET":
        try:
            newPaw = ""
            oldPsw = ""
            try:
                lib_name = request.GET["lib_name"]
                oldPsw = request.GET["oldPsw"]
                newPaw = request.GET["newPaw"]
                confirPsw = request.GET["confirPsw"]
            except:
                pass

            librarian = Administrator.objects.get(administrator_name=lib_name)

            if librarian:
                if not newPaw is "":
                    if oldPsw == librarian.password and newPaw == confirPsw:
                        librarian.password = newPaw
                    else:
                        return JsonResponse({"result": False})
                librarian.save()
                response = JsonResponse({'result': True})
            else:
                response = JsonResponse({'result': False})
            return response
        except Exception as e:
            return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


# 系统管理员删除图书管理员
def delete_librarian(request):
    if request.method == "GET":
        try:
            lib_name = request.GET['lib_name']
            librarian = Administrator.objects.get(administrator_name=lib_name)
            librarian.delete()
            return JsonResponse({'result': True})

        except:
                return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))


# 系统管理员改变罚金数目等规则
def edit_rules(request):
    if request.method == "GET":
        try:
            overdue_fine = request.GET["overdue_fine"]
            return_days = request.GET["return_days"]
            deposit_amount =request.GET["deposit_amount"]

            rule = Role.objects.first()
            rule.days_limit = return_days
            rule.deposit = deposit_amount
            rule.fine = overdue_fine
            rule.save()
            return JsonResponse({'result': True})
        except:
            return JsonResponse({'result': False})
    else:
        return HttpResponseRedirect(reverse("index"))
