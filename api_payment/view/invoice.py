from api_payment.models import Invoice, Setting
from api_payment.services import BaseParameterMixin
from django.http.response import HttpResponse

from api_payment.utils import succ_resp
from ..serializers import InvoiceSerializer, InvoicesSerializer
from django.db.models import Q
from rest_framework import mixins, generics
import rest_framework
import json
import datetime
import roman

class InvoiceListCreateView(BaseParameterMixin, mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView, mixins.RetrieveModelMixin):
    
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    def get(self, request):
        account_id = self.get_account_id()
        self.queryset = Invoice.objects.filter(accountId=account_id)

        return self.list(request)
    
    def post(self, request, *args, **kwargs):
        account_id = self.get_account_id()
        invoker_id = self.get_invoker_id()
        plan = self.get_plan()
        temp_data = request.data
        
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        m = roman.toRoman(month)

        # nomer invoice
        try:
            nomer_urut= Invoice.objects.all().values('id').latest('id')
            nomer_urut = int(nomer_urut['id']) + 1
        except Invoice.DoesNotExist:
            nomer_urut= Invoice.objects.values('id').latest('id')
            nomer_urut = 1
        
        no_invoice = str(nomer_urut) + "/JALA/" + m + "/" + str(year)[-2:]

        for temp in temp_data:
            email=temp.get("email")
            total_user=temp.get("total_user")
            package = temp.get("package")
            on_boarding_service = temp.get("on_boarding_service")
            total_price_user = temp.get("total_amount")
            # total_amount = temp.get("total_amount")
            # sub_total = temp.get("sub_total")

            onboard = 0
            if(on_boarding_service == True):
                onboard = 5000000

            sub_total = total_price_user + onboard
            tax = sub_total * (11/100)
            total_amount = sub_total + tax

            new_channel = Invoice(
                email=email,
                total_user= total_user,
                package = package,
                total_price_user=total_price_user,
                on_boarding_service = on_boarding_service,
                sub_total=sub_total,
                tax=tax,
                total_amount=int(total_amount),
                invoice_number=no_invoice,
                accountId = account_id,
                plan=plan
            )
            new_channel.save()

        datas = Invoice.objects.filter(id=new_channel.id)
        serializer = InvoicesSerializer(datas, many=True)

        if(serializer.data != None):
            for p in serializer.data:
                if p['plan'] == 'starter':
                    plan = 'Starter'
                else :
                    plan = 'Professional'

                det_package = "Paket "+ str(plan)+" - Yearly"
                harga = Setting.objects.filter(name='yearly', type='user')
                price = harga[0].priceuser

                if(p['package'] == 'quarterly'):
                    det_package = "Paket "+ str(plan)+" - Quarterly"
                    harga = Setting.objects.filter(name='quarterly', type='user')
                    price = harga[0].priceuser
                
                    total_onboard = 0
                    price_onboard = 0
                    if(p['on_boarding_service'] == True):
                        total_onboard = 1
                        price_onboard = 5000000

                    user = p['total_user']

                    data = {"order_summary" :[
                        {
                            "detail": det_package,
                            "qty": user,
                            "price": price,
                            "total": p['total_price_user']
                        },
                        {
                            "detail": "On Boarding service",
                            "qty": total_onboard,
                            "price": price_onboard,
                            "total": price_onboard
                        }
                    ]}
                    p.update(data)

                    data_total =  {"total_summary": {
                        "sub_total": p['sub_total'],
                        "tax": p['tax'],
                        "total_amount": p['total_amount']
                    }}
                    p.update(data_total)

        return succ_resp(data=serializer.data)

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
