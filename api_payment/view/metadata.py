from rest_framework.views import APIView
from rest_framework.response import Response
import json

class PaymentMetadata(APIView):
    def get(self, request):
        res = {
            'payment_statuses' : {'pending', 'paid', 'unpaid', 'waiting'},
            'statuses' : {'hold', 'running', 'stop'},
            'sorting' : {'oldest', 'newest'}
            }
        return Response(status=200, data=res)