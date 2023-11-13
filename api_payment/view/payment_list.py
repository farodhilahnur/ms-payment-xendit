from rest_framework.views import APIView
from rest_framework.response import Response
import json

from api_payment.models import Setting

class PaymentListCreateView(APIView):
    
   def get(self, request):
        type = self.request.GET.get('type')

        res = [
            {
                "type" : "Debit or Credit Card",
                "picture" : ""
            },
            {
                "type" : "Bank Transfer",
                "picture" : ""
            }
        ]
        if(type == 'transfer'):
            lis = Setting.objects.filter(type='bank').values()
            res = []
            for l in lis:
                data = {
                    "id" : l['id'],
                    "name" : l['name'],
                    "picture" :l['picture'],
                    "bank" : l['bank'],
                }
                res.append(data)

        return Response(status=200, data=res)