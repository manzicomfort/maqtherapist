from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.therapist_view, name='therapist'),
    path('get_response/', views.get_ai_response, name='get_response'),
]
