from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from petstagram.pets.forms import PetCreateForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.pets.utils import get_pet_by_name_and_username


# Create your views here.

# pet_add, pet_details, pet_edit, pet_delete
@login_required
def pet_details(request, username, pet_slug):
    pet = get_pet_by_name_and_username(pet_slug)

    context = {
        'pet': pet,
        'photos_count': pet.photo_set.count(),
        'pet_photos': pet.photo_set.all(),
    }

    return render(request,
                  template_name='pets/pet-details-page.html',
                  context=context,
                  )


@login_required
def pet_add(request):
    if request.method == 'GET':
        form = PetCreateForm()
    else:
        # request.method == 'post'
        form = PetCreateForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()

            return redirect('profile-details', pk=1)  # TODO: fix when auth.

    context = {
        'form': PetCreateForm(),
    }

    return render(request, template_name='pets/pet-add-page.html', context=context)


@login_required
def pet_edit(request, username, pet_slug):
    # TODO: use 'username' when auth
    pet = Pet.objects \
        .filter(slug=pet_slug) \
        .get()
    if request.method == 'GET':
        form = PetEditForm(instance=pet)
    else:
        form = PetEditForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet-details', username=username, pet_slug=pet_slug)

    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
    }

    return render(request, template_name='pets/pet-edit-page.html', context=context)


@login_required
def pet_delete(request, username, pet_slug):
    pet = Pet.objects \
        .filter(slug=pet_slug) \
        .get()
    if request.method == 'GET':
        form = PetDeleteForm(instance=pet)
    else:
        form = PetDeleteForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('profile-details', pk=1)

    context = {
        'form': form,
        'pet_slug': pet_slug,
        'username': username,
    }

    return render(request, template_name='pets/pet-delete-page.html', context=context)
