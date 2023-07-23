from django.core.mail import send_mail
from django.urls import include, path

from .views import PhotoAddView, photo_details, photo_edit, photo_delete

urlpatterns = [
    # photos/
    path('add/', PhotoAddView.as_view(), name='photo-add'),
    path('<int:pk>/', include([
        path('', photo_details, name='photo-details'),
        path('edit/', photo_edit, name='photo-edit'),
        path('delete/', photo_delete, name='photo-delete')
    ]))
]
