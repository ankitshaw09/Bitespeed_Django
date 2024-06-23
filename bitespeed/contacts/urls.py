from django.urls import path
from .views import add_contact,identify_contact

urlpatterns = [
    path('add-contact/', add_contact, name='add_contact'),
    path('identify/', identify_contact, name='identify_contact'),
]
