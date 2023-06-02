from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import PasswordChangeForm, OrgDetailForm, UserExtendForm, UploadDocumentForm, SubOrgDetailForm
from .models import ContactUsQuery, Organisation, UserExtend, Invoice, Document, Renewal, Service, \
    Message, Notification, QrCode, UploadDocument, SubOrganisation


def landingview(request):
    context = {

    }
    return render(request, 'index.html', context)

datetime_object = datetime.strptime("7/15/2022", "%m/%d/%Y")


@login_required(login_url='login')
def dashboardview(request):
    orgsdetail = UserExtend.objects.get(user=request.user).organisation.values_list()
    orgs = []
    alert = None
    msg_no = 0
    invoice_no = 0
    docs_no = 0
    renewal_no = 0
    for org in orgsdetail:
        if str(org[11]) == "True":
            alert = True
        orgs.append(org[0])
    qr = QrCode.objects.filter(organisation__in=orgs)
    for org in orgs:
        message = Message.objects.filter(organisation=org, new=True)
        invoice = Invoice.objects.filter(organisation=org, paid=False)
        document = Document.objects.filter(organisation=org, status=False)
        renewal = Renewal.objects.filter(organisation=org)
        for x in renewal:
            if x.due_date < datetime_object:
                renewal_no += 1
        invoice_no += len(invoice)
        msg_no += len(message)
        docs_no += len(document)
    if msg_no > 0:
        message = True
    else:
        message = False
    if invoice_no > 0:
        invoice = True
    else:
        invoice = False
    if docs_no > 0:
        document = True
    else:
        document = False
    if renewal_no > 0:
        renewal = True
    else:
        renewal = False
    context = {
        'alert': alert,
        'message': message,
        'invoice': invoice,
        'document': document,
        'renewal': renewal,
        'message_no': msg_no,
        'invoice_no': invoice_no,
        'document_no': docs_no,
        'renewal_no': renewal_no,
        'qrs': qr,
        's': True
    }
    return render(request, 'dashboard.html', context)


def loginview(request):
    msg = None
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('UserName')
            password = request.POST.get('Password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboardview')
            else:
                msg = 'UserName or Password Incorrect'
        context = {
            'msg': msg,
        }
        return render(request, 'account/login.html', context)
    else:
        return redirect('landingview')


def contactusview(request):
    msg = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('Phone')
        org = request.POST.get('Organisation')
        message = request.POST.get('Message')
        date_and_time = timezone.now()
        ContactUsQuery.objects.create(name=name, email=email, phone=phone, organisation=org, message=message,
                                      date_and_time=date_and_time)
        msg = 'Thank you! Your submission has been received! We will contact you shortly.'

        send_mail(
            'Your submission has been received!',
            'Thank you! Your submission has been received! We will contact you shortly.',
            settings.EMAIL_HOST_USER,
            [email, ],
            fail_silently=True,
            # html_message=None,
        )
        send_mail(
            'New Query on DiplomaticXpress',
            'Name: ' + name + '\nEmail: ' + email + '\nPhone: ' + phone + '\nOrganisation: ' + org + '\nMessage: ' + message + '\nDate and Time: ' + str(
                date_and_time),
            settings.EMAIL_HOST_USER,
            ['shrinidhi.hegde@sync.energy', ],
            fail_silently=True,
            # html_message=None,
        )
    context = {
        'msg': msg
    }
    return render(request, 'contactus.html', context)


def logoutview(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('landingview')
    else:
        return redirect('landingview')


@login_required(login_url='login')
def changepasswordview(request):
    msg = None
    success = None
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            msg = 'Password Changed Successfully!'
            success = True
            # return redirect('landingview')
        else:
            msg = 'Form is not Valid'
    else:
        form = PasswordChangeForm(user=request.user)
    context = {
        'form': form,
        'msg': msg,
        'success': success
    }
    return render(request, 'account/changepassword.html', context)


@login_required(login_url='login')
def myorgview(request):
    org_listx = []
    org_list = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[1])
    for org in org_listx:
        org_list.append(Organisation.objects.get(name_of_mission=str(org)))
    context = {
        'org_list': org_list
    }
    return render(request, 'pages/myorganisations.html', context)


