from rest_framework.views import APIView
from rest_framework.response import Response
import json

class PackageListCreateView(APIView):
    
   def get(self, request):

        res = [
            {
            'Paket Starter' : {"Real-time lead distribution" : True,
                                "Lead Performance" : True,
                                "Campaign Performance" : True,
                                "Lead Volume" : "5000 Leads",
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
                            },
            'Paket Professinoal' : {"Real-time lead distribution" : True,
                                "Lead Performance" : True,
                                "Campaign Performance" : True,
                                "Lead Volume" : "Unlimited",
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
                            },
            'Paket Enterprise' : {"Real-time lead distribution" : True,
                                "Lead Performance" : True,
                                "Campaign Performance" : True,
                                "Lead Volume" : "Unlimited",
                                "Team Performance" : True,
                                "Export / Import Database" : True,
                                "Web Integration" : True,
                                "Lead Migration" : True,
                                "Product Support (Online)" : "Online / sOffline",
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
            ]

        return Response(status=200, data=res)