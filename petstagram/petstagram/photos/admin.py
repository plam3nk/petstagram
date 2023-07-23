from django.contrib import admin

from petstagram.photos.models import Photo


# Register your models here.


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'publication_date', 'pets')

    @staticmethod
    def pets(self, photo_obj):
        tagged_pets = photo_obj.tagged_pets.all()
        if tagged_pets:
            return ', '.join(p.name for p in tagged_pets)
        else:
            return 'No pets'

