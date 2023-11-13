# media list, create
from api_payment.models import Invoice, Payment, PaymentTransfer, PaymentTransferManual, Setting
from api_payment.services import BaseParameterMixin, ExternalService
from django.http.response import HttpResponse
from api_payment.utils import succ_resp

from ..serializers import InvoiceSerializer, PaymentTransferManualSerializer, PaymentTransferSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import os
import json
from datetime import timedelta, datetime
import pytz
import uuid 

class ManualTransferListCreateView(BaseParameterMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentTransferManualSerializer

    def get(self, request, pk):
        account_id = self.get_account_id()
        self.queryset = PaymentTransferManual.objects.filter(accountId=account_id, invoice_id=pk).order_by('-createdAt')[:1]

        return self.list(request)
    
    def post(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        temp = request.data

        info = Invoice.objects.filter(id=pk).values('invoice_number', 'total_amount', 'email', 'id')
        infomail = Invoice.objects.filter(id=pk).values()
        for temps in temp:
            bank=temps.get("bank")
            name=temps.get("bank_account_name")
            rekening=temps.get("bank_account_number")
            
            partial_data = {"bank_transfer":{
                "bank": bank
                }
            }
            payment_type = "bank_transfer_manual"

            # ini buat nambah exp date 1 hari
            datenow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exp_time = datetime.strptime(datenow, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)

            if bank == "bca" :
                new_channel = PaymentTransferManual(
                    accountId=account_id,
                    invoice_id = pk,
                    email=info[0]['email'],
                    payment_type = payment_type,
                    bank = bank,
                    expired_date=exp_time,
                    total_amount=info[0]['total_amount'],
                    bank_account_name=name,
                    bank_account_number=rekening
                )

                new_channel.save()

                if infomail[0]['plan'] == 'starter':
                    plan = 'Starter'
                else :
                    plan = 'Professional'

                package_name = 'Paket '+str(plan)+' Yearly'
                priceuser = list(Setting.objects.filter(name='yearly').values_list('priceuser', flat=True))[0]
                if infomail[0]['package'] == 'quarterly':
                    package_name = 'Paket '+str(plan)+' Quarterly'
                    priceuser = list(Setting.objects.filter(name='quarterly').values_list('priceuser', flat=True))[0]
                
                onqty = 0
                onprice = '0'
                if infomail[0]['on_boarding_service'] == True:
                    onqty = 1
                    onprice = '5.000.000'

                ExternalService().send_email_manual(email= info[0]['email'], invoice=infomail[0]['invoice_number'], package_name=package_name, package_total=infomail[0]['total_price_user'], package_qty=infomail[0]['total_user'], package_per_price=priceuser, onborading_qty=onqty, onboarding_total=onprice, subtotal=infomail[0]['sub_total'], amount=infomail[0]['total_amount'], tax=infomail[0]['tax'], payment="Bank Transfer " + str(bank) )
                ExternalService().send_email_plain(email=info[0]['email'])
        Invoice.objects.filter(id=pk).update(payment_status='waiting', expired_date=exp_time)
        self.queryset = PaymentTransferManual.objects.get(id=new_channel.id)
        serializer = PaymentTransferManualSerializer(self.queryset, many=False)

        return succ_resp(data=serializer.data)

class ManualTransferView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = PaymentTransferManual.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = PaymentTransferManualSerializer

    def get(self, request, **kwargs):
        account_id = self.get_account_id()

        invoice = Invoice.objects.filter(id=self.kwargs["pk_invoice"], accountId = account_id).first()
        self.queryset = PaymentTransferManual.objects.filter(id=self.kwargs['pk'], invoice=invoice, accountId = account_id)

        return self.retrieve(request, **kwargs)

    def put(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
