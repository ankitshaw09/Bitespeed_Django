from .models import Contact
from django.db import models, transaction

@transaction.atomic
def link_contacts(phone_number=None, email=None):
    # Fetch existing contacts by phone number or email
    existing_contacts = Contact.objects.filter(
        models.Q(phoneNumber=phone_number) | models.Q(email=email),
        deletedAt__isnull=True
    ).order_by('createdAt')

    if not existing_contacts.exists():
        # Create a new primary contact if no existing contact is found
        contact = Contact(phoneNumber=phone_number, email=email, linkPrecedence='primary')
        contact.save()
        return contact

    # Find the primary contact
    primary_contact = existing_contacts.first()
    for contact in existing_contacts:
        if contact.linkPrecedence == 'primary' and contact.createdAt < primary_contact.createdAt:
            primary_contact = contact

    # Check if the incoming request has new information
    new_information = False
    if phone_number and phone_number != primary_contact.phoneNumber:
        new_information = True
    if email and email != primary_contact.email:
        new_information = True

    # Link all secondary contacts to the primary contact
    for contact in existing_contacts:
        if contact != primary_contact:
            contact.linkedId = primary_contact.id
            contact.linkPrecedence = 'secondary'
            contact.save()

    # Handle the case where a primary contact should turn into a secondary contact
    conflicting_primary_contacts = Contact.objects.filter(
        models.Q(phoneNumber=phone_number) | models.Q(email=email),
        linkPrecedence='primary',
        deletedAt__isnull=True
    ).exclude(id=primary_contact.id).order_by('createdAt')

    if conflicting_primary_contacts.exists():
        for conflicting_contact in conflicting_primary_contacts:
            if conflicting_contact.createdAt < primary_contact.createdAt:
                # Current primary contact becomes secondary
                primary_contact.linkPrecedence = 'secondary'
                primary_contact.linkedId = conflicting_contact.id
                primary_contact.save()

                # Update all secondary contacts of the current primary
                secondary_contacts = Contact.objects.filter(
                    linkedId=primary_contact.id,
                    deletedAt__isnull=True
                )
                for sec_contact in secondary_contacts:
                    sec_contact.linkedId = conflicting_contact.id
                    sec_contact.save()

                # Set the conflicting contact as the new primary
                conflicting_contact.linkPrecedence = 'primary'
                conflicting_contact.linkedId = None
                conflicting_contact.save()

                primary_contact = conflicting_contact

    # Create a new secondary contact if there is new information
    if new_information:
        new_contact = Contact(phoneNumber=phone_number, email=email, linkedId=primary_contact.id, linkPrecedence='secondary')
        new_contact.save()
        return new_contact

    return primary_contact

def consolidate_contact(contact):
    primary_contact_id = contact.id if contact.linkPrecedence == 'primary' else contact.linkedId
    all_contacts = Contact.objects.filter(
        models.Q(id=primary_contact_id) | models.Q(linkedId=primary_contact_id),
        deletedAt__isnull=True
    )

    primary_contact = all_contacts.get(id=primary_contact_id)
    emails = [primary_contact.email] + [c.email for c in all_contacts if c.email and c.email != primary_contact.email]
    phone_numbers = [primary_contact.phoneNumber] + [c.phoneNumber for c in all_contacts if c.phoneNumber and c.phoneNumber != primary_contact.phoneNumber]
    secondary_contact_ids = [c.id for c in all_contacts if c.id != primary_contact_id]

    return {
        "primaryContactId": primary_contact_id,
        "emails": emails,
        "phoneNumbers": phone_numbers,
        "secondaryContactIds": secondary_contact_ids
    }
