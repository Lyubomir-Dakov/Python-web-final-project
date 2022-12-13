from django.urls import path, include

from car_showroom.common.views import index, about, like_car, comment_car, test_drive_car, edit_test_drive, \
    del_test_drive

urlpatterns = (
    path('', index, name='home page'),
    path('about/', about, name='about page'),
    path('like/<int:car_id>/', like_car, name='like car'),
    path('comment/<int:car_id>/', comment_car, name='add comment'),
    path('test-drive/<int:car_id>/', include([
        path('', test_drive_car, name='test drive'),
        path('edit/', edit_test_drive, name='edit test drive'),
        path('delete/', del_test_drive, name='delete test drive'),
    ]))
)
