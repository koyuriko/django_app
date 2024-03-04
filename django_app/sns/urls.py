from django.urls import path
from . import views #.はカレントディレクトリを表す

app_name = 'sns'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='index'),
    path('edit/<int:num>', views.edit, name='edit'),
    path('delete/<int:num>', views.delete, name='delete'),
    path('post', views.post, name='post'),
    path('post/<int:num>', views.post, name='post'),
    path('filter/', views.filter, name='filter'),
    path('filter/<int:num>', views.filter, name='filter'),
    path('goods', views.goods, name='goods'),
    path('good/<int:good_id>', views.good, name='good'),
]