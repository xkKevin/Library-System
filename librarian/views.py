from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    '''
    首页
    :param request:
    :return:
    '''

    username = request.session.get('username', "None")
    if username != "None":
        message = {'login': True, "username": username}
    else:
        message = {'login': False, "username": username}
    return render(request, 'index.html', message)


def clear_message(request):
    '''
    注销
    :param request:
    :return:
    '''
    del request.session["username"]
    return HttpResponseRedirect(reverse("index"))
