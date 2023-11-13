from api_payment.models import Invoice
from api_payment.services import BaseParameterMixin, ExternalService
from api_payment.utils import succ_resp
from ..serializers import CekInvoiceSerializer
from rest_framework import mixins, generics
from datetime import datetime, timedelta

class CekPayment(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = CekInvoiceSerializer

    def get(self, request):
        account_id = self.get_account_id()
        resp = []
        listdata = []

        now = datetime.now() + timedelta(seconds=25200)
        data = Invoice.objects.filter(account_expired__isnull=False, account_expired__lte=now, update_core=False).exclude(payment_status='paid').values('id', 'invoice_number', 'accountId', 'expired_date')
        trialaccount = ExternalService().get_info_account()
        
        for x in data :
            x.update({'detail' : 'subscribe'})
            listdata.append(x)
        for t in trialaccount:
            if datetime.strptime(t['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')  + timedelta(days=30) < now :
                t.update({'detail' : 'demo'})
                listdata.append(t)

        if listdata != []:
            for d in listdata:
                resp.append(d)
                d.update({'message' : 'failed'})
                tocore = ExternalService().update_to_core(accountId=d['accountId'], status='unpaid')
                Invoice.objects.filter(invoice_number=d['invoice_number']).update(status='stop')

                if(tocore == 200):
                    d.update({'message' : 'success'})
                    # print(d)
                    if(d.get('invoice_number') != None):
                        Invoice.objects.filter(invoice_number=d['invoice_number']).update(update_core=True)
                
        return succ_resp(data=resp)
    