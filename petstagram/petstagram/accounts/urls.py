from django.urls import path, include

from .views import RegisterUserView, LoginUserView, LogoutUserView, ProfileDetailsView, ProfileEditView,\
    ProfileDeleteView

urlpatterns = [
    # localhost:8000/accounts/register/
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', ProfileDetailsView.as_view(), name='profile-details'),
        path('edit/', ProfileEditView.as_view(), name='profile-edit'),
        path('delete/', ProfileDeleteView.as_view(), name='profile-delete'),
    ]))
]
