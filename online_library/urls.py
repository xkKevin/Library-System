"""online_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import librarian.views as librarian_views
import reader.views as reader_views
import administrator.views as administrator_views


urlpatterns = [
    # 网页 url
    url(r'^admin/', admin.site.urls),
    url(r'^$', librarian_views.index, name="index"),
    url(r'^login/$', reader_views.login, name="login"),
    url(r'^loginAdmin/$', administrator_views.login, name="admin_login"),
    url(r'^loginAdmin/manage/$', administrator_views.Adminlogin, name="admin_manage_login"),
    url(r'^loginAdminRoot/$', administrator_views.login_adminRoot, name="loginAdminRoot"),
    url(r'^manage/$', librarian_views.manager_page, name="manage_page"),
    url(r'^update_reader/$', librarian_views.update_reader_page, name="update_reader_page"),
    url(r'^change_passwd/$', reader_views.change_passwd_page, name="change_passwd"),
    # 用户禁止注册 转由图书管理员注册读者 因而废弃该url
    # url(r'^register/$', reader_views.register, name="register"),
    url(r'^clear_message/$', librarian_views.clear_message, name="logout"),
    url(r'^user_message/$', reader_views.user_message, name="user_message"),
    url(r'^add_book/$', librarian_views.add_book, name="add_book"),
    url(r'^search_book/$', librarian_views.search_book, name="search_book"),
    url(r'^manager/add_reader/$', librarian_views.add_reader, name="manager_add_reader"),
    url(r'^manager/delete_reader/$', librarian_views.delete_reader, name="manager_delete_reader"),
    url(r'^manager/update_reader/$', librarian_views.update_reader, name="manager_update_reader"),
    url(r'^manager/update_readerByMe/$', librarian_views.update_readerByMe, name="manager_update_readerByMe"),
    url(r'^manager/get_readerHis/$', librarian_views.get_reader_history, name="manager_get_readerHis"),
    url(r'^manager/get_adminPsw/$', administrator_views.get_adminPsw, name="manager_get_adminPsw"),
    url(r'^manager/update_book_message/$', librarian_views.update_book_message_page, name="update_book_message"),
    # tyr admin更新超级管理员密码
    url(r'^admin/change_passwd/$', administrator_views.admin_change_password, name='admin_change_passwd'),
    url(r'^manager/update_adminPsw/$', administrator_views.update_adminPsw, name="manager_update_adminPsw"),
    # tyr admin更新lib密码
    url(r'^manager/update_libPsw/$', administrator_views.update_lib, name="manager_get_updatelibPsw"),
    # api js 请求 url
    url(r'^manager/return_book/api/$', librarian_views.return_book_api, name="manage_return_book_api"),
    url(r'^manager/borrow_book/api/$', librarian_views.borrow_book_api, name="manage_borrow_book_api"),
    url(r'^manager/user_message/api/$', librarian_views.manage_user_api, name="manage_user_message_api"),
    url(r'^manager_login/api/$', librarian_views.administrator_login_post, name="manage_login_api"),
    url(r'^test_user_name/api/$', reader_views.user_name_is_available, name="test_user_name_api"),
    url(r'^register/api/$', reader_views.register_post, name="register_api"),
    url(r'^login/api/$', reader_views.login_post, name="login_api"),
    url(r'^isbn/api/$', librarian_views.book_message_api, name="isbn_api"),
    url(r'^add_book/api/$', librarian_views.add_book_api, name="add_book_api"),
    url(r'^update_book/api/$', librarian_views.update_book, name="update_book_api"),
    url(r'^get_book/api/$', librarian_views.get_book, name="get_book_api"),
    url(r'^reserve/api/$', librarian_views.reserve_api, name="reserve_api"),
    url(r'^search_book/api/$', librarian_views.search_book_api, name="search_book_api"),
    url(r'^changePsw/api/$', reader_views.sendEmailToChangePsw, name="change_reader_psw"),
    url(r'^forgetpsw/$', reader_views.forget_passwd_page, name="forget_reader_psw"),
    url(r'^i18n/', include('django.conf.urls.i18n')),

]
