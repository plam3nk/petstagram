import pyperclip
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from pyperclip import copy

from petstagram.common.forms import PhotoCommentForm, SearchForm
from petstagram.common.models import PhotoLike
from petstagram.common.utils import get_user_liked_photos, get_photo_url
from petstagram.photos.models import Photo


def apply_likes_count(photo):
    photo.likes_count = photo.photolike_set.count()

    return photo


def apply_user_liked_photo(photo):
    # TODO: fix this for user when authentication is available.
    photo.is_liked_by_user = photo.likes_count > 0

    return photo


def index(request):
    photos = Photo.objects.all()
    search_form = SearchForm(request.GET)

    if search_form.is_valid():
        search_text = search_form.cleaned_data['search_text']
        photos = photos.filter(tagged_pets__name__icontains=search_text)

    for photo in photos:
        photo.liked_by_user = photo.photolike_set\
            .filter(user=request.user)\
            .exists()

    context = {
        'photos': photos,
        'comment_form': PhotoCommentForm(),
        'search_form': search_form,
    }
    return render(
        request,
        template_name='common/home-page.html',
        context=context
    )


@login_required
def like_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    kwargs = {
        'photo': photo,
        'user': request.user
    }
    like_object = PhotoLike.objects \
        .filter(**kwargs) \
        .first()
    if like_object:
        like_object.delete()
    else:
        new_like_object = PhotoLike(**kwargs)
        new_like_object.save()
    # http://127.0.0.1:8000/
    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
    # Method 1
    # photo_like = PhotoLike(
    #     photo_id=photo_id,
    # )
    # photo_like.save()

    # Method 3 'Wrong - additional call to DB'
    # Correct, only if validation is needed
    # photo = Photo.objects.get(pk=photo_id)
    # PhotoLike.objects.create(
    #     photo=photo
    # )


@login_required
def share_photo(request, photo_id):
    # copy(request.META['HTTP_HOST'] + resolve_url('photo details', photo_id))
    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


@login_required
def comment_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    if request.method == 'POST':
        form = PhotoCommentForm(request.POST)
        if form.is_valid():
            print('form is valid')
            new_comment_instance = form.save(commit=False)
            new_comment_instance.photo = photo
            new_comment_instance.save()
        return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")
