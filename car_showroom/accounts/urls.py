from django.urls import path, include

from car_showroom.accounts.views import SignUpView, SignInView, SignOutView, UserDetailView, UserEditView, \
    UserDeleteView

urlpatterns = (
    path('register/', SignUpView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', UserDetailView.as_view(), name='user details'),
        path('edit/', UserEditView.as_view(), name='edit user'),
        path('delete/', UserDeleteView.as_view(), name='delete user'),
    ]))
)
