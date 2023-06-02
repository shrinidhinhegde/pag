from django.contrib import admin
from .models import ContactUsQuery, Organisation, UserExtend, Invoice, Document, Renewal, Service, Message, \
    Notification, QrCode, UploadDocument, SubOrganisation


class ContactUsQueryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'organisation', 'date_and_time']


class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name_of_mission', 'entity', 'email']


class UserExtendAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'organisation', 'issue_date', 'due_date', 'paid', 'amount']


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'jurisdiction', 'created', 'type_of_doc', 'status']


class RenewalAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'description', 'received_date', 'due_date']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'type_of_service', 'start_of_service', 'end_of_service', 'jurisdiction', 'product',
                    'cancel_status']


class MessageAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'date']


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_title', 'date']


class QrCodeAdmin(admin.ModelAdmin):
    list_display = ['organisation']


class UploadDocumentAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'jurisdiction', 'created', 'type_of_doc']


class SubOrganisationAdmin(admin.ModelAdmin):
    list_display = ['organisation', 'name', 'entity']


admin.site.register(ContactUsQuery, ContactUsQueryAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(UserExtend, UserExtendAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Renewal, RenewalAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(QrCode, QrCodeAdmin)
admin.site.register(UploadDocument, UploadDocumentAdmin)
admin.site.register(SubOrganisation, SubOrganisationAdmin)
