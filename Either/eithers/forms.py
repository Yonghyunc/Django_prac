from dataclasses import field
from django import forms
from .models import Vote, Comment


class VoteForm(forms.ModelForm):
    # title = forms.CharField(
    #     label = '투표 이름',
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder':'투표 이름'
    #         }
    #     ),
    #     error_messages={
    #         'required': '제목은 필수 입력사항입니다.'
    #     }
    # )

    # issue_a = forms.CharField(
    #     label = '항목 A',
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder':'항목 A'
    #         }
    #     ),
    #     error_messages={
    #         'required': '항목 A는 필수 입력사항입니다.'
    #     }
    # )

    # issue_b = forms.CharField(
    #     label = '항목 B',
    #     widget=forms.TextInput(
    #         attrs={
    #             'placeholder':'항목 B'
    #         }
    #     ),
    #     error_messages={
    #         'required': '항목 B는 필수 입력사항입니다.'
    #     }
    # )

    class Meta:
        model = Vote
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'content',
            'pick',
        )
