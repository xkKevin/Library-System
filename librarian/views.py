from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from librarian.models import Book, AllBook, BorrowOrder, ReserveOrder
from reader.models import User

import requests


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


def search_book_api(request):
    '''
    查询书籍API
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return JsonResponse({"result": False, "msg": "未登录"})
    book_type = request.GET.get('book_type', None)
    book_name = request.GET.get('book_name', None)
    if book_name is None or book_type is None:
        return JsonResponse({"result": False, "msg": "查询参数不正确"})
    try:
        if book_type == "全部":
            result = Book.objects.filter(book_name__contains=book_name)
        else:
            result = Book.objects.filter(book_name__contains=book_name, type__contains=book_type)
        if len(result) > 0:
            result_json = render(request, 'result_json.html', {"book_list": result})
            return JsonResponse({"result": True, "html": bytes.decode(result_json.content)})
        else:
            return JsonResponse({"result": False, "msg": "很抱歉未找到相关图书信息"})
    except :
        return JsonResponse({"result": False, "msg": "查询出错"})


def search_book(request):
    '''
    查询书籍
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return HttpResponseRedirect(reverse("login"))
    book_type = request.GET.get('book_type', None)
    book_name = request.GET.get('book_name', None)
    if book_name is None or book_type is None:
        return JsonResponse({"result": False, "msg": "查询参数不正确"})
    try:
        if book_type == "全部":
            result = Book.objects.filter(book_name__contains=book_name)
        else:
            result = Book.objects.filter(book_name__contains=book_name, type__contains=book_type)
        return render(request, 'search_results.html', {"book_list": result})

    except :
        return JsonResponse({"result": False, "msg": "查询出错"})


def reserve_api(request):
    '''
    预约API
    :param request:
    :return:
    '''
    username = request.session.get('username', "None")
    if username == "None":
        return JsonResponse({'result': False, "msg": "未登录"})
    if request.method == 'POST':
        isbn = request.POST['isbn']

        try:
            book = AllBook.objects.filter(isbn=isbn, is_available=True).first()
            user = User.objects.get(user_name=username)
            borrow = ReserveOrder.objects.filter(isbn=isbn, user_id=user.user_id).first()
            if borrow:
                borrow.borrow_time = timezone.now()
                return JsonResponse({"result": True, "update": True})
            isbn = Book.objects.get(isbn=isbn)
        except Exception as e:
            return JsonResponse({'result': False, "msg": "数据库错误"})
        if not (book and user and isbn):
            return JsonResponse({'result': False, "msg": "未查到相关数据"})
        borrow_time = timezone.now()
        try:
            result = ReserveOrder.objects.create(book=book, user=user, borrow_time=borrow_time, successful=False,
                                                 isbn=isbn)
            if result:
                return JsonResponse({"result": True, "update": False})
            else:
                return JsonResponse({"result": False, "msg": "数据库保存失败"})
        except Exception as e:
            return JsonResponse({"result": False,  "msg": "数据库错误"})


def clear_message(request):
    '''
    注销
    :param request:
    :return:
    '''
    del request.session["username"]
    return HttpResponseRedirect(reverse("index"))


def add_book(request):
    '''
    添加图书
    :param request:
    :return:
    '''
    return render(request, 'add_book.html')


def book_message_api(request):
    '''
    通过ISBN查询书籍
    :param request:
    :return: JSON数据
    '''
    isbn = request.GET.get('isbn', None)
    douban_url = 'https://api.douban.com/v2/book/isbn/'
    result_json ={}
    if isbn:
        result = requests.get(douban_url+isbn)
        if result.status_code == 200:
            result_json['result'] = True
            import json
            book_message = json.loads(result.text)
            if 'msg' not in book_message.keys():
                try:
                    result_json['isbn'] = book_message['isbn13']
                    result_json['author'] = ','.join(book_message['author'])
                    result_json['image_url'] = book_message['image']
                    result_json['book_name'] = book_message['title']
                    result_json['type'] = ','.join([i['name'] for i in book_message['tags']])
                except KeyError:
                    pass
        else:
            result_json['result'] = False
        return JsonResponse(result_json)


def add_book_api(request):
    '''
    添加图书
    :param request:
    :return:
    '''
    if request.method == "POST":
        try:
            isbn = request.POST['isbn']
            try:
                temp = Book.objects.get(isbn=isbn)
                if temp:
                    return JsonResponse({"result": False, 'msg': "该书已存在"})
            except Book.DoesNotExist:
                pass
            author = request.POST['author']
            book_name = request.POST['book_name']
            image_url = request.POST['image_url']
            total_num = request.POST['total_num']
            type = request.POST["type"]
            place = request.POST['place']

            book = Book()
            book.isbn = isbn
            book.author = author
            book.book_name = book_name
            book.image_url = image_url
            book.total_num = total_num
            book.type = type
            book.place = place
            book.available_num = total_num
            book.save()
            all_book_list = list()
            for x in range(int(total_num)):
                all_book_list.append(AllBook(isbn=book, is_available=True))
            AllBook.objects.bulk_create(all_book_list)
        except Exception as e:
            return JsonResponse({'result': False, "msg": "数据库保存错误"})
    return JsonResponse({'result': True})