@login_required(login_url='login')
def myorgdetailview(request, active, name):
    c = 0
    my_org = UserExtend.objects.get(user=request.user)
    admin = my_org.admin_access
    if True:
        for org in my_org.organisation.values_list():
            if name == str(org[1]):
                c = 1
                break
    if c == 0:
        return redirect('myorganisations')

    org = Organisation.objects.get(name_of_mission=name)
    users = UserExtend.objects.filter(organisation__in=[org.id])
    suborg = SubOrganisation.objects.filter(organisation=org)
    context = {
        'org': org,
        'users': users,
        'active': active,
        'admin': admin,
        'suborgs': suborg
    }
    return render(request, 'pages/myorganisations-detail.html', context)


@login_required(login_url='login')
def orgeditview(request, name):
    c = 0
    msg = None
    success = None
    my_org = UserExtend.objects.get(user=request.user)
    if my_org.admin_access:
        if True:
            for org in my_org.organisation.values_list():
                if name == str(org[1]):
                    c = 1
                    break
        if c == 0:
            return redirect('myorganisations')

        if request.method == 'POST':
            form = OrgDetailForm(data=request.POST, instance=Organisation.objects.get(name_of_mission=name))
            if form.is_valid():
                form.save()
                msg = "The details are updated!"
                success = True
            else:
                msg = "The form is invalid."
        form = OrgDetailForm(instance=Organisation.objects.get(name_of_mission=name))
        context = {
            'name': name,
            'form': form,
            'msg': msg,
            'success': success,
        }
        return render(request, 'pages/myorganisations-org-edit.html', context)
    else:
        return redirect('myorganisations')


@login_required(login_url='login')
def orgusereditview(request, id, name):
    msg = None
    success = None
    curr_user = UserExtend.objects.get(user=request.user)
    l1 = []
    l2 = []
    for x in curr_user.organisation.values_list():
        l1.append(x[1])
    id_user = UserExtend.objects.get(id=id)
    for x in id_user.organisation.values_list():
        l2.append(x[1])
    if curr_user.id == id:
        if request.method == 'POST':
            form = UserExtendForm(data=request.POST, instance=UserExtend.objects.get(id=id))
            if form.is_valid():
                form.save()
                request.user.email = form.cleaned_data.get('email')
                request.user.save()
                msg = "The details are updated!"
                success = True
            else:
                msg = "The form is invalid."
        form = UserExtendForm(instance=UserExtend.objects.get(id=id))
        context = {
            'form': form,
            'admin': curr_user.admin_access,
            'msg': msg,
            'success': success,
            'name': name
        }
        return render(request, 'pages/myorganisations-user-edit.html', context)
    elif (set(l1) & set(l2)) and curr_user.admin_access:
        if request.method == 'POST':
            form = UserExtendForm(data=request.POST, instance=UserExtend.objects.get(id=id))
            if form.is_valid():
                form.save()
                request.user.email = form.cleaned_data.get('email')
                request.user.save()
                msg = "The details are updated!"
                success = True
            else:
                msg = "The form is invalid."
        form = UserExtendForm(instance=UserExtend.objects.get(id=id))
        context = {
            'form': form,
            'admin': curr_user.admin_access,
            'msg': msg,
            'success': success,
            'name': name
        }
        return render(request, 'pages/myorganisations-user-edit.html', context)
    else:
        return redirect('myorganisations')


@login_required(login_url='login')
def invoiceview(request, active):
    org_listx = []
    invoice_list = []
    invoice_list_share = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[0])
    for org in org_listx:
        invoice_list.append(Invoice.objects.filter(organisation=org))
        invoice_list_share.append(Invoice.objects.filter(organisation=org, sharing=True))
    context = {
        'active': active,
        'invoice_list': invoice_list,
        'invoice_list_share': invoice_list_share
    }
    return render(request, 'pages/invoices.html', context)


@login_required(login_url='login')
def documentview(request, active):
    org_listx = []
    document_list = []
    document_list_sharing = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[0])
    for org in org_listx:
        document_list.append(Document.objects.filter(organisation=org))
        document_list_sharing.append(Document.objects.filter(organisation=org, sharing=True))
    context = {
        'active': active,
        'document_list': document_list,
        'document_list_sharing': document_list_sharing
    }
    return render(request, 'pages/documents.html', context)


@login_required(login_url='login')
def documentsee(request, id):
    try:
        doc = Document.objects.get(id=id)
    except:
        return redirect('documentview', active=1)
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        context = {
            'doc': doc
        }
        doc.status = True
        doc.save()
        return render(request, 'pages/documentsee.html', context)
    else:
        return redirect('documentview', active=1)


@login_required(login_url='login')
def documentshare(request, id):
    try:
        doc = Document.objects.get(id=id)
    except:
        return redirect('documentview', active=1)
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        doc.sharing = True
        doc.save()
        return redirect('documentview', active=2)
    else:
        return redirect('documentview', active=1)


