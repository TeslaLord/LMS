from django.urls import path
from . import views

# app_name = "users"
urlpatterns = [
    # path('', views.home, name='home'),
    #     path('homework/', views.homework, name='homework'),
    path('homework2/<int:pk>', views.HomeworkDetailView.as_view(), name='homework2'),
    path('section_list/', views.SectionListView.as_view(), name='section_list'),
    path('section_detail/<int:pk>',
         views.SectionDetailView.as_view(), name='section_detail'),
    path('profile_detail/<int:pk>',
         views.ProfileDetailView.as_view(), name='profile_detail')
]
