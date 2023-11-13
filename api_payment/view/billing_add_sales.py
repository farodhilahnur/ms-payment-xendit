from rest_framework.views import APIView
from rest_framework.response import Response
import json

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
            res = [
            {
                "bank" : "BCA",
                "picture" : ""
            },
            {
                "bank" : "BNI",
                "picture" : ""
            },
            {
                "bank" : "BRIVA - Virtual Account",
                "picture" : ""
            },
            {
                "bank" : "MANDIRI",
                "picture" : ""
            }
        ]

        return Response(status=200, data=res)