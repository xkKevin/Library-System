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
from django.conf.urls import url,include
from django.contrib import admin
import librarian.views as librarian_views
import reader.views as reader_views
import administrator.views as administrator_views


urlpatterns = [
    # 网页 url
    url(r'^admin/', admin.site.urls),
    url(r'^$', librarian_views.index, name="index"),
    url(r'^login/$', reader_views.login, name="login"),
    url(r'^register/$', reader_views.register, name="register"),
    url(r'^clear_message/$', librarian_views.clear_message, name="logout"),
    url(r'^user_message/$', reader_views.user_message, name="user_message"),
    url(r'^add_book/$', librarian_views.add_book, name="add_book"),
    url(r'^search_book/$', librarian_views.search_book, name="search_book"),
    # api js 请求 url
    url(r'^test_user_name/api/$', reader_views.user_name_is_available, name="test_user_name_api"),
    url(r'^register/api/$', reader_views.register_post, name="register_api"),
    url(r'^login/api/$', reader_views.login_post, name="login_api"),
    url(r'^isbn/api/$', librarian_views.book_message_api, name="isbn_api"),
    url(r'^add_book/api/$', librarian_views.add_book_api, name="add_book_api"),
    url(r'^reserve/api/$', librarian_views.reserve_api, name="reserve_api"),
    url(r'^search_book/api/$', librarian_views.search_book_api, name="search_book_api"),
    url(r'^i18n/', include('django.conf.urls.i18n')),

]
# urlpatterns += i18n_patterns('',)
