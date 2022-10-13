from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        exclude = ('user', 'like_users',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': '댓글을 입력하세요',
                'rows': 2,
                'cols': 50,
            }
        )
    )

    class Meta:
        model = Comment
        exclude = ('article', 'user', )