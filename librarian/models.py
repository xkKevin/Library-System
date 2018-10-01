from django.db import models
from reader.models import User


class Book(models.Model):
    author = models.CharField(max_length=50)
    isbn = models.IntegerField(primary_key=True)
    total_num = models.IntegerField(null=False)
    available_num = models.IntegerField(null=False)
    book_name = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=20, null=False)
    place = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.book_name


class AllBook(models.Model):
    book_id = models.IntegerField(auto_created=True, primary_key=True)
    is_available = models.BooleanField(null=False, default=True)
    isbn = models.ForeignKey(Book, related_name="all_book_isbn")

    def __str__(self):
        return self.book_id


class BorrowOrder(models.Model):
    order_id = models.IntegerField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, related_name="borrow_order_user")
    book = models.ForeignKey(AllBook, related_name="borrow_order_book")
    borrow_time = models.DateTimeField(null=False)
    debt = models.IntegerField(default=0)
    return_time = models.DateTimeField()
    is_return = models.BooleanField(null=False)

    def __str__(self):
        return self.order_id


class ReserveOrder(models.Model):
    order_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, related_name="reserve_order_user")
    book = models.ForeignKey(AllBook, related_name="reserve_order_user")
    borrow_time = models.DateTimeField(null=False)
    successful = models.BooleanField(null=False)

    def __str__(self):
        return self.order_id


class Role(models.Model):
    books_limit = models.IntegerField()
    days_limit = models.IntegerField()
    deposit = models.IntegerField()
    fine = models.IntegerField()

    def __str__(self):
        return self.books_limit