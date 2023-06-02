import random
import string
import urllib.parse

import requests
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ContactUsQuery(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    date_and_time = models.DateTimeField(null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    organisation = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(max_length=5000, blank=True, null=True)


class Organisation(models.Model):
    name_of_mission = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address_1 = models.CharField(max_length=200, blank=True, null=True)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    entity = models.CharField(max_length=100, blank=True, null=True)
    read_notification = models.BooleanField(default=True)

    def __str__(self):
        return self.name_of_mission


class SubOrganisation(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    address_1 = models.CharField(max_length=200, blank=True, null=True)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    entity = models.CharField(max_length=100, blank=True, null=True)


class UserExtend(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    organisation = models.ManyToManyField(to=Organisation, related_name='+')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    admin_access = models.BooleanField(default=False)
    account_type = models.CharField(max_length=100, blank=True, null=True)


class Invoice(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(auto_now=True)
    due_date = models.DateField(null=True)
    paid = models.BooleanField(default=False)
    amount = models.FloatField(null=True, blank=True)
    file = models.FileField(upload_to='Invoices', null=True, blank=True)
    sharing = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            message = "New Invoice " + self.invoice_number + " is added to your organisation of amount "\
                      + str(self.amount) + " on " + str(timezone.localdate())
            Message.objects.create(organisation=self.organisation, message=message)
            # send email for the same
        super(Invoice, self).save(*args, **kwargs)


class Document(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    jurisdiction = models.CharField(max_length=100, blank=True, null=True)
    type_of_doc = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateField(auto_now=True)
    status = models.BooleanField(default=False)
    file = models.FileField(upload_to='Documents', null=True, blank=True)
    sharing = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            message = "New Document is added to your organisation under "+self.jurisdiction+" jurisdiction on "\
                      + str(timezone.localdate())
            Message.objects.create(organisation=self.organisation, message=message)
            # send email for the same
        super(Document, self).save(*args, **kwargs)


class UploadDocument(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    created = models.DateField(auto_now=True)
    jurisdiction = models.CharField(max_length=100, blank=True, null=True)
    type_of_doc = models.CharField(max_length=100, blank=True, null=True)
    file = models.FileField(upload_to='Documents', null=True, blank=True)


class Renewal(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    description = models.CharField(max_length=500, blank=True, null=True)
    received_date = models.DateField(auto_now=True)
    due_date = models.DateField(null=True)


class Service(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    type_of_service = models.CharField(max_length=500, blank=True, null=True)
    start_of_service = models.DateField(null=True)
    end_of_service = models.DateField(null=True)
    product = models.CharField(max_length=500, blank=True, null=True)
    jurisdiction = models.CharField(max_length=200, blank=True, null=True)
    cancel_status = models.BooleanField(default=False)


class Message(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    new = models.BooleanField(default=True)


class Notification(models.Model):
    organisation = models.ManyToManyField(Organisation)
    notification_title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(auto_now=True)
    message = models.TextField(max_length=5000)

    def save(self, *args, **kwargs):
        if self.pk:
            for org in self.organisation.values_list():
                x = Organisation.objects.get(id=org[0])
                x.read_notification = True
                x.save()
        super(Notification, self).save(*args, **kwargs)


class QrCode(models.Model):
    organisation = models.ForeignKey(to=Organisation, on_delete=models.CASCADE)
    image = models.CharField(max_length=5000, null=True, blank=True)
    gibberish = models.CharField(max_length=20, null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        gibberish = ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))
        self.gibberish = gibberish
        if self.link is None:
            l = "https://compliance.pagric.com"
        else:
            l = self.link
        link = l + 'sharing/' + gibberish + '/' + str(self.organisation)
        link = urllib.parse.quote(link, safe='')
        self.image = link
        super(QrCode, self).save(*args, **kwargs)
