from django.urls import  path
import view

urlpatterns =[
    path('check-sha',view.getShaDetails),
    path('decrypt',view.decryptFile),
]