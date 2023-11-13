# media list, create
from api_payment.models import Invoice, Payment, PaymentCard, PaymentTransfer, Setting
from api_payment.services import BaseParameterMixin, ExternalService
from django.http.response import HttpResponse
from api_payment.utils import resp

from ..serializers import InvoiceSerializer, PaymentCardSerializer, PaymentTransferSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import requests
import json
import uuid 
import os
from base64 import b64encode

from xendit import Xendit

class PaymentCreditListCreateView(BaseParameterMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentCardSerializer

    def get_info_card(self,token):
        url = 'https://api.xendit.co/credit_card_tokens/'+token
        pub_key = os.environ.get('XENDIT_API_KEY')
        credentials = f"{pub_key}:{''}"
        encodedCredentials = str(b64encode(credentials.encode("utf-8")), "utf-8")
        
        response = requests.request("GET", url, headers={"Authorization": f"Basic {encodedCredentials}", 'Content-Type': 'application/json','Accept': 'application/json'})
        if(response.status_code == 200):
            res = json.loads(response.text)
            return res
        else:
            return None
    
    def get_charge(self, token, orderid, amount):
        api_key = os.environ.get('XENDIT_API_KEY')
        xendit_instance = Xendit(api_key=api_key)
        CreditCard = xendit_instance.CreditCard
        charge = CreditCard.create_charge(
            token_id= token,
            external_id= orderid,
            amount= amount,
        )

        return charge
    
    def get(self, request, pk):
        account_id = self.get_account_id()
        self.queryset = PaymentCard.objects.filter(accountId=account_id, invoice_id=pk)

        return self.list(request)
    
    def post(self, request, pk, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        token =self.get_tokenid()
        temps = request.data

        info = Invoice.objects.filter(id=pk).values('invoice_number', 'total_amount', 'email', 'accountId', 'total_user', 'plan')
        orderid = str(info[0]['invoice_number']) + "-" +uuid.uuid4().hex[:6].upper()

        # post buat ambil token card
        new_channel = PaymentCard(
            accountId=account_id,
            invoice_id = pk,
            payment_type = "credit_card",
            order_id=orderid,
            total_amount= info[0]['total_amount'],
        )
        new_channel.save()

        infocard = PaymentCard.objects.filter(id=new_channel.id)
        if token != None :
            infocard.update(token_id=token)
            carddata = self.get_info_card(token=token)
            # print(carddata)
            if carddata != None :
                infocard.update(card_data=carddata['card_info'], bank=carddata['card_info']['bank'], brand=carddata['card_info']['brand'])

        infocard = infocard.values()
        try :
            # post buat get charge
            charge =  self.get_charge(token=token, orderid=infocard[0]['order_id'], amount=infocard[0]['total_amount'])
            PaymentCard.objects.filter(id=new_channel.id).update(charge_status=charge.status, charge_id=charge.id)
        except :
            charge = None

       # setelah charge kita update statusnya di invoice + card info
        if charge != None:
            if charge.status == 'CAPTURED' or charge.status == 'AUTHORIZED' :
                Invoice.objects.filter(id=pk).update(payment_status='paid')
                PaymentCard.objects.filter(id=new_channel.id).update(status='paid', charge_id=charge.id, charge_status=charge.status)
                ExternalService().update_plan(accountId=info[0]['accountId'], plan=info[0]['plan'])
                ExternalService().update_maxmember(accountId=info[0]['accountId'], member=info[0]['total_user'])

                infoin = Invoice.objects.filter(id=pk).values()
                if infoin[0]['plan'] == 'starter':
                    plan = 'Starter'
                else :
                    plan = 'Professional'
                package_name = 'Paket '+str(plan)+' Yearly'
                priceuser = list(Setting.objects.filter(name='yearly').values_list('priceuser', flat=True))[0]
                if infoin[0]['package'] == 'quarterly':
                    package_name = 'Paket '+str(plan)+' Quarterly'
                    priceuser = list(Setting.objects.filter(name='quarterly').values_list('priceuser', flat=True))[0]
                
                onqty = 0
                onprice = '0'
                if infoin[0]['on_boarding_service'] == True:
                    onqty = 1
                    onprice = '5.000.000'
                    
                ExternalService().send_email_cc(email=infoin[0]['email'], invoice=infoin[0]['invoice_number'], package_name=package_name, package_total=infoin[0]['total_price_user'], package_qty=infoin[0]['total_user'], package_per_price=priceuser, onborading_qty=onqty, onboarding_total=onprice, subtotal=infoin[0]['sub_total'], amount=infoin[0]['total_amount'], tax=infoin[0]['tax'] )
                ExternalService().send_email_payment_process(email=infoin[0]['email'], paymentdate=infoin[0]['createdAt'])
                if infoin[0]['plan'] == 'starter':
                    ExternalService().update_privilege(accountId=account_id)
        # update ke core + kirim email

        self.queryset = PaymentCard.objects.get(id=new_channel.id)
        serializer = PaymentCardSerializer(self.queryset, many=False)
        datas = serializer.data
        status = 200

        return resp(data=datas, status=status)

class PaymentCardRetrieveUpdateDeleteView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = PaymentCard.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = PaymentCardSerializer

    def get(self, request, **kwargs):
        account_id = self.get_account_id()
        
        invoice = Invoice.objects.filter(id=self.kwargs["pk_invoice"], accountId = account_id).first()
        self.queryset = PaymentCard.objects.filter(id=self.kwargs['pk'], invoice=invoice, accountId = account_id)

        return self.retrieve(request, **kwargs)

    def put(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

class InvoiceRetrieveUpdateDeleteView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = Invoice.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = InvoiceSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")

class PaymentCardAuthView(BaseParameterMixin, mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):
    
    queryset = Payment.objects.all()
    serializer_class = PaymentCardSerializer

    def get_info_card(self,token):
        url = 'https://api.xendit.co/credit_card_tokens/'+token
        pub_key = os.environ.get('XENDIT_API_KEY')
        credentials = f"{pub_key}:{''}"
        encodedCredentials = str(b64encode(credentials.encode("utf-8")), "utf-8")
        
        response = requests.request("GET", url, headers={"Authorization": f"Basic {encodedCredentials}", 'Content-Type': 'application/json','Accept': 'application/json'})
        if(response.status_code == 200):
            res = json.loads(response.text)
            return res
        else:
            return None
    
    def get_charge(self, token, orderid, amount, cvv):
        api_key = os.environ.get('XENDIT_API_KEY')
        xendit_instance = Xendit(api_key=api_key)
        CreditCard = xendit_instance.CreditCard

        charge = CreditCard.create_charge(
            token_id= token,
            external_id= orderid,
            amount= amount,
            card_cvn=str(cvv),
        )
        return charge
       
    def get(self, request, pk):
        account_id = self.get_account_id()
        self.queryset = PaymentCard.objects.filter(accountId=account_id, invoice_id=pk)

        return self.list(request)
    
    def post(self, request, pk, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        temp = request.data

        infocard = PaymentCard.objects.filter(id=pk)
        token = temp.get("id")

        if token != None :
            infocard.update(token_id=token)
            carddata = self.get_info_card(token=token)
            print(carddata)
            if carddata != None :
                infocard.update(card_data=carddata['card_info'], bank=carddata['card_info']['bank'], brand=carddata['card_info']['brand'])

        infocard = infocard.values()
        try :
            # post buat get charge
            charge =  self.get_charge(token=token, orderid=infocard[0]['order_id'], amount=infocard[0]['total_amount'], cvv=infocard[0]['cvv'])
            PaymentCard.objects.filter(id=pk).update(charge_status=charge.status, charge_id=charge.id)
        except :
            charge = None

       # setelah charge kita update statusnya di invoice + card info
        if charge != None:
            if charge.status == 'CAPTURED' or charge.status == 'AUTHORIZED' :
                Invoice.objects.filter(id=infocard[0]['invoice_id']).update(payment_status='paid')
                PaymentCard.objects.filter(id=pk).update(status='paid')
        
        # update ke core + kirim email

        try : 
            self.queryset = PaymentCard.objects.get(id=pk)
            serializer = PaymentCardSerializer(self.queryset, many=False)
            datas = serializer.data
            status = 200
        except :
            datas = { 'message' : 'not Found'}
            status = 400

        return resp(data=datas, status=status)
