from django.db import models
from django.utils import timezone

class Contact(models.Model):
    phoneNumber = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedId = models.IntegerField(null=True, blank=True)
    linkPrecedence = models.CharField(max_length=10, choices=[('primary', 'primary'), ('secondary', 'secondary')])
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.createdAt = timezone.now()
        self.updatedAt = timezone.now()
        super(Contact, self).save(*args, **kwargs)
