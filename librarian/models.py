from django.db import models
from reader.models import User
from administrator.models import Administrator


class Book(models.Model):
    author = models.CharField(max_length=50)
    isbn = models.IntegerField(primary_key=True)
    total_num = models.IntegerField(null=False)
    available_num = models.IntegerField(null=False)
    book_name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=20, null=False)
    place = models.CharField(max_length=50, null=False)
    image_url = models.CharField(max_length=100, default='None')
    price = models.CharField(max_length=100, default='100')

    def __str__(self):
        return self.book_name


class AllBook(models.Model):
    book_id = models.IntegerField(auto_created=True, primary_key=True)
    is_available = models.BooleanField(null=False, default=True)
    isbn = models.ForeignKey(Book, related_name="all_book_isbn")

    def __str__(self):
        return str(self.book_id)


class BorrowOrder(models.Model):
    order_id = models.IntegerField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, related_name="borrow_order_user")
    book = models.ForeignKey(AllBook, related_name="borrow_order_book")
    borrow_time = models.DateTimeField(null=False)
    debt = models.IntegerField(default=0)
    return_time = models.DateTimeField(null=True)
    is_return = models.BooleanField(null=False)
    # 判断是否为历史订单 方便后期查找
    expire = models.BooleanField(default=False)
    # 最后计算欠费的时间
    last_count_time = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.borrow_time)


class ReserveOrder(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, related_name="reserve_order_user")
    book = models.ForeignKey(AllBook, related_name="reserve_order_book")
    isbn = models.ForeignKey(Book, related_name="reserve_order_isbn")
    borrow_time = models.DateTimeField(null=False)
    successful = models.BooleanField(null=False)
    # 判断是否为历史订单 方便后期查找
    expire = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


class Role(models.Model):
    books_limit = models.IntegerField()
    days_limit = models.IntegerField()
    deposit = models.IntegerField()
    fine = models.IntegerField()

    def __str__(self):
        return str(self.books_limit)


class Notice(models.Model):

    title = models.TextField(null=False)
    content = models.TextField(null=False)
    author = models.ForeignKey(Administrator, related_name="Notices")
    expire = models.BooleanField(null=False)
    issue_time = models.DateField(null=False, auto_now_add=True)

    def __str__(self):
        return str(self.title)


class MoneyOrder(models.Model):

    teller = models.ForeignKey(Administrator, null=False, related_name="MoneyOrder")
    order_type = models.IntegerField(null=False)
    user_id = models.ForeignKey(User, null=False, related_name="_Money_order")
    num = models.IntegerField(null=False)
    order_time = models.DateField(null=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)


# 用于每天自动更新一次数据库borrower表的debt，更新后添加一条数据
class AutoUpdateDB(models.Model):
    is_updated = models.BooleanField()
    updated_date = models.DateField(auto_now_add=True)
