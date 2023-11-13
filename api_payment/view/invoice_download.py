from api_payment.models import Invoice
from api_payment.services import BaseParameterMixin
from django.http.response import HttpResponse

from easy_pdf.views import PDFTemplateView
from django.shortcuts import get_list_or_404, get_object_or_404
from jinja2 import Template


class InvoicePDFView(PDFTemplateView):
    template_name = "invoice_pdf.html"

    def get_context_data(self, **kwargs):
        invoice = Invoice.objects.filter(id=self.kwargs['pk']).values()
        amount = invoice[0]['total_amount']
        invoice_number = invoice[0]['invoice_number']
        tax  = invoice[0]['tax']
        subttotal  = invoice[0]['sub_total']
        usr  = invoice[0]['total_user']
        total_price_user = invoice[0]['total_price_user']

        on_boarding_service = invoice[0]['on_boarding_service']
        serviceqty = 0
        serviceprice = 'Rp. 0'
        if on_boarding_service == True :
          serviceqty = 1
          serviceprice = 'Rp. 5.000.000'

        email = invoice[0]['email']
        package = invoice[0]['package']
        plan = invoice[0]['plan']
        infopackage = 'Paket '+ str(plan)+' - Yearly'
        if package == 'quarterly':
          infopackage = 'Paket '+ str(plan)+' - Quarterly'
      
        address= "123 Street name"
        city= "Vancouver"
        phone= "555-555-2345"

        htmlw = '''<head>
        
	<style>
		@page {
			size: a4 portrait;
			@frame header_frame {           /* Static Frame */
				-pdf-frame-content: header_content;
				left: 50pt; width: 512pt; top: 50pt; height: 40pt;
			}
			@frame content_frame {          /* Content Frame */
				left: 50pt; width: 512pt; top: 90pt; height: 632pt;
			}
			@frame footer_frame {           /* Another static Frame */
				-pdf-frame-content: footer_content;
				left: 50pt; width: 512pt; top: 772pt; height: 20pt;
			}
		}
	</style>
	</head>
	
	<body>
		<!-- Content for Static Frame 'header_frame' -->
		<div id="header_content">
    <table>
      <tr>
        <td><h3>Invoice JALA.ai</h3></td>
        <td><h3>No. invoice : {{invoice_number}}</h3></td>
      </tr>
    </table>
			
		</div>
	
		<!-- Content for Static Frame 'footer_frame' -->
		<div id="footer_content">(c) - page <pdf:pagenumber>
			of <pdf:pagecount>
		</div>
	
		<!-- HTML Content -->
		<table>
				<tr>
          <td><h4>Order from</h4></td>
          <td><h4>Billed to</h4></td>
				</tr>
				<tr>
					<td>JALA Digital Indonesia</td>
					<td>{{email}}</td>
				</tr>

		</table>
	
		<hr>
	
		<table>
			<tr>
	 
				<th>Detail</th>
				<th>Qty</th>
				<th>Price every qty</th>
				<th>Total</th>
			</tr>
			<tr>
	 
				<td>{{infopackage}}</td>
				<td>{{usr}}</td>
				<td>Rp. 420.000</td>
				<td>Rp. {{total_price_user}}</td>
			</tr>
			<tr>
	 
				<td>Onborading Service </td>
				<td>{{serviceqty}}</td>
				<td>{{serviceprice}}</td>
				<td>{{serviceprice}}</td>
			</tr>
		</table>
	
		<hr>
    <p style="text-align:right"><strong>Sub Total: Rp. {{subttotal}} </strong></p>
    <p style="text-align:right"><strong>Tax : Rp. {{tax}} </strong></p>
		<p style="text-align:right"><strong>Total: Rp. {{amount}} </strong></p>
    <p style="text-align:center"><strong>Payment Method: Bank Transfer BCA </strong></p>
    <p style="text-align:center"><strong>Nomor VA: 9999992323 </strong></p>
	</body>
	</html>'''
        template = Template(htmlw)
        res = template.render(amount=amount, tax=tax, invoice_number=invoice_number, infopackage=infopackage, phone=phone, subttotal=subttotal, email=email, usr=usr, serviceqty=serviceqty, serviceprice=serviceprice, total_price_user=total_price_user)
        handle1=open('api_payment/templates/invoice_pdf.html','r+')
        handle1.write(res)
        context = super().get_context_data(**kwargs)
        myinstance = get_object_or_404(Invoice, pk=context['pk'])
        context['myinstance'] = myinstance

        return context
