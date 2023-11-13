from os import dup
from django.db.models.base import Model
from .services import ExternalService
from django.db.models import fields
from rest_framework import serializers
from .models import Invoice, Payment, PaymentCard, PaymentTransfer, PaymentTransferManual, Setting
import os
from datetime import datetime, timedelta, date

class InvoiceSerializer(serializers.ModelSerializer):
    order_summary = serializers.SerializerMethodField('get_project')
    total_summary = serializers.SerializerMethodField('get_total_summary')
    payment_type = serializers.SerializerMethodField('get_type')
   
    def get_project(self, obj):
        plan = 'starter'
        if obj.plan != None :
            plan = str(obj.plan)
        
        det_package = "Paket "+ plan.capitalize() +"  - Yearly"
        harga = Setting.objects.filter(name='yearly', type='user', plan=plan)
        price = harga[0].priceuser

        if obj.package == 'quarterly' :
            det_package = "Paket "+ plan.capitalize() +"  - Quarterly"
            harga = Setting.objects.filter(name='quarterly', type='user', plan=plan)
            price = harga[0].priceuser
        
        total_onboard = 0
        price_onboard = 0
        if(obj.on_boarding_service == True):
            total_onboard = 1
            price_onboard = 5000000

        user = obj.total_user

        data = [
            {
                "detail": det_package,
                "qty": user,
                "price": price,
                "total": obj.total_price_user
            },
            {
                "detail": "On Boarding service",
                "qty": total_onboard,
                "price": price_onboard,
                "total": price_onboard
            }
        ]
            
        return data
    
    def get_total_summary(self, obj):
        try : 
            mount = int(obj.total_amount)
            data =  {
                "sub_total": obj.sub_total,
                "tax": obj.tax,
                "total_amount": obj.total_amount,
                "unique" : int(str(mount)[-3:])
            }
        except:
            data = {
                "sub_total": 0,
                "tax": 0,
                "total_amount": 0,
                "unique" : 0
            }
            
        return data

    def get_type(self, obj):
        manual = PaymentTransferManual.objects.filter(invoice=obj.id).count()
        if manual > 0:
            return 'manual'
        else :
            return 'automatic'

    class Meta:
        model = Invoice
        fields = '__all__'