@login_required(login_url='login')
def documentsharestop(request, id):
    try:
        doc = Document.objects.get(id=id)
    except:
        return redirect('documentview', active=1)
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        doc.sharing = False
        doc.save()
        return redirect('documentview', active=2)
    else:
        return redirect('documentview', active=1)


@login_required(login_url='login')
def invoicesee(request, id):
    try:
        invoice = Invoice.objects.get(id=id)
    except:
        return redirect('invoiceview', active=1)
    l1 = [str(invoice.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        context = {
            'invoice': invoice
        }
        return render(request, 'pages/invoicesee.html', context)
    else:
        return redirect('invoiceview', active=1)


@login_required(login_url='login')
def invoiceshare(request, id):
    try:
        doc = Invoice.objects.get(id=id)
    except:
        return redirect('invoiceview', active=1)
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        doc.sharing = True
        doc.save()
        return redirect('invoiceview', active=2)
    else:
        return redirect('invoiceview', active=1)


@login_required(login_url='login')
def invoicesharestop(request, id):
    try:
        doc = Invoice.objects.get(id=id)
    except:
        return redirect('invoiceview', active=1)
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        doc.sharing = False
        doc.save()
        return redirect('invoiceview', active=2)
    else:
        return redirect('invoiceview', active=1)


@login_required(login_url='login')
def renewalsview(request, active):
    org_listx = []
    renewal_list = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[0])
    for org in org_listx:
        renewal_list.append(Renewal.objects.filter(organisation=org))
    context = {
        'active': active,
        'renewal_list': renewal_list,
        'today': datetime_object,
    }
    return render(request, 'pages/renewals.html', context)


@login_required(login_url='login')
def serviceview(request, active):
    org_listx = []
    service_organisation = []
    service_number = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[0])
    for org in org_listx:
        organ = Service.objects.filter(organisation=org)
        service_organisation.append(Organisation.objects.get(id=org).name_of_mission)
        service_number.append(len(organ))
    service_list = zip(service_organisation, service_number)
    context = {
        'active': active,
        'service_list': service_list
    }
    return render(request, 'pages/services.html', context)


@login_required(login_url='login')
def servicedetailview(request, active, name):
    c = 0
    my_org = UserExtend.objects.get(user=request.user)
    if True:
        for org in my_org.organisation.values_list():
            if name == str(org[1]):
                c = 1
                break
    if c == 0:
        return redirect('serviceview', active=1)

    org = Organisation.objects.get(name_of_mission=name)
    services = Service.objects.filter(organisation__in=[org.id])
    active_services = []
    inactive_service = []
    for service in services:
        if service.cancel_status:
            inactive_service.append(service)
        else:
            active_services.append(service)
    context = {
        'name': name,
        'active_service': active_services,
        'inactive_service': inactive_service,
        'active': active,
    }
    return render(request, 'pages/servicedetail.html', context)


