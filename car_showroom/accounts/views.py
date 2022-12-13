from django.contrib.auth import views as auth_views, get_user_model, login
from django.urls import reverse_lazy
from django.views import generic as views
from car_showroom.accounts.forms import AppUserCreationForm

UserModel = get_user_model()


class SignUpView(views.CreateView):
    template_name = 'accounts/sign-up-page.html'
    form_class = AppUserCreationForm
    success_url = reverse_lazy('home page')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in-page.html'


class SignOutView(auth_views.LogoutView):
    pass


class UserDetailView(views.DetailView):
    template_name = 'accounts/profile-details-page.html'
    model = UserModel

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.request.user == self.object
        context['cars_count'] = self.object.car_set.count()
        cars = self.object.car_set.prefetch_related('carlike_set')
        context['likes_count'] = sum(x.carlike_set.count() for x in cars)
        return context


class UserEditView(views.UpdateView):
    template_name = 'accounts/profile-edit-page.html'
    model = UserModel
    fields = ('email',)

    def get_success_url(self):
        return reverse_lazy('user details', kwargs={
            'pk': self.request.user.pk,
        })


class UserDeleteView(views.DeleteView):
    template_name = 'accounts/profile-delete-page.html'
    model = UserModel
    success_url = reverse_lazy('home page')
