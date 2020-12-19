from django.contrib import admin
from django.urls import path, include
from .views import Table1APIView, Table1Details

urlpatterns = [
    path('table1/', Table1APIView.as_view()),
    path('table1/<int:id>/', Table1Details.as_view()),
]
