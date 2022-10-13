from django.shortcuts import render, redirect
from .models import Vote, Comment
from .forms import VoteForm, CommentForm
import random

# Create your views here.
def index(request):
    votes = Vote.objects.all()
    random_id = random.choice(list(range(1, len(votes) + 1)))
    context = {
        'votes': votes,
        'random_id': random_id,
    }
    return render(request, 'eithers/index.html', context)


def create(request):
    print(request)
    if request.method == "POST":
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save()
            return redirect('eithers:detail', vote.pk)
    else:
        form = VoteForm()
    context = {
        'form': form,
    }
    return render(request, 'eithers/create.html', context)


def detail(request, pk):
    vote = Vote.objects.get(pk=pk)
    comment_form = CommentForm()
    comments = vote.comment_set.all()

    cnt_a = 0
    cnt_b = 0

    for comment in comments:
        if comment.pick == 'issue_a':
            cnt_a += 1
        else:
            cnt_b += 1
    if cnt_a != 0 or cnt_b != 0:
        percent_a = int(round((cnt_a / (cnt_a + cnt_b)) * 100, 0))
        percent_b = 100 - percent_a
    else:
        percent_a = 50
        percent_b = 50

    context = {
        'vote': vote,
        'comment_form': comment_form,
        'comments': comments,
        'percent_a': percent_a,
        'percent_b': percent_b,
    }
    return render(request, 'eithers/detail.html', context)


def comments_create(request, pk):
    vote = Vote.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.vote = vote
        comment.save()
    return redirect('eithers:detail', vote.pk)


def comments_delete(request, vote_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('eithers:detail', vote_pk)
