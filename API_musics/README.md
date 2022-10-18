# Django REST Framework
▫ DRF를 활용한 음악 정보 관련 REST API 서버 구축 

▫ 프로젝트 이름 : my_api  
▫ 앱 이름 : musics  

<br><br>

---

## 1️⃣ Model & Admin
``` python
# musics/models.py

from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=200)


class Music(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
```
<br>

``` python
# musics/admin.py

from django.contrib import admin
from .models import Artist, Music


admin.site.register(Artist)
admin.site.register(Music)
```

``` 
$ python manage.py createsuperuser
```
> Username : yong21

<br><br>

---

## 2️⃣ Serializer

<br>

### ⭐ ArtistListSerializer
▫ 모든 가수의 정보 반환   
▫ id, name 필드 출력   

<br>

### ⭐ ArtistSerializer
▫ 상세 가수의 정보 생성 및 반환  
▫ id, name, music_set, music_count 필드 출력  

<br>

### ⭐ MusicListSerializer
▫ 모든 음악 정보 반환  
▫ id, title 필드 출력  

<br>

### ⭐ MusicSerializer
▫ 상세 음악의 정보 생성 및 반환  
▫ id, title, artist 필드 출력 

<br>

``` python
# musics/serializers.py

from rest_framework import serializers
from .models import Artist, Music


class ArtistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id', 'name',)


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id', 'title', 'artist',)
        read_only_fields = ('artist',)


class ArtistSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True, read_only=True)
    music_count = serializers.IntegerField(source='music_set.count', read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class MusicListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Music 
        fields = ('id', 'title',)
```
> 역참조 위해 ArtistSerializer - MusicSerializer 클래스 위치 조정함 


<br><br>

---

## 3️⃣ url & view

``` python
# my_api/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('musics.urls')),
]
```
<br><br>

### 📌 GET
▫ 모든 가수의 id, name 컬럼을 JSON으로 응답

<br>

``` python
urlpatterns = [
    path('artists/', views.artist_list),
]
```
<br>

``` python
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import ArtistListSerializer
from .models import Artist, Music


@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistListSerializer(artists, many=True)
    return Response(serializer.data)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196319351-2282967f-5c86-4b8e-bb34-f0545c59b2a3.png)

<br><br>


### 📌 POST 
▫ 가수 정보 생성  
- 검증 성공 : 가수 정보 DB 저장, 생성된 가수의 정보와 201 Created 응답
- 검증 실패 : 400 Bad Request 응답

<br>

``` python
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .serializers import ArtistListSerializer, ArtistSerializer
from .models import Artist, Music


@api_view(['GET', 'POST'])
def artist_list(request):
    if request.method == 'GET':
        artists = Artist.objects.all()
        serializer = ArtistListSerializer(artists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196320296-5be25c59-0308-4213-a132-db20343e6415.png)

<br><br>

### 📌 GET
▫ 특정 가수의 모든 컬럼을 JSON으로 응답  
▫ 특정 가수의 노래 정보와 노래의 개수 정보를 함께 응답  

<br>

``` python
urlpatterns = [
    ...
    path('artists/<int:artist_pk>/', views.artist_detail),
]
```
<br>

``` python
@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = Artist.objects.get(pk=artist_pk)
    serializer = ArtistSerializer(artist)
    return Response(serializer.data)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196322071-3a2c912d-f415-4976-93c6-c88ac8250ca4.png)


<br><br>

### 📌 POST
▫ 특정 가수의 음악 정보 생성  
- 검증 성공 : 음악 정보 DB 저장, 생성된 음악 정보와 201 Created 응답
- 검증 실패 : 400 Bad Request 응답

<br>

``` python
urlpatterns = [
    ...
    path('artists/<int:artist_pk>/music/', views.music_create),
]
```
<br>

``` python
@api_view(['POST'])
def music_create(request, artist_pk):
    artist = Artist.objects.get(pk=artist_pk)
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(artist=artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
```
> MusicSerializer는 모델폼이 아니기 때문에 **commit**이 존재하지 않음  
> save 괄호 안에 바로 객체를 할당하여 참조하는 artist의 값을 넣어줌  

> Serializer에 **읽기 전용 필드** 반드시 설정해주기 !!   
> : 유효성 검사 제외, 데이터 조회 시에는 출력  
> `read_only_fields = ('artist',)`

<br>

![image](https://user-images.githubusercontent.com/93974908/196324624-a1a28e09-3a3e-48df-9d4c-c422b4bb1923.png)

<br><br>

### 📌 GET

▫ 모든 음악의 id, title 컬럼을 JSON으로 응답 

<br>

``` python 
urlpatterns = [
    ...
    path('music/', views.music_list),
]
```
<br>

``` python 
@api_view(['GET'])
def music_list(request):
    musics = Music.objects.all()
    serializer = MusicListSerializer(musics, many=True)
    return Response(serializer.data)
```

<br>

![image](https://user-images.githubusercontent.com/93974908/196326701-6fc1aab8-ff72-4ce2-ba82-38d2f4907111.png)

<br><br>

### 📌 GET
▫ 특정 음악의 모든 컬럼 JSON으로 응답 

<br>

``` python
urlpatterns = [
    ...
    path('music/<int:music_pk>/', views.music_detail),
]
```

<br>

``` python
@api_view(['GET'])
def music_detail(request, music_pk):
    music = Music.objects.get(pk=music_pk)
    serializer = MusicSerializer(music)
    return Response(serializer.data)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196327421-89e33e0e-638b-43bc-a8bd-e710b88c3796.png)


<br><br>

### 📌 PUT
▫ 특정 음악의 정보 수정 
- 검증 성공 : 수정된 음악의 정보 DB 저장
- 검증 실패 : 400 Bad Request 응답 

▫ 수정 완료 후, 수정된 음악의 정보 응답

<br>

``` python
@api_view(['GET', 'PUT'])
def music_detail(request, music_pk):
    music = Music.objects.get(pk=music_pk)

    if request.method == 'GET':
        serializer = MusicSerializer(music)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196327907-ad0819ce-2c12-4b4c-87c7-149cc1ba0b1d.png)



<br><br>

### 📌 DELETE
▫ 특정 음악의 정보 삭제   
▫ 삭제 완료 후, 삭제한 음악의 id, 204 No Content 응답

<br>

``` python
@api_view(['GET', 'PUT', 'DELETE'])
def music_detail(request, music_pk):
    music = Music.objects.get(pk=music_pk)

    if request.method == 'GET':
        serializer = MusicSerializer(music)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        music.delete()
        return Response(music_pk, status=status.HTTP_204_NO_CONTENT)
```
<br>

![image](https://user-images.githubusercontent.com/93974908/196335254-f7213a6c-b805-4ecc-adbe-1d714173453d.png)
