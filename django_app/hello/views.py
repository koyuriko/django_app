from django.shortcuts import render
from django.shortcuts import redirect
# from django.views.generic import FormView
from django.http import HttpResponse
from django.db.models import Count,Sum,Avg,Min,Max
from django.core.paginator import Paginator

from .models import Friend, Message
from .forms import FriendForm, MessageForm, FindForm
# from .forms import HelloForm,FindForm, CheckForm, 

# helloアプリの内容を書き換え
# index関数です

def index(request, num=1):
    data = Friend.objects.all()
    page = Paginator(data, 3) #3件づつリスト表示
    params = {
        'title': 'Hello',  # 動的にページに属性を与えます
        'message': '',
        'data': page.get_page(num),
    }
    # data = Friend.objects.all().order_by('age')  # ソート・昇順
    # data = Friend.objects.all().order_by('-age') #ソート・降順
    # data = Friend.objects.all().order_by('age').reverse() #ソート・逆順
    # re1 = Friend.objects.aggregate(Count('age'))
    # re2 = Friend.objects.aggregate(Sum('age'))/
    # re3 = Friend.objects.aggregate(Avg('age'))
    # re4 = Friend.objects.aggregate(Min('age'))
    # re5 = Friend.objects.aggregate(Max('age'))
    # msg = 'Sort as age<br>count:' + str(re1['age__count']) \
    #     + '<br>Sum:' + str(re2['age__sum']) \
    #     + '<br>Average:' + str(re3['age__avg']) \
    #     + '<br>Min:' + str(re4['age__min']) \
    #     + '<br>Max:' + str(re5['age__max'])
    return render(request, 'hello/index.html', params)

# Message関数です

def message(request, page=1):
    if (request.method == 'POST'):
        # obj = Message()
        # form = MessageForm(request.POST, instance=obj)
        form = MessageForm(request.POST)
        form.save()
    data = Message.objects.all()
    paginator = Paginator(data, 5) #5件づつリスト表示
    params = {
        'title': 'Message',  # 動的にページに属性を与えます
        'form': MessageForm(),
        'data': paginator.get_page(page),
    }
    return render(request, 'hello/message.html', params)

# create関数です

def create(request):
    if (request.method == 'POST'):
        friend = FriendForm(request.POST)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',  # 動的にページに属性を与えます
        'form': FriendForm(),
    }
    return render(request, 'hello/create.html', params)

# edit関数です

def edit(request, num):
    obj = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend = FriendForm(request.POST, instance=obj)
        friend.save()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',  # 動的にページに属性を与えます
        'id': num,
        'form': FriendForm(instance=obj),
    }
    return render(request, 'hello/edit.html', params)

# delete関数です

def delete(request, num):
    friend = Friend.objects.get(id=num)
    if (request.method == 'POST'):
        friend.delete()
        return redirect(to='/hello')
    params = {
        'title': 'Hello',  # 動的にページに属性を与えます
        'id': num,
        'obj': friend,
    }
    return render(request, 'hello/delete.html', params)

# find関数です

def find(request):
    if (request.method == 'POST'):
        msg = 'search result:'
        form = FindForm(request.POST)
        find = request.POST['find']
        list = find.split()
        data = Friend.objects.all()[int(list[0]):int(list[1])]
    else:
        msg = 'search words...'
        form = FindForm()
        data = Friend.objects.all()
    params = {
        'title': 'Hello',
        'message': msg,
        'form': form,
        'data': data,
    }
    return render(request, 'hello/find.html', params)

# check関数です

def check(request):
    params = {
        'title': 'Hello',
        'message': 'check validation.',
        'form': FriendForm(),
    }
    if (request.method == 'POST'):
        obj = Friend()
        form = FriendForm(request.POST, instance=obj)
        params['form'] = form
        if (form.is_valid()):
            params['message'] = 'OK:入力内容の不備はありません'
        else:
            params['message'] = 'NO good:チェックの結果、入力の不備があります'
    return render(request, 'hello/check.html', params)

# def find(request):
#     if (request.method == 'POST'):
#         msg = 'Search result:'
#         form = FindForm(request.POST)
#         find = request.POST['find']
#         list = find.split()
#         data = Friend.objects.all()[int(list[0]):int(list[1])]
#     else:
#         msg = 'Search words....'
#         form = FindForm()
#         data = Friend.objects.all()
#     params = {
#         'title': 'Hello',  # 動的にページに属性を与えます
#         'message': msg,
#         'form': form,
#         'data': data,
#     }
    # return render(request, 'hello/find.html', params)

    #    name = request.POST['name']
    #    mail = request.POST['mail']
    #    gender = 'gender' in request.POST
    #    age = int(request.POST['age'])
    #    birth = request.POST['birthday']
    #    friend = Friend(name=name,mail=mail,gender=gender, \
    #                    age=age,birthday=birth)
    #    friend.save()
    #    return redirect(to='/hello')
    # return render(request, 'hello/create.html', params)


# def index(request):
#     data = Friend.objects.all().values('id', 'name')
#     params = {
#         'title': 'Hello',  # 動的にページに属性を与えます
#         'data': data,
#     }
    # data = Friend.objects.all()
    # params = {
    #     'title': 'Hello',  # 動的にページに属性を与えます
    #     'message': 'all friends.',
    #     'data': [],
    #     'form': HelloForm()
    # }
    # if (request.method == 'POST'):
    #     num=request.POST['id']
    #     item = Friend.objects.get(id=num)
    #     params['data'] = [item]
    #     params['form'] = HelloForm(request.POST)
    # else:
    #     params['data'] = Friend.objects.all()

    # if (request.method == 'POST'):
    #     params['message'] = '名前:' + request.POST['name'] + \
    #     '<br>メール:' + request.POST['mail'] + \
    #     '<br>年齢:' + request.POST['age']
    #     params['form'] = HelloForm(request.POST)
    # return render(request, 'hello/index.html', params)


# class IndexView(FormView):
#     template_name = 'hello/index.html'
#     form_class = HelloForm
#     # success_url = '/'

#     def __init__(self):
#         self.params = {
#             'title': 'Hello',
#             'message': 'your data:',
#             'form': self.form_class(),
#         }

#     def get(self, request):
#         return render(self.request, self.template_name, self.params)

#     def form_valid(self, form):
#         self.params["message"] = '名前:{}<br>メール:{}<br>年齢:{}'.format(
#             form.cleaned_data['name'],
#             form.cleaned_data['mail'],
#             form.cleaned_data['age'],
#         )
#         print(self.request.POST)
#         self.params['form'] = self.form_class(self.request.POST)
#         return render(self.request, self.template_name, self.params)


# def index(request):
#     params = {
#         'title': 'Hello/index',  # 動的にページに属性を与えます
#         'msg': 'お名前は？',
#         # 'goto': 'next',
#     }
#     return render(request, 'hello/index.html', params)


# def form(request):
#     msg = request.POST['msg']
#     params = {
#         'title': 'Hello/Form',  # 動的にページに属性を与えます
#         'msg': 'こんにちは！' + msg + 'さん',
#         # 'goto': 'next',
#     }
#     return render(request, 'hello/index.html', params)

# def next(''request):
#     params = {
#         'title': 'Hello/Next',
#         'msg': 'デザイン制作の次のページです。',
#         'goto': 'index',
#     }
# return render(request, 'hello/index.html', params)

# def index(request):
# helloアプリの内容を書き換え
# return HttpResponse('Hello Django!')
# msg = request.GET['keys1']
# return HttpResponse('you typed:"' + msg + '".')
