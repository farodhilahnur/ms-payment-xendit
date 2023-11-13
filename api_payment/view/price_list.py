from rest_framework.views import APIView
from rest_framework.response import Response
import json

from api_payment.models import Setting

class PriceListCreateView(APIView):
    
   def get(self, request):
        total_user = self.request.GET.get('total_user')
        plan = self.request.GET.get('plan')

        if(total_user == None) :
            if plan == 'starter' :
                lis = Setting.objects.filter(type='user', plan='starter').values()
            elif plan == 'professional' :
                lis = Setting.objects.filter(type='user', plan='professional').values()
            else : 
                lis = Setting.objects.filter(type='user', plan='starter').values()
                plan = 'starter'

            res = []
            for l in lis :
                data = {
                l['name'] : {"periode" : l['periode'],
                                    "total_price_user" : l['priceuser'],
                                    "plan" : plan,
                                }
                }
                res.append(data)
            
        else :
            hargatahunan = Setting.objects.filter(name='yearly', type='user')
            pricetahun = hargatahunan[0].priceuser

            hargaquarter = Setting.objects.filter(name='quarterly', type='user')
            pricequarter = hargaquarter[0].priceuser

            total_harga_quarter = int(pricequarter) * int(total_user)
            total_harga_year = int(pricetahun) * int(total_user)

            res = [
                {
                'quarterly' : {"periode" : "3 Bulan Pemakaian",
                                    "total_price_user" : pricequarter,
                                    "total_harga" : total_harga_quarter,
                                }
                },
                {
                    'yearly' : {"periode" : "1 Bulan Pemakaian",
                                    "total_price_user" : pricetahun,
                                    "total" : total_harga_year,
                                }
                }
                ]

        return Response(status=200, data=res)