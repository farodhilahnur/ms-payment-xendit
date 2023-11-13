from django.urls import path
from api_payment.view.billing_current import BillingCurrentPlanCreateView, UserNotifView
from api_payment.view.billing_history import BillingHistoryCreateView, BillingHistoryRetrieveUpdateDeleteView
from api_payment.view.billing_upgrade import BillingUpgradeCreateView
from api_payment.view.cek_exp import CekPayment
from api_payment.view.confirm import PaymentConfirmListCreateView, PaymentManualConfirmListCreateView

from api_payment.view.invoice import InvoiceListCreateView, InvoiceRetrieveUpdateDeleteView
from api_payment.view.invoice_download import InvoicePDFView
from api_payment.view.metadata import PaymentMetadata
from api_payment.view.package_list import PackageListCreateView
from api_payment.view.payment_crredit import PaymentCardAuthView, PaymentCardRetrieveUpdateDeleteView, PaymentCreditListCreateView
from api_payment.view.payment_list import PaymentListCreateView
from api_payment.view.payment_manual import ManualTransferListCreateView, ManualTransferView
from api_payment.view.payment_transfer import PaymentTransferListCreateView, PaymentTransferView
from api_payment.view.price_list import PriceListCreateView

urlpatterns = [   
   # path('payment/notification_handling', NotificationListCreateView.as_view()),
   path('invoice', InvoiceListCreateView.as_view()),
   path('invoice/<int:pk>', InvoiceRetrieveUpdateDeleteView.as_view()),

   path('invoice/<int:pk>/payment_transfer', PaymentTransferListCreateView.as_view()),
   path('invoice/<int:pk_invoice>/payment_transfer/<int:pk>', PaymentTransferView.as_view()),

   path('invoice/<int:pk>/payment_manual', ManualTransferListCreateView.as_view()),
   path('invoice/<int:pk_invoice>/payment_manual/<int:pk>', ManualTransferView.as_view()),

   path('invoice/<int:pk>/payment_card', PaymentCreditListCreateView.as_view()),
   path('invoice/<int:pk_invoice>/payment_card/<int:pk>', PaymentCardRetrieveUpdateDeleteView.as_view()),
   path('payment_card/<int:pk>/tokenize', PaymentCardAuthView.as_view()),

   path('invoice/confirm', PaymentConfirmListCreateView.as_view()),
   path('invoice/<int:pk>/confirm', PaymentManualConfirmListCreateView.as_view()),
   path('invoice/<int:pk>/download', InvoicePDFView.as_view()),

   path('package_list', PackageListCreateView.as_view()),
   path('starter_price_list', PriceListCreateView.as_view()),
   path('payment_list', PaymentListCreateView.as_view()),

   # Billing
   path('billing/current_plan', BillingCurrentPlanCreateView.as_view()),
   path('billing/add_sales', PaymentTransferListCreateView.as_view()),
   path('billing/history', BillingHistoryCreateView.as_view()),
   path('billing/history/<int:pk>', BillingHistoryRetrieveUpdateDeleteView.as_view()),
   path('billing/history/<int:pk>/download', InvoicePDFView.as_view()),
   path('billing/upgrade_plan', BillingUpgradeCreateView.as_view()),

   path('billing/user_active_notif', UserNotifView.as_view()),


   path('metadata', PaymentMetadata.as_view()),
   path('cek/payment_status', CekPayment.as_view()),

]
