from api_payment.models import Invoice, PaymentTransfer, PaymentTransferManual
from api_payment.services import BaseParameterMixin
from django.http.response import HttpResponse
from ..serializers import InvoiceBillSerializer, InvoiceHistorySerializer, InvoiceSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import rest_framework
import json
from datetime import timedelta, datetime
import roman

class BillingHistoryCreateView(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceBillSerializer

    def get(self, request):
        account_id = self.get_account_id()
        filter_sort = self.filter_sort()
        filter_date = self.filter_date()
        size = self.get_size()
        skip = self.get_skip()

        if(size != None):
            if(skip != None) :
                size = self.page_limit(size=size, skip=skip)
                skip = int(skip)
            else :
                size = self.page_limit(size=size, skip=0)
                skip = None
        else :
            skip = None
            size = None
        
        today = datetime.today()
        PaymentTransferManual.objects.filter(status='pending', accountId=account_id, expired_date__lte = today).update(status='unpaid')
        PaymentTransfer.objects.filter(status='pending', accountId=account_id, expired_date__lte = today).update(status='unpaid')
        
        self.queryset = Invoice.objects.filter(accountId=account_id, **filter_date).order_by(filter_sort)[skip:size]

        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        temp_data = request.data
        
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        m = roman.toRoman(month)

        # nomer invoice
        nomer_urut= Invoice.objects.all().count() + 1
        # nomer = f"{nomer_urut:02}"
        no_invoice = str(nomer_urut) + "/JALA/" + m + "/" + str(year)[-2:]

        for temp in temp_data:
            total_user=temp.get("total_user")
            package = temp.get("package")
            on_boarding_service = temp.get("on_boarding_service")
            sub_total = temp.get("sub_total")
            total_amount = temp.get("total_amount")
            
            new_channel = Invoice(
                total_user= total_user,
                package = package,
                on_boarding_service = on_boarding_service,
                sub_total=sub_total,
                total_amount=total_amount,
                invoice_number=no_invoice,
                accountId = account_id
            )
            new_channel.save()
        
        return self.list(request)

class BillingHistoryRetrieveUpdateDeleteView(BaseParameterMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    mixins.DestroyModelMixin, 
                    generics.GenericAPIView):

    def get_queryset(self):
        account_id = self.get_account_id()
        
        queryset = Invoice.objects.filter(accountId=account_id)
        return queryset
    
    serializer_class = InvoiceHistorySerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()

        temp = request.data
        bank_name = temp.get("bank_account_name")
        bank_number = temp.get("bank_account_number")

        if bank_name and bank_number != None :
            PaymentTransferManual.objects.filter(invoice=pk).update(bank_account_name=bank_name, bank_account_number=bank_number)
        
        proof = temp.get("proof_picture")
        if proof != None :
            PaymentTransferManual.objects.filter(invoice=pk).update(proof=proof)

        return self.update(request, pk)
    
    def delete(self, request, pk):
        self.destroy(request, pk)
        response = "success delete id "+str(pk)
        return HttpResponse(json.dumps(response, ensure_ascii=False), content_type="application/json")
