from importlib.resources import contents
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Message, Good
from .forms import MessageForm

# indexビュー関数です
@login_required(login_url='/admin/login/') #login時にのみindexビュー関数を呼び出して使用出来ます
def index(request, page=1):
    max = 10 #ページに表示する件数
    form = MessageForm()
    msgs = Message.objects.all()
    #ページネーション
    paginate = Paginator(msgs, max)
    page_items = paginate.get_page(page)
    params = {
        'login_user':request.user,
        'form':form,
        'contents':page_items,
    }
    return render(request, 'sns/index.html', params)

# goods関数です（いいねリストページ）
@login_required(login_url='/admin/login/') #login時にのみgoodsリストページ関数を呼び出して使用出来ます
def goods(request):
#ログインユーザーのもうgoodしたmessageを絞り込み取得
    goods = Good.objects.filter(owner=request.user)
    params = {
        'login_user':request.user,
        'contents':goods,
    }
    return render(request, 'sns/good.html', params)

# edit関数です
@login_required(login_url='/admin/login/') #login時にのみedit関数を呼び出して使用出来ます
def edit(request, num):
    obj = Message.objects.get(id=num)
    if (request.method == 'POST'):
        form = MessageForm(request.POST, instance=obj)
        if form.is_valid(): #バリデーションがOKの時
            post = form.save(commit=False) #messageFormの内容をインスタンスに保存する前処理
            post.owner = request.user #messageテーブルにログインしている人のレコードを保存
            post.save()
            return redirect(to='/sns/post') #送信したら投稿リストページにリダイレクト、edit関数の処理を呼ぶ\
        else:
            form = MessageForm(request.POST, instance=obj)
            params = {
            'login_user':request.user,
            'id': num,
            'form': MessageForm(instance=obj),
            }
    return render(request, 'sns/edit.html', params)

# delete関数です
@login_required(login_url='/admin/login/') #login時にのみdelete関数を呼び出して使用出来ます
def delete(request, num):
    messages = Message.objects.get(id=num)
    if (request.method == 'POST'):
            messages.delete()
            return redirect(to='/sns/post') #送信したら投稿リストページにリダイレクト
    params = {
            'login_user':request.user,
            'id': num,
            'item':messages,
            }
    return render(request, 'sns/delete.html', params)

# filter関数です
@login_required(login_url='/admin/login/') #login時にのみfilter関数を呼び出して使用出来ます
def filter(request, num):
    uname = User.objects.get(id=num)
    messages = Message.objects.filter(owner=uname)
    params = {
            'login_user':request.user,
            'userid':num,
            'username':uname,
            'contents':messages,
    }
    return render(request, 'sns/filter.html', params)

# postビュー関数です
@login_required(login_url='/admin/login/') #login時にのみpost関数を呼び出して使用出来ます
def post(request):
    #post送信処理
    if request.method == 'POST':
    #送信内容取得
        form = MessageForm(request.POST)
    #バリデーションがOK
        form.is_valid()
        post = form.save(commit=False) #messageFormの内容をインスタンスに保存する前処理
        post.owner = request.user #messageテーブルにログインしている人のレコードを保存
        post.save()
        return redirect(to='/sns/') #送信したらトップページにリダイレクト、index関数の処理を呼ぶ
    else:
        messages = Message.objects.filter(owner=request.user)
        params = {
            'login_user':request.user,
            'contents':messages,
            }
    return render(request, 'sns/post.html', params)

# good関数、いいねボタンの処理です
@login_required(login_url='/admin/login/') #login時にのみgood関数を呼び出して使用出来ます
def good(request, good_id):
    #goodいいねmessageを取得
    good_msg = Message.objects.get(id=good_id)
    #goodいいねの数の確認
    is_good = Good.objects.filter(owner=request.user).filter(message=good_msg).count()
    #ゼロより大きいか確認（good済なのか判定）
    if is_good > 0:
    #ログインユーザーgood済のgood解除したいmessageを取得
        reject_good_msg = Message.objects.get(id=good_id)
    #ログインユーザーgood済のgood解除したいmessage総数の確認
        is_good = Good.objects.filter(owner=request.user).filter(message=reject_good_msg).count()
    #goodいいねレコードインスタンスを削除(goodいいねした後、goodいいね数を0クリア)
        Good.objects.filter(owner=request.user).filter(message=reject_good_msg).delete()
    #システムメッセージをアラート表示
        messages.success(request, 'Goodを解除しました')
    #相手のgoodいいね    を解除したので、いいねを減らす処理
        reject_good_msg.good_count -= 1
    #goodいいね解除、マイナス1を保存
        reject_good_msg.save()
        return redirect(to='/sns') #送信したらトップページにリダイレクト、index関数の処理を呼ぶ
    else:
    #goodいいねレコードインスタンスを削除
        Good.objects.filter(owner=request.user).filter(message=good_msg).delete()
    #相手のgoodいいねmessageのgoodいいねカウントを足す
        good_msg.good_count += 1
    #goodいいね数1プラスをを保存
        good_msg.save()
    #インスタンスを作成してgoodいいねを保存（いいね数1プラスを保存）
        good = Good()
    #ログインユーザーをgoodテーブルに保存
        good.owner = request.user
    #goodいいね数1をgoodテーブルのメッセージに保存
        good.message = good_msg
        good.save()
    #システムメッセージをアラート表示
        messages.success(request, '新しくGoodしました')
    return redirect(to='/sns')