class InvoicesSerializer(serializers.ModelSerializer):
    # order_summary = serializers.SerializerMethodField('get_project')
    # total_summary = serializers.SerializerMethodField('get_total_summary')
   
    def get_project(self, obj):
        plan = 'starter'
        if obj.plan != None :
            plan = str(obj.plan)
        
        det_package = "Paket "+ plan.capitalize() +"  - Yearly"
        harga = Setting.objects.filter(name='yearly', type='user', plan=plan)
        price = harga[0].priceuser

        if obj.package == 'quarterly' :
            det_package = "Paket "+ plan.capitalize() +"  - Quarterly"
            harga = Setting.objects.filter(name='quarterly', type='user', plan=plan)
            price = harga[0].priceuser
        
        total_onboard = 0
        price_onboard = 0
        if(obj.on_boarding_service == True):
            total_onboard = 1
            price_onboard = 5000000

        user = obj.total_user

        data = [
            {
                "detail": det_package,
                "qty": user,
                "price": price,
                "total": obj.total_price_user
            },
            {
                "detail": "On Boarding service",
                "qty": total_onboard,
                "price": price_onboard,
                "total": price_onboard
            }
        ]
            
        return data
    
    def get_total_summary(self, obj):

        data =  {"total_summary": {
            "sub_total": obj.sub_total,
            "tax": obj.tax,
            "total_amount": obj.total_amount
        }}
            
        return data

    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceHistorySerializer(serializers.ModelSerializer):
    order_summary = serializers.SerializerMethodField('get_project')
    total_summary = serializers.SerializerMethodField('get_total_summary')
    payment = serializers.SerializerMethodField('get_payment')
    customer_detail = serializers.SerializerMethodField('get_customer_detail')

    def get_project(self, obj):
        plan = 'starter'
        if obj.plan != None :
            plan = str(obj.plan)
        
        det_package = "Paket "+ plan.capitalize() +"  - Yearly"
        harga = Setting.objects.filter(name='yearly', type='user', plan=plan)
        price = harga[0].priceuser

        if obj.package == 'quarterly' :
            det_package = "Paket "+ plan.capitalize() +"  - Quarterly"
            harga = Setting.objects.filter(name='quarterly', type='user', plan=plan)
            price = harga[0].priceuser
        
        total_onboard = 0
        price_onboard = 0
        if(obj.on_boarding_service == True):
            total_onboard = 1
            price_onboard = 5000000

        user = obj.total_user

        data = [
            {
                "detail": det_package,
                "qty": user,
                "price": price,
                "total": obj.total_price_user
            },
            {
                "detail": "On Boarding service",
                "qty": total_onboard,
                "price": price_onboard,
                "total": price_onboard
            }
        ]
            
        return data
    
    def get_total_summary(self, obj):

        data =  {
            "sub_total": obj.sub_total,
            "tax": obj.tax,
            "total_amount": obj.total_amount
        }
            
        return data

    def img(self, bank):
        img = ''
        if(bank == 'bca'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/ccb8ea59-9cf4-4ca0-a2bf-c6caccb0619a.png'
        elif (bank == 'bni'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/3a9855a3-8f3a-403e-bacc-89f485d3a061.png'
        elif (bank == 'mandiri'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/aa12bc89-a647-4ff8-8d93-c2f1fb8dd696.png'

        return img

    def get_payment(self, obj):
       
        a = {
            "type" : "Bank Transfer",
            "bank" : "bca",
            "detail" : '***********',
            "total_amount": '-',
            "name" : '-',
            "account_number": '-',
            "picture" : ''
        }
        detail = PaymentTransfer.objects.filter(accountId=obj.accountId, invoice=obj.id)

        if(list(detail) != []) :
            detail = PaymentTransfer.objects.filter(accountId=obj.accountId, invoice=obj.id).values().latest('createdAt')
            a = {
                "type" : "Bank Transfer Automatic",
                "bank" : detail['bank'],
                "detail" : detail['virtual_account'],
                "total_amount": '-',
                "name" : '-',
                "account_number": '-',
                "picture" : self.img(bank=detail['bank'])
            }
        else :
            try : 
                detailc = PaymentCard.objects.filter(accountId=obj.accountId, invoice=obj.id).values('total_amount', 'first_name', 'card_number', 'bank', 'brand').latest('id')

                pict = ''
                if detailc['brand'] == 'VISA' :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/c6f24f5b-4106-407d-b24f-5c2331df0039.png'
                elif detailc['brand'] == 'MASTERCARD' :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/b109dc02-d390-41ff-b46d-745badbe93f3.png'
                else :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/029b5d41-f6a1-4b94-a783-a9e66f0968d7.png'
            
                a = {
                    "type" : "Card Credit" + str(detailc['bank']),
                    "bank" : detailc['bank'],
                    "detail" : detailc['card_number'],
                    "total_amount": detailc['total_amount'],
                    "name" : detailc['first_name'],
                    "account_number": '-',
                    "picture" : pict
                }
            except :
                a = {
                    "type" : "Card Credit",
                    "bank" : "bca",
                    "detail" : '***********',
                    "total_amount": '-',
                    "name" : '-',
                    "account_number": '-',
                    "picture" : ''
                }
        detailmanual = PaymentTransferManual.objects.filter(accountId=obj.accountId, invoice=obj.id).count()

        if(detailmanual > 0) :
            detail = Setting.objects.filter(name='manual', bank='bca').values('bank_account_name', 'bank_account_number', 'picture')
            a = {
                "type" : "Bank Transfer Manual",
                "bank" : 'bca',
                "total_amount": obj.total_amount,
                "name" : detail[0]['bank_account_name'],
                "account_number": detail[0]['bank_account_number'],
                "picture" : detail[0]['picture']
            }
                
        return a

    def get_customer_detail(self, obj):

        b = {
            "bank_account_name": '-',
            "bank_account_number": '-',
            "proof_picture" : ''
        }
        detailmanual = PaymentTransferManual.objects.filter(accountId=obj.accountId, invoice=obj.id)
        if detailmanual.count() > 0:
            b = {
                "bank_account_name": list(detailmanual.order_by('-createdAt').values_list('bank_account_name', flat=True))[0],
                "bank_account_number": list(detailmanual.order_by('-createdAt').values_list('bank_account_number', flat=True))[0],
                "proof_picture": list(detailmanual.order_by('-createdAt').values_list('proof', flat=True))[0]
            }
        return b

    class Meta:
        model = Invoice
        fields = '__all__'

class CekInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'accountId', 'expired_date']

class PaymentTransferSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField('get_payment_detail')

    def get_payment_detail(self, obj):
        detail = Setting.objects.filter(type='bank', bank=obj.bank).values('bank_account_name', 'bank_account_number', 'picture')
        a = {
            "type" : "Bank Transfer Automatic",
            "bank" : obj.bank,
            "total_amount": obj.total_amount,
            "name" : '',
            "account_number": '',
            "picture" : detail[0]['picture']
        }
        
        return a

    class Meta:
        model = PaymentTransfer
        fields = '__all__'

class PaymentCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentCard
        fields = '__all__'

class PaymentTransferManualSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField('get_payment_detail')

    def get_payment_detail(self, obj):
        detail = Setting.objects.filter(name='manual', bank=obj.bank).values('bank_account_name', 'bank_account_number', 'picture')

        a = {
            "type" : "Bank Transfer Manual",
            "bank" : obj.bank,
            "total_amount": obj.total_amount,
            "name" : detail[0]['bank_account_name'],
            "account_number": detail[0]['bank_account_number'],
            "picture" : detail[0]['picture']
        }
        
        return a
    
    class Meta:
        model = PaymentTransferManual
        fields = '__all__'

class BillingSerializer(serializers.ModelSerializer):
    price_per_user = serializers.SerializerMethodField('get_price')
    package_type = serializers.SerializerMethodField('get_project')
    next_bill = serializers.SerializerMethodField('get_next_bill')
    leads = serializers.SerializerMethodField('get_quota')
    payment_detail = serializers.SerializerMethodField('get_payment_detail')
   
    def get_project(self, obj):
        plan = 'starter'
        if obj.plan != None :
            plan = str(obj.plan).capitalize()

        if obj.package == 'quarterly' :
            return 'Package '+ plan +' - Quarterly'
        elif obj.package == 'yearly' :
            return 'Package '+ plan +' - Yearly'
        else :
            return obj.package
    
    def get_price(self, obj):
        plan = 'starter'
        if obj.plan != None :
            plan = str(obj.plan)
        if obj.package == 'quarterly' :
            harga = Setting.objects.filter(name='quarterly', type='user', plan=plan)
            return harga[0].priceuser
        elif obj.package == 'yearly' :
            harga = Setting.objects.filter(name='yearly', type='user', plan=plan)
            return harga[0].priceuser
        else :
            return 0

    def get_next_bill(self, obj):
        if obj.payment_status == 'paid':
            invoiceawal = Invoice.objects.filter(accountId=obj.accountId, payment_status='paid', status='running').order_by('-id')
            tanggalawal = Invoice.objects.filter(accountId=obj.accountId, payment_status='paid', status='running').order_by('id')[:1]

            if obj.package == 'quarterly' :
                if invoiceawal.count() > 0:
                    hari = 0
                    for a in invoiceawal:
                        if a.package == 'quarterly':
                            hari += 90
                        else :
                            hari += 365
                    dates = tanggalawal[0].createdAt + timedelta(days=hari)
                else :
                    dates  = obj.createdAt + timedelta(days=90)

            elif obj.package == 'yearly' :
                if invoiceawal.count() > 0:
                    hari = 0
                    for a in invoiceawal:
                        if a.package == 'quarterly':
                            hari += 90
                        else :
                            hari += 365
                    dates = tanggalawal[0].createdAt + timedelta(days=hari)
                else :
                    dates = obj.createdAt + timedelta(days=365)
        else :
            dates = '-'

        return dates
    
    def get_quota(self, obj):
        remaiaining = 5000
        quota = 5000
        total = 0
        if obj.package not in ['quarterly','yearly']:
            data = {
                "quota" : '-',
                "remaining" : '-'
            }
        else :
            request_object = self.context['request']
            invoker_id = request_object.query_params.get('invoker_id')
            user_id = request_object.query_params.get('user_id')
            usr = None
            if invoker_id != None:
                usr = invoker_id
            if user_id != None:
                usr = user_id
            
            total = ExternalService().total_lead(obj.accountId, usr)
            if(total != None):
                if(total <= 5000) :
                    remaiaining = int(quota) - int(total)

            data = {
                "quota" : quota,
                "remaining" : remaiaining
            }
        return data

    def img(self, bank):
        img = ''
        if(bank == 'bca'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/ccb8ea59-9cf4-4ca0-a2bf-c6caccb0619a.png'
        elif (bank == 'bni'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/3a9855a3-8f3a-403e-bacc-89f485d3a061.png'
        elif (bank == 'mandiri'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/aa12bc89-a647-4ff8-8d93-c2f1fb8dd696.png'

        return img

    def get_payment_detail(self, obj):
        print(obj.id)
        a = {
            "type" : "Bank Transfer",
            "bank" : "bca",
            "detail" : '***********',
            "picture" : ''
        }
        detail = PaymentTransfer.objects.filter(accountId=obj.accountId, invoice=obj.id)
        detailcard = PaymentCard.objects.filter(accountId=obj.accountId, invoice=obj.id)

        if(list(detail) != []) :
            detail = PaymentTransfer.objects.filter(accountId=obj.accountId, invoice=obj.id).values().latest('createdAt')
            a = {
                "type" : "Bank Transfer - Automatic",
                "bank" : detail['bank'],
                "detail" : detail['virtual_account'],
                "picture" : self.img(bank=detail['bank'])
            }
        elif(list(detailcard) != []) :
            try:
                detailc = PaymentCard.objects.filter(accountId=obj.accountId, invoice=obj.id).values('card_number', 'bank', 'brand').latest('id')
                pict = ''
                if detailc['brand'] == 'VISA' :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/c6f24f5b-4106-407d-b24f-5c2331df0039.png'
                elif detailc['brand'] == 'MASTERCARD' :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/b109dc02-d390-41ff-b46d-745badbe93f3.png'
                else :
                    pict = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/029b5d41-f6a1-4b94-a783-a9e66f0968d7.png'
            
                a = {
                    "type" : "Card Credit",
                    "bank" : detailc['bank'],
                    "detail" : '***',
                    "picture" : pict
                }
            except PaymentCard.DoesNotExist:
                a = {
                    "type" : "Bank Transfer",
                    "bank" : "bca",
                    "detail" : '***********',
                    "picture" : ''
                }
        else :
            a = {
                    "type" : "Bank Transfer - Manual",
                    "bank" : "BCA",
                    "detail" : '***********',
                    "picture" : 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/ee13d270-7f9b-4d5e-90f3-32deab1eee7a.png'
                }
            
        return a
        
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceBillSerializer(serializers.ModelSerializer):
    invoice_type = serializers.SerializerMethodField('get_type')
    payment_type = serializers.SerializerMethodField('get_pay_type')
    payment_date = serializers.SerializerMethodField('get_payment_date')
    payment_status = serializers.SerializerMethodField('get_pay_status')

    def get_type(self, obj):

        data =  "Package Purchase"
            
        return data

    def get_pay_type(self, obj):
        manual = PaymentTransferManual.objects.filter(invoice=obj.id).count()
        card = PaymentCard.objects.filter(invoice=obj.id).count()
        if manual > 0:
            return 'manual'
        elif card > 0 :
            return 'card'
        else :
            return 'automatic'
    
    def get_payment_date(self, obj):
        if obj.payment_date == None:
            return obj.createdAt + timedelta(days=1)
        else :
            return obj.payment_date
        
    def get_pay_status(self, obj):

        if obj.payment_status == 'pending': 
            manual = PaymentTransferManual.objects.filter(invoice=obj.id).count()
            card = PaymentCard.objects.filter(invoice=obj.id).count()
            if manual > 0:
                a = PaymentTransferManual.objects.filter(invoice=obj.id).latest('id')
                return a.status
            elif card > 0:
                a = PaymentCard.objects.filter(invoice=obj.id).latest('id')
                return a.status
            else :
                try :
                    a = PaymentTransfer.objects.filter(invoice=obj.id).latest('id')
                    return a.status
                except PaymentTransfer.DoesNotExist:
                    return 'pending'
        else :
            return obj.payment_status

    class Meta:
        model = Invoice
        fields = '__all__'