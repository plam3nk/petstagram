from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from django.contrib.auth import forms as auth_form

from petstagram.accounts.forms import RegisterUserForm

# Create your views here.

# register_user, login_user, show_profile_details, edit_profile, delete_profile
UserModel = get_user_model()


class RegisterUserView(views.CreateView):
    form_class = RegisterUserForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        # user = self.object

        login(self.request, self.object)

        # When user is registered through the administrator it will not send email!
        # send_mail() # Not good one.

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['next'] = self.request.GET.get('next', '')

        return context

    def get_success_url(self):
        return self.request.POST.get('next', self.success_url)


class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login-page.html'
    # success_url = ''
    # def get_success_url(self):


class LogoutUserView(auth_views.LogoutView):
    pass


class ProfileDetailsView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    profile_image = static('images/person.png')

    def get_profile_image(self):
        if self.object.profile_picture is not None:
            return self.object.profile_picture
        return self.profile_image

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile_image'] = self.get_profile_image()
        context['pets'] = self.request.user.pet_set.all()

        return context

    # 'UserModel.objects.all()' returns 'queryset'
    # To work provide 'model', 'queryset' or 'get_queryset'


# def show_profile_details(request, pk):
#     pets = Pet.objects.all()
#
#     context = {
#         'pets': pets,
#     }
#
#     return render(request, template_name='accounts/profile-details-page.html')

class ProfileEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'


class ProfileDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
