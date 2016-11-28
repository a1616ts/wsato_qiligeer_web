from django.conf.urls import url
from domains import views

urlpatterns = [
    # 書籍
    url(r'^domain/$', views.book_list, name='domain_list'),   # 一覧
    url(r'^domain/add/$', views.book_edit, name='domain_add'),  # 登録
    url(r'^domain/mod/(?P<book_id>\d+)/$', views.book_edit, name='domain_mod'),  # 修正
    url(r'^domain/del/(?P<book_id>\d+)/$', views.book_del, name='domain_del'),   # 削除
]
