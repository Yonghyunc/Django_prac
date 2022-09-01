from django.urls import path

# 명시적 상대경로
from . import views

app_name = 'articles'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('greeting/', views.greeting, name='greeting'),
    path('dinner/', views.dinner, name='dinner'),
    path('throw/', views.throw, name='throw'),
    path('catch/', views.catch, name='catch'),
    
    # 변수 값에 따라 하나의 path()에 여러 페이지를 연결시킬 수 있음
    # 변수는 <> 안에 정의, views 함수의 인자로 할당됨
    path('hello/<str:name>/', views.hello, name='hello'),
]
