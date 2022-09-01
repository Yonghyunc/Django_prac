from multiprocessing import context
import random
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'articles/index.html')


def greeting(request):
    # context 데이터가 많아질 경우, 다음과 같이 작성하는 것이 바람직
    foods = ['apple', 'banana', 'coconut', 'mango', 'grape']
    info = {
        'name' : 'Alice',
    }

    # 다른 이름으로 사용 가능하지만, 관행적으로 context 사용 
    context = {
        'info' : info,
        'foods' : foods,
    }
    return render(request, 'articles/greeting.html', context)


def dinner(request):
    foods = ['apple', 'banana', 'coconut', 'mango', 'grape']
    pick = random.choice(foods)
    context = {
        'pick' : pick,
        'foods' : foods,
    }
    return render(request, 'articles/dinner.html', context)


def throw(request):
    return render(request, 'articles/throw.html')


def catch(request):
    # throw에서 보낸 데이터를 찾아서 저장
    # print(request)
    # print(type(request))
    # print(request.GET)
    # print(request.GET.get('message'))
    message = request.GET.get('message')
    context = {
        'message' : message,
    }
    return render(request, 'articles/catch.html', context)

def hello(request, name):
    context = {
        'name' : name,
    }
    return render(request, 'articles/hello.html', context)