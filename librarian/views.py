from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from librarian.models import Book, AllBook, BorrowOrder, ReserveOrder
from reader.models import User

import requests
import datetime


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


def reserve_api(request):
    if request.method == 'POST':
        book_id = request.POST['book_id']
        user_id = request.POST['user_id']

        book = AllBook.objects.get(book_id=book_id)
        user = User.objects.get(user_id=user_id)
        ReserveOrder.objects.create(book_id=book_id, user_id=user_id,
                                    borrow_time=datetime.datetime.now(), successful=False)


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

