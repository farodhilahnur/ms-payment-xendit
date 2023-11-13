from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime, timedelta
from api_payment.models import Invoice, PaymentCard, PaymentTransfer, Setting
from api_payment.services import ExternalService

class BillingUpgradeCreateView(APIView):

    def img(self, bank):
        img = ''
        if(bank == 'bca'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/ccb8ea59-9cf4-4ca0-a2bf-c6caccb0619a.png'
        elif (bank == 'bni'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/3a9855a3-8f3a-403e-bacc-89f485d3a061.png'
        elif (bank == 'mandiri'):
            img = 'https://jala-testing.s3.ap-southeast-1.amazonaws.com/accounts/imgs/aa12bc89-a647-4ff8-8d93-c2f1fb8dd696.png'

        return img

    def payment(self, invid, account_id):
        detail = PaymentTransfer.objects.filter(accountId=account_id, invoice=invid)

        if(list(detail) != []) :
            detail = PaymentTransfer.objects.filter(accountId=account_id, invoice=invid).values().latest('createdAt')
            a = {
                "type" : "Bank Transfer",
                "bank" : detail['bank'],
                "detail" : detail['virtual_account'],
                "picture" : self.img(bank=detail['bank'])
            }
        else :
            detail = PaymentCard.objects.filter(accountId=account_id, invoice=invid).values('card_number', 'bank').latest('id')
            a = {
                "type" : "Card",
                "bank" : detail['bank'],
                "detail" : detail['card_number'],
                "picture" : self.img(bank=detail['bank'])
            }

        return a
        
    def get(self, request):
        account_id = self.request.GET.get('account_id')
        enter = {
                'Paket Enterprise' : {"Real-time lead distribution" : True,
                                    "Lead Performance" : True,
                                    "Campaign Performance" : True,
                                    "Lead Volume (Unlimited)" : True,
                                    "Team Performance" : True,
                                    "Export / Import Database" : True,
                                    "Web Integration" : True,
                                    "Lead Migration" : True,
                                    "Product Support (Online / Offline)" : True,
                                    "Sales Pipelines" : True,
                                    "Lead Rotation" : True,
                                    "Facebook Lead Form Integration" : True,
                                    "Instagram Lead Form Integration" : True,
                                    "Google Sheet Integration" : True,
                                    "Customer" : True,
                                    "Lead Scoring" : True,
                                    "JALA Assistant (Mobile App)" : True
                                }
                }    
        starter =  {'Paket Starter' : {"Real-time lead distribution" : True,
                                    "Lead Performance" : True,
                                    "Campaign Performance" : True,
                                    "Lead Volume (5000 Leads)" : True,
                                    "Team Performance" : True,
                                    "Export / Import Database" : True,
                                    "Web Integration" : True,
                                    "Lead Migration" : True,
                                    "Product Support (Online)" : True,
                                    "Sales Pipelines" : False,
                                    "Lead Rotation" : False,
                                    "Facebook Lead Form Integration" : False,
                                    "Instagram Lead Form Integration" : False,
                                    "Google Sheet Integration" : False,
                                    "Customer" : False,
                                    "Lead Scoring" : False,
                                    "JALA Assistant (Mobile App)" : True
                                }
                                }
        profesional =   {'Paket Professinoal' : {"Real-time lead distribution" : True,
                                    "Lead Performance" : True,
                                    "Campaign Performance" : True,
                                    "Lead Volume (Unlimited)" : True,
                                    "Team Performance" : True,
                                    "Export / Import Database" : True,
                                    "Web Integration" : True,
                                    "Lead Migration" : True,
                                    "Product Support (Online)" : True,
                                    "Sales Pipelines" : True,
                                    "Lead Rotation" : True,
                                    "Facebook Lead Form Integration" : True,
                                    "Instagram Lead Form Integration" : True,
                                    "Google Sheet Integration" : True,
                                    "Customer" : True,
                                    "Lead Scoring" : True,
                                    "JALA Assistant (Mobile App)" : True
                                }}
            
        try : 
            invid = Invoice.objects.filter(accountId=account_id).values_list('id', flat=True).latest('id')
            invoice = Invoice.objects.filter(accountId=account_id).values().latest('id')

            plan = 'starter'
            if invoice['plan'] != None :
                plan = str(invoice['plan'])
            
            det_package = "Paket "+ plan.capitalize() +"  - Yearly"
            harga = Setting.objects.filter(name='yearly', type='user', plan=plan)
            price = harga[0].priceuser
            period = "1 year"

            if invoice['package'] == 'quarterly' :
                det_package = "Paket "+ plan.capitalize() +"  - Quarterly"
                harga = Setting.objects.filter(name='quarterly', type='user', plan=plan)
                price = harga[0].priceuser
                period = "3 months"

            isplan = False
            if(invid != []):
                isplan = True

            if(invid != []):
                responses = [
                {
                    "isCurrentPlan" : isplan,
                    "plan" : det_package,
                    "payment" : {
                        "period" : period,
                        "price_per_user" : price,
                        "detail" : self.payment(invid = invid, account_id=account_id)
                    },
                    "features": starter
                },
                {
                    "isCurrentPlan" : False,
                    "plan" : "Professional Package",
                    "detail" : "Get an unlimited lead quota and get more exclusive features.",
                    "payment" : {
                        "period" : '-',
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": profesional
                },
                {
                    "isCurrentPlan" : False,
                    "detail" : "Get unlimited lead quotas, more exclusive features, offline product support, and special features, namely product bookings.",
                    "plan" : "Enterprise",
                    "payment" : {
                        "period" : '-',
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": enter
                }
            ]
        except :
            core = ExternalService().get_info_user(account_id=account_id)
            remaindays = '7'
            if(core != None) :
                exp = datetime.strptime(str(core['createdAt']) , '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(days=7)
                remaindays =  (exp - datetime.today()).days
                if remaindays < 0:
                    remaindays = 0

            response = [
                {
                    "isCurrentPlan" : True,
                    "plan" : "FREE DEMO",
                    "detail" : 'Expires in ' + str(remaindays) + ' Days',
                    "payment" : {
                        "period" : "7 Days of usage",
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": '-'
                },
                {
                    "isCurrentPlan" : False,
                    "plan" : 'Paket Starter',
                    "detail" : 'Get complete features from JALA.ai at an affordable price',
                    "payment" : {
                        "period" : '-',
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": starter
                },
                {
                    "isCurrentPlan" : False,
                    "plan" : "Professional Package",
                    "detail" : "Get an unlimited lead quota and get more exclusive features.",
                    "payment" : {
                        "period" : '-',
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": profesional
                },
                {
                    "isCurrentPlan" : False,
                    "detail" : "Get unlimited lead quotas, more exclusive features, offline product support, and special features, namely product bookings.",
                    "plan" : "Enterprise",
                    "payment" : {
                        "period" : '-',
                        "price_per_user" : '-',
                        "detail" : '-'
                    },
                    "features": enter
                }
            ]
            
            return Response(status=200, data=response)

        return Response(status=200, data=responses)