@login_required(login_url='login')
def servicecancelview(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        service = Service.objects.get(id=id)
        service.cancel_status = True
        service.save()
        return redirect('servicedetailview', active=2, name=name)
    else:
        return redirect('serviceview', active=2)


@login_required(login_url='login')
def alertview(request):
    orgsdetail = UserExtend.objects.get(user=request.user).organisation.values_list()
    orgs = []
    for org in orgsdetail:
        orgs.append(org[0])
        x = Organisation.objects.get(id=org[0])
        x.read_notification = False
        x.save()
    notification = Notification.objects.filter(organisation__in=orgs).distinct()
    context = {
        'notifications': notification,
    }
    return render(request, 'pages/alerts.html', context)


@login_required(login_url='login')
def messageview(request):
    orgsdetail = UserExtend.objects.get(user=request.user).organisation.values_list()
    orgs = []
    for org in orgsdetail:
        orgs.append(org[0])
    message = Message.objects.filter(organisation__in=orgs)
    for mess in message:
        mess.new = False
        mess.save()
    context = {
        'messages': message,
    }
    return render(request, 'pages/messages.html', context)


@login_required(login_url='login')
def sharingsave(request):
    if request.method == 'POST':
        org = Organisation.objects.get(name_of_mission=request.POST.get('organisation'))
        orgsdetail = UserExtend.objects.get(user=request.user, organisation=org.id)
        if orgsdetail:
            qr = QrCode.objects.get(organisation=org.id)
            qr.link = str(request.get_raw_uri())[:-14]
            qr.save()
            return redirect('dashboardview')
        else:
            return redirect('dashboardview')
    else:
        return redirect('dashboardview')


def sharingview(request, hash, name):
    try:
        org = Organisation.objects.get(name_of_mission=name)
    except:
        return redirect('landingview')
    try:
        data = QrCode.objects.get(organisation=org.id, gibberish=hash)
    except:
        return redirect('landingview')
    if data:
        documents = Document.objects.filter(organisation=org.id, sharing=True)
        invoices = Invoice.objects.filter(organisation=org.id, sharing=True)

    for document in documents:
        print(document)
    context = {
        'documents': documents,
        'invoices': invoices,
        'hash': hash,
        'name': name,
    }
    return render(request, 'sharing.html', context)


def documentseesharing(request, id, hash, name):
    try:
        org = Organisation.objects.get(name_of_mission=name)
    except:
        return redirect('landingview')
    try:
        data = QrCode.objects.get(organisation=org.id, gibberish=hash)
    except:
        return redirect('landingview')
    if data:
        document = Document.objects.get(id=id)
        context = {
            'file': document,
            'hash': hash,
            'name': name,
        }
        return render(request, 'pages/filesharing.html', context)
    else:
        return redirect('landingview')


def invoiceseesharing(request, id, hash, name):
    try:
        org = Organisation.objects.get(name_of_mission=name)
    except:
        return redirect('landingview')
    try:
        data = QrCode.objects.get(organisation=org.id, gibberish=hash)
    except:
        return redirect('landingview')
    if data:
        document = Invoice.objects.get(id=id)
        context = {
            'file': document,
            'hash': hash,
            'name': name,
        }
        return render(request, 'pages/filesharing.html', context)
    else:
        return redirect('landingview')


@login_required(login_url='login')
def depository(request):
    org_listx = []
    document_list = []
    document_list_sharing = []
    my_org = UserExtend.objects.get(user=request.user)
    for org in my_org.organisation.values_list():
        org_listx.append(org[0])
    for org in org_listx:
        document_list.append(UploadDocument.objects.filter(organisation=org))
    context = {
        'document_list': document_list,
    }
    return render(request, 'pages/depository.html', context)


@login_required(login_url='login')
def depositoryview(request, id):
    try:
        doc = UploadDocument.objects.get(id=id)
    except:
        return redirect('depository')
    l1 = [str(doc.organisation)]
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user)
    for x in curr_user.organisation.values_list():
        l2.append(x[1])
    if (set(l1) & set(l2)):
        context = {
            'doc': doc
        }
        doc.status = True
        doc.save()
        return render(request, 'pages/depositorysee.html', context)
    else:
        return redirect('depository')


@login_required(login_url='login')
def depositorydelete(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        try:
            doc = UploadDocument.objects.get(id=id)
        except:
            doc = None
        if doc:
            doc.delete()
        return redirect('depository')
    else:
        return redirect('depository')


@login_required(login_url='login')
def uploaddoc(request):
    success = None
    l2 = []
    curr_user = UserExtend.objects.get(user=request.user).organisation.values_list()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            org = request.POST.get('org')
            orgid = Organisation.objects.get(name_of_mission=org)
            sayyve = form.save(commit=False)
            sayyve.organisation = orgid
            sayyve.save()
            success = True
        else:
            return redirect('depository')
    else:
        form = UploadDocumentForm()

    for x in curr_user:
        l2.append(x[1])
    context = {
        'form': form,
        'success': success,
        'options': l2
    }
    return render(request, 'pages/uploaddoc.html', context)


@login_required(login_url='login')
def suborgeditview(request, name, nname):
    msg = None
    success = None
    my_org = UserExtend.objects.get(user=request.user)
    if my_org.admin_access:
        org = SubOrganisation.objects.get(name=name)
        x = UserExtend.objects.get(user=request.user, organisation=org.organisation)
        if x != my_org:
            return redirect('myorganisations')

        if request.method == 'POST':
            form = SubOrgDetailForm(data=request.POST, instance=SubOrganisation.objects.get(name=name))
            if form.is_valid():
                form.save()
                msg = "The details are updated!"
                success = True
            else:
                msg = "The form is invalid."
        form = SubOrgDetailForm(instance=SubOrganisation.objects.get(name=name))
        context = {
            'name': nname,
            'form': form,
            'msg': msg,
            'success': success,
        }
        return render(request, 'pages/myorganisations-sub-org-edit.html', context)
    else:
        return redirect('myorganisations')