# media list, create
from api_payment.models import Invoice, Payment, PaymentTransfer, Setting
from api_payment.services import BaseParameterMixin, ExternalService
from django.http.response import HttpResponse
from api_payment.utils import succ_resp

from ..serializers import InvoiceSerializer, PaymentTransferSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import os
import json
from datetime import timedelta, datetime
from xendit import Xendit
import uuid 
import pytz
import logging


class PaymentTransferListCreateView(BaseParameterMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentTransferSerializer

 

    def get(self, request, pk):
        account_id = self.get_account_id()
        self.queryset = PaymentTransfer.objects.filter(accountId=account_id, invoice_id=pk).order_by('-createdAt')

        return self.list(request)
    
    def post(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        base_url_apikey = os.environ.get('XENDIT_API_KEY')
        temp = request.data

        xendit_instance = Xendit(api_key=base_url_apikey)

        info = Invoice.objects.filter(id=pk).values('invoice_number', 'total_amount', 'email', 'id', 'expired_date', 'accountId')
        infomail = Invoice.objects.filter(id=pk).values()
        for temps in temp:
            bank=temps.get("bank")
            payment_type = "bank_transfer"

            # ini buat nambah exp date 1 hari
            # timenow = datetime.now(tz=pytz.timezone('Asia/Jakarta'))
            # timeDeltaKwarg = {"minutes": 1440}
            # exp_date = timenow+timedelta(**timeDeltaKwarg)

            # ini buat nambah exp date 1 hari
            datenow = datetime.now(tz=pytz.timezone('Asia/Jakarta')).strftime("%Y-%m-%d %H:%M:%S")
            exp_time = datetime.strptime(datenow, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)

            orderid = str(info[0]['invoice_number']) + "-" +uuid.uuid4().hex[:6].upper()
            charge_response = xendit_instance.VirtualAccount.create(
                        external_id= orderid,
                        bank_code= bank.upper(),
                        name= 'Rp ' + str(info[0]['total_amount']),
                        is_closed= True,
                        expected_amount= info[0]['total_amount'],
                        expiration_date= exp_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        is_single_use=True
                    )
            logger = logging.getLogger(__name__)
            logger.info(charge_response)

            new_channel = PaymentTransfer(
                accountId=account_id,
                invoice_id = pk,
                payment_type = payment_type,
                bank = str(bank).upper(),
                expired_date=exp_time,
                expired=exp_time,
                transaction_time=datenow,
                virtual_account=charge_response.account_number,
                total_amount=charge_response.expected_amount,
                order_id=charge_response.external_id,
                transaction_id=charge_response.id
            )
            new_channel.save()

            hargaquarter = Setting.objects.filter(name='quarterly').values_list('priceuser', flat=True)
            hargayearly = Setting.objects.filter(name='yearly').values_list('priceuser', flat=True)

            if infomail[0]['plan'] == 'starter':
                plan = 'Starter'
            else :
                plan = 'Professional'

            package_name = 'Paket '+str(plan)+' Quarterly'

            priceuser = hargayearly[0]
            if infomail[0]['package'] == 'quarterly':
                package_name = 'Paket '+str(plan)+' Quarterly'
                priceuser = hargaquarter[0]
            onqty = 0
            onprice = '0'
            if infomail[0]['on_boarding_service'] == True:
                onqty = 1
                onprice = '5.000.000'

            if bank == 'mandiri' or 'MANDIRI': 
                ExternalService().send_email_mandiri(email='dhillankr40@gmail.com', invoice=infomail[0]['invoice_number'], package_name=package_name, package_total=int(infomail[0]['total_price_user']), package_qty=infomail[0]['total_user'], package_per_price=priceuser, onborading_qty=onqty, onboarding_total=onprice, subtotal=int(infomail[0]['sub_total']), amount=int(infomail[0]['total_amount']), tax=infomail[0]['tax'], va=charge_response.account_number, payment="Bank Transfer " + str(bank).upper() )
            else :
                ExternalService().send_email(email= info[0]['email'], invoice=infomail[0]['invoice_number'], package_name=package_name, package_total=infomail[0]['total_price_user'], package_qty=infomail[0]['total_user'], package_per_price=priceuser, onborading_qty=onqty, onboarding_total=onprice, subtotal=infomail[0]['sub_total'], amount=infomail[0]['total_amount'], tax=infomail[0]['tax'], va=charge_response.account_number, payment="Bank Transfer " + str(bank).upper() )
            
        self.queryset = PaymentTransfer.objects.get(id=new_channel.id)
        serializer = PaymentTransferSerializer(self.queryset, many=False)

        return succ_resp(data=serializer.data)

class PaymentTransferView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = PaymentTransfer.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = PaymentTransferSerializer

    def get(self, request, **kwargs):
        account_id = self.get_account_id()

        invoice = Invoice.objects.filter(id=self.kwargs["pk_invoice"], accountId = account_id).first()
        self.queryset = PaymentTransfer.objects.filter(id=self.kwargs['pk'], invoice=invoice, accountId = account_id)

        return self.retrieve(request, **kwargs)

    def put(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
