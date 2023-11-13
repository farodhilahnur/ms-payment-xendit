from datetime import timedelta, datetime
from api_payment.models import Invoice
from api_payment.serializers import BillingSerializer, InvoiceSerializer
from api_payment.services import BaseParameterMixin, ExternalService
from rest_framework import mixins, generics
import json

from api_payment.utils import succ_resp

class BillingCurrentPlanCreateView(BaseParameterMixin, mixins.RetrieveModelMixin,  mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = Invoice.objects.all()
    serializer_class = BillingSerializer

    def data(self, account_id, createdAt, email):
        if account_id != None:
            info_date = ExternalService().get_info_user(account_id=account_id)
            dates = datetime.strptime(info_date['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')  + timedelta(days=7)

        data ={"id": 1,
                "price_per_user": '-',
                "package_type": "Package Starter - FREE DEMO",
                "next_bill": dates,
                "leads": {
                    "quota": '-',
                    "remaining": '-'
                },
                "payment_detail": {
                    "type": "-",
                    "bank": "-",
                    "detail": None,
                    "picture": '-'
                },
                "email": str(email),
                "invoice_number": '-',
                "package": "-",
                "createdAt": str(createdAt),
                "createdBy": None,
                "modifiedAt": "-",
                "modifiedBy": None,
                "total_user": None,
                "total_price_user": None,
                "tax": None,
                "on_boarding_service": None,
                "sub_total": None,
                "total_amount": None,
                "payment_status": "unpaid",
                "exp_date": None,
                "accountId": int(account_id),
                "payment_date": None,
                "status": "running"}        
        return data

    def get(self, request):
        account_id = self.get_account_id()
        last = Invoice.objects.filter(accountId=account_id).values('id').order_by('-createdAt')

        if list(last) != []:
            self.queryset = Invoice.objects.get(id=list(last)[0]['id'])
            serializer = BillingSerializer(self.queryset, many=False, context={'request': request})
        else:
            user = ExternalService().get_info_user(account_id=account_id)
            return succ_resp(data=self.data(account_id=account_id, createdAt=user['createdAt'], email=user['name']))

        return succ_resp(data=serializer.data)

class UserNotifView(BaseParameterMixin, mixins.RetrieveModelMixin,  mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = Invoice.objects.all()
    serializer_class = BillingSerializer

    def get(self, request):
        email = self.get_email()
        ExternalService().send_email_active_user(email=email)

        return succ_resp(data='succes')
    