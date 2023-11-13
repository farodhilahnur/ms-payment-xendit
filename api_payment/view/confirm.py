from api_payment.models import Invoice, PaymentCard, PaymentTransfer
from api_payment.services import BaseParameterMixin, ExternalService
from django.http.response import HttpResponse

from api_payment.utils import succ_resp
from ..serializers import InvoiceSerializer, InvoicesSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import rest_framework
import json
from datetime import datetime, timedelta

class PaymentConfirmListCreateView(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get(self, request):
        account_id = self.get_account_id()
        self.queryset = Invoice.objects.filter(accountId=account_id)

        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        temp = request.data

        order_id=temp.get("external_id")
        id=temp.get("id")
        time = temp.get("created") 
        user_date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')
        time = user_date 

        paymentdate = datetime.strftime(time, '%Y-%m-%d %H:%M')

        list_data = []

        data = PaymentTransfer.objects.filter(order_id=order_id).values()
        if(list(data) != []):
            for da in data :              
                list_data.append(da)
       
            # for a in list_data:
            PaymentTransfer.objects.filter(order_id=order_id).update(status='paid')
            invoiceid = PaymentTransfer.objects.filter(order_id=order_id).values_list('invoice', flat=True)
            Invoice.objects.filter(id=list(invoiceid)[0]).update(payment_status='paid', payment_date=time)
            y = Invoice.objects.filter(id=list(invoiceid)[0]).values()

            if y[0]['package'] == 'quarterly' :
                dates = y[0]['payment_date'] + timedelta(days=90)
                Invoice.objects.filter(id=list(invoiceid)[0]).update(account_expired=dates)
            else :
                dates = y[0]['payment_date'] + timedelta(days=365)
                Invoice.objects.filter(id=list(invoiceid)[0]).update(account_expired=dates)
            ExternalService().update_plan(accountId=y[0]['accountId'], plan=y[0]['plan'])
            ExternalService().update_maxmember(accountId=y[0]['accountId'], member=y[0]['total_user'])
            ExternalService().send_email_succes(email=y[0]['email'], amount=y[0]['total_amount'], date_payment=paymentdate)
            ExternalService().send_email_payment_process(email=y[0]['email'], paymentdate=paymentdate)

            if y[0]['plan'] == 'starter':
                ExternalService().update_privilege(accountId=y[0]['accountId'])

        return succ_resp(data='serializer.data')

class PaymentManualConfirmListCreateView(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get(self, request):
        account_id = self.get_account_id()
        self.queryset = Invoice.objects.filter(accountId=account_id)

        return self.list(request)
    
    def post(self, request, pk, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        temp = request.data

        Invoice.objects.filter(id=pk).update(payment_status='paid', payment_date=datetime.now())
        y = Invoice.objects.filter(id=pk).values()

        if y[0]['package'] == 'quarterly' :
            dates = y[0]['payment_date'] + timedelta(days=90)
            Invoice.objects.filter(id=pk).update(account_expired=dates)
        else :
            dates = y[0]['payment_date'] + timedelta(days=365)
            Invoice.objects.filter(id=pk).update(account_expired=dates)

        paymentdate = y[0]['payment_date'] + timedelta(hours=7)
        ExternalService().update_plan(accountId=y[0]['accountId'], plan=y[0]['plan'])
        ExternalService().update_maxmember(accountId=y[0]['accountId'], member=y[0]['total_user'])
        ExternalService().send_email_payment_process(email=y[0]['email'], paymentdate=paymentdate)

        if y[0]['plan'] == 'starter':
            ExternalService().update_privilege(accountId=y[0]['accountId'])

        return succ_resp(data='serializer.data')
