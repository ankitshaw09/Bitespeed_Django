# contacts/views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services import link_contacts, consolidate_contact
from .serializers import ContactSerializer

@api_view(['POST'])
def add_contact(request):
    phone_number = request.data.get('phoneNumber')
    email = request.data.get('email')

    contact = link_contacts(phone_number=phone_number, email=email)
    

    serializer = ContactSerializer(contact)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def identify_contact(request):
    phone_number = request.data.get('phoneNumber')
    email = request.data.get('email')

    contact = link_contacts(phone_number=phone_number, email=email)
    consolidated_contact = consolidate_contact(contact)

    return Response({"contact": consolidated_contact}, status=status.HTTP_200_OK)