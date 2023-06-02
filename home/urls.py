from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .forms import PasswordResetform, PasswordResetConfirm
from .views import landingview, loginview, contactusview, logoutview, changepasswordview, dashboardview, myorgview, \
    myorgdetailview, orgeditview, orgusereditview, invoiceview, documentview, documentsee, invoicesee, renewalsview, \
    serviceview, servicedetailview, servicecancelview, alertview, messageview, sharingsave, sharingview, documentshare, \
    documentsharestop, invoiceshare, invoicesharestop, documentseesharing, invoiceseesharing, depository, \
    depositoryview, depositorydelete, uploaddoc, suborgeditview
import django.contrib.auth.views as auth_views

urlpatterns = [
    path('', landingview, name='landingview'),
    path('dashboard/', dashboardview, name='dashboardview'),
    path('login/', loginview, name='login'),
    path('contactus/', contactusview, name='contactus'),
    path('logout/', logoutview, name='logoutview'),
    path('reset/', auth_views.PasswordResetView.as_view(template_name='account/password_reset.html', form_class= PasswordResetform), name='reset'),
    path('reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='account/reset_done.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='account/reset_confirm.html', form_class= PasswordResetConfirm), name='password_reset_confirm'),
    path("reset/complete", auth_views.PasswordResetCompleteView.as_view(template_name='account/reset_complete.html'), name='password_reset_complete'),
    path('change-password/', changepasswordview, name='changepasswordview'),

    path('myorganisations/', myorgview, name='myorganisations'),
    path('myorganisations/<int:active>/<str:name>', myorgdetailview, name='orgdetailview'),
    path('organisation-edit/<str:name>', orgeditview, name='orgedit'),
    path('suborganisation-edit/<str:name>/<str:nname>', suborgeditview, name='suborgedit'),
    path('organisation-user-edit/<int:id>/<str:name>', orgusereditview, name='orguseredit'),

    path('invoices/<int:active>', invoiceview, name='invoiceview'),
    path('invoices/view/<int:id>', invoicesee, name='invoicesee'),
    path('invoiceshare/<int:id>', invoiceshare, name='invoiceshare'),
    path('invoicesharestop/<int:id>', invoicesharestop, name='invoicesharestop'),

    path('documents/<int:active>', documentview, name='documentview'),
    path('documents/view/<int:id>', documentsee, name='documentsee'),
    path('documentshare/<int:id>', documentshare, name='documentshare'),
    path('documentsharestop/<int:id>', documentsharestop, name='documentsharestop'),

    path('renewables/<int:active>', renewalsview, name='renewalsview'),

    path('services/<int:active>', serviceview, name='serviceview'),
    path('services/<int:active>/<str:name>', servicedetailview, name='servicedetailview'),
    path('service-cancel', servicecancelview, name='servicecancelview'),

    path('depository', depository, name='depository'),
    path('depositoryview/<int:id>', depositoryview, name='depositorysee'),
    path('depositorydel', depositorydelete, name='depositorydelete'),
    path('uploaddoc/', uploaddoc, name='uploaddoc'),

    path('alerts/', alertview, name='alertview'),
    path('messages/', messageview, name='messageview'),

    path('sharing-reset/', sharingsave, name='sharingsave'),
    path('sharing/<str:hash>/<str:name>', sharingview, name='sharingview'),
    path('shareddocuments/view/<int:id>/<str:hash>/<str:name>', documentseesharing, name='documentsee-sharing'),
    path('sharedinvoices/view/<int:id>/<str:hash>/<str:name>', invoiceseesharing, name='invoicesee-sharing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

