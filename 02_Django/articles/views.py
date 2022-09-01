from django.shortcuts import render, redirect
from .models import Article

# Create your views here.

def index(request):
    # DB 전체 데이터 조회
    articles = Article.objects.all()
    # 최신순으로 조회
    # articles = Article.objects.all()[::-1]
    # articles = Article.objects.order_by('-pk')
    context = {
        'articles' : articles,
    }
    return render(request, 'articles/index.html', context)


def new(request):
    return render(request, 'articles/new.html')


def create(request):
    # 사용자의 데이터를 받아서
    title = request.POST.get('title')
    content = request.POST.get('content')

    # DB에 저장
    # 두번째 방법 사용
    article = Article(title=title, content=content)
    article.save()

    # return redirect('/articles/')
    return redirect('articles:detail', article.pk)


def detail(request, pk):
    article = Article.objects.get(pk=pk) # key=value
    context = {
        'article' : article,
    }
    return render(request, 'articles/detail.html', context)


def delete(request, pk):
    article = Article.objects.get(pk=pk)
    article.delete()
    return redirect('articles:index')


def edit(request, pk):
    article = Article.objects.get(pk=pk)
    context = {
        'article' : article,
    }
    return render(request, 'articles/edit.html', context)


def update(request, pk):
    article = Article.objects.get(pk=pk)
    article.title = request.POST.get('title')
    article.content = request.POST.get('content')
    article.save()

    return redirect('articles:detail', article.pk)