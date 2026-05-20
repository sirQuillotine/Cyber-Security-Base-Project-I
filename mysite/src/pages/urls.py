from django.urls import path

from .views import homePageView, addView, accountView, evilPageView

urlpatterns = [
    path('', homePageView, name='home'),
    path('add/', addView, name='add'),
    path('accounts/<str:account>/', accountView, name='account'),
    path('evil/', evilPageView, name='evil'),  # serve evil page from same origin

]
