# REST_API 실습 

<br><br>

---
# 단일 모델 

### 1️⃣ djangorestframework & django_seed 설치 후 앱 등록
``` 
$ pip install djangorestframework

$ pip install django-seed
```
``` python 
# settings.py

INSTALLED_APPS = [
    'articles',
    'django_extensions',
    'rest_framework',
    'django_seed',
    ...
]
```
<br><br>

### 2️⃣ 모델 작성 및 마이그레이션

``` python
# articles/models.py

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
```
$ python manage.py makemigrations

$ python manage.py migrate
```
<br><br>

### 3️⃣ django-seed 라이브러리 활용하여 5개의 데이터 생성 

``` 
$ python manage.py seed articles --number=5
```

![image](https://user-images.githubusercontent.com/93974908/196308269-693fe573-117a-4d52-b86b-28a09886c554.png)


<br><br>

### 4️⃣ serializers 작성
▫ serializers.py 생성

#### ▫ ArticleListSerializer
- 모든 게시글 정보를 반환하기 위한 ModelSerializer
- id, title 필드 정의

#### ▫ ArticleSerializer
- 게시글 상세 정보를 반환 및 생성하기 위한 ModelSerializer
- 모든 필드 정의

``` python
# articles/serializers.py

from rest_framework import serializers
from .models import Article


class ArticleListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ('id', 'title',)


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
```


<br><br>

## 📌 GET
▫ 모든 게시글의 id과 title 컬럼을 JSON 데이터 타입으로 응답  

``` python
urlpatterns = [
    path('articles/', views.article_list),
]
```

``` python
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ArticleListSerializer
from .models import Article


@api_view(['GET'])
def article_list(request):
    articles = Article.objects.all()
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)
```

![image](https://user-images.githubusercontent.com/93974908/196309745-6ab7717e-fccd-4717-9bc0-468a410886ce.png)


<br><br>

## 📌 POST
▫ 검증 성공 : 새로운 게시글의 정보를 DB에 저장하고, 저장된 게시글의 정보 응답  
▫ 검증 실패 : 400 Bad Request


``` python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import ArticleListSerializer, ArticleSerializer
from .models import Article


@api_view(['GET', 'POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```

![image](https://user-images.githubusercontent.com/93974908/196310938-b06a8bd0-278b-44e6-9124-53a73ad59cac.png)

![image](https://user-images.githubusercontent.com/93974908/196311398-26a0a20f-e211-4272-9a7f-b31e486b8b91.png) 

<br><br>

## 📌 GET
▫ 특정 게시글의 모든 컬럼을 JSON 타입으로 응답

``` python
urlpatterns = [
    ...
    path('articles/<int:article_pk>/', views.article_detail),
]
```

``` python
@api_view(['GET'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)
    serializer = ArticleSerializer(article)
    return Response(serializer.data)
```

![image](https://user-images.githubusercontent.com/93974908/196311154-12ae7d87-86c2-4a6f-b94f-f68c24f8f2e9.png)

<br><br>

## 📌 PUT
▫ 특정 게시물의 정보 수정   
▫ 검증 성공 : 수정된 게시글의 정보를 DB에 저장   
▫ 검증 실패 : 400 Bad Request  
▫ 수정이 완료되면 수정한 게시글의 정보 응답  

``` python
@api_view(['GET', 'PUT'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```

![image](https://user-images.githubusercontent.com/93974908/196312045-0d9ae557-6dd5-4777-b505-9724b0ee5485.png)

<br><br>

## 📌 DELETE
▫ 특정 게시글을 삭제하고, 삭제가 완료되면 삭제한 게시글의 id 응답  

``` python
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, article_pk):
    article = Article.objects.get(pk=article_pk)

    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        article.delete()
        return Response(article_pk, status=status.HTTP_200_OK)
```

![image](https://user-images.githubusercontent.com/93974908/196313107-bc764032-7719-47f0-862d-f93cb7f0f8b0.png)