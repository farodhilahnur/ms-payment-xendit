import django
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from .utils import get_uuid

# Create your models here.

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(db_column='email', max_length=1000, blank=True, null=True,  verbose_name='Email')
    invoice_number = models.CharField(db_column='invoice_number',  max_length=1000, blank=True, null=True, verbose_name='Invoice number')
    package = models.CharField(db_column='package', max_length=1000, blank=True, null=True,  verbose_name='Package') 
    plan = models.CharField(db_column='plan', max_length=1000, blank=True, null=True,  verbose_name='plan')
    payment_type = models.CharField(db_column='payment_type', max_length=1000, blank=True, null=True,  verbose_name='Payment type')
    payment_status = models.CharField(db_column='payment_status', max_length=1000, default='pending', blank=True, null=True, verbose_name='Payment Status') 
    payment_date = models.DateTimeField(db_column='payment_date', blank=True, null=True, verbose_name='Payment Date')
    total_user = models.IntegerField(db_column='total_user', blank=True, null=True,  verbose_name='total user')
    total_price_user = models.BigIntegerField(db_column='total_price_user',  blank=True, null=True, verbose_name='Total Price User')
    tax = models.IntegerField(db_column='tax',  blank=True, null=True, verbose_name='Tax')
    on_boarding_service = models.BooleanField(db_column='on_boarding_service', default=False, verbose_name='On boarding service')
    sub_total = models.BigIntegerField(db_column='sub_total', blank=True, null=True,  verbose_name='Sub total')
    total_amount = models.BigIntegerField(db_column='total_amount',  blank=True, null=True, verbose_name='Total amount')
    expired_date = models.DateTimeField(db_column='expired_date', blank=True, null=True, verbose_name='Expiration Date')
    status = models.CharField(db_column='status', max_length=1000, default='running', blank=True, null=True, verbose_name='Status') 
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    update_core = models.BooleanField(db_column='update_core', default=False, verbose_name='update core')
    account_expired = models.DateTimeField(db_column='account_expired', blank=True, null=True, verbose_name='Expiration account')

    class Meta:
        db_table = 'tbl_invoice'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(Invoice, self).save(*args, **kwargs)

class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, db_column='invoice_id', blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(db_column='email', max_length=1000, blank=True, null=True,  verbose_name='Email')
    payment_type = models.CharField(db_column='payment_type', max_length=1000, blank=True, null=True,  verbose_name='Payment type')
    bank = models.CharField(db_column='bank', max_length=1000, blank=True, null=True,  verbose_name='Bank')
    virtual_account = models.IntegerField(db_column='virtual_account', blank=True, null=True,  verbose_name='Virtual Account')
    time_remaining = models.CharField(db_column='time_remaining', max_length=1000, blank=True, null=True,  verbose_name='Time remaining')
    total_amount = models.BigIntegerField(db_column='total_amount',  blank=True, null=True, verbose_name='Total amount')
    first_name = models.CharField(db_column='first_name', max_length=1000, blank=True, null=True,  verbose_name='First name')
    last_name = models.CharField(db_column='last_name', max_length=1000, blank=True, null=True,  verbose_name='Last name')
    card_number = models.IntegerField(db_column='card_number', blank=True, null=True,  verbose_name='Card number')
    valid_thru = models.CharField(db_column='valid_thru', max_length=1000, blank=True, null=True,  verbose_name='Valid thru')
    cvv = models.IntegerField(db_column='cvv', blank=True, null=True,  verbose_name='Cvv')
    otp = models.IntegerField(db_column='otp', blank=True, null=True,  verbose_name='Otp')
    status = models.CharField(db_column='status', max_length=1000, default='pending', blank=True, null=True, verbose_name='Status') 
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
 
    class Meta:
        db_table = 'tbl_payment'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(Payment, self).save(*args, **kwargs)

class PaymentTransfer(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, db_column='invoice_id', blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(db_column='email', max_length=1000, blank=True, null=True,  verbose_name='Email')
    payment_type = models.CharField(db_column='payment_type', max_length=1000, blank=True, null=True,  verbose_name='Payment type')
    bank = models.CharField(db_column='bank', max_length=1000, blank=True, null=True,  verbose_name='Bank')
    virtual_account = models.BigIntegerField(db_column='virtual_account', blank=True, null=True,  verbose_name='Virtual Account')
    expired_date = models.DateTimeField(db_column='expired_date', blank=True, null=True,  verbose_name='expired_date')
    expired = models.DateTimeField(db_column='expired', blank=True, null=True,  verbose_name='expired')
    transaction_time = models.DateTimeField(db_column='transaction_time', blank=True, null=True,  verbose_name='transaction time')
    total_amount = models.BigIntegerField(db_column='total_amount',  blank=True, null=True, verbose_name='Total amount')
    status = models.CharField(db_column='status', max_length=1000, default='pending', blank=True, null=True, verbose_name='Status') 
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    order_id = models.CharField(db_column='order_id', max_length=1000, blank=True, null=True,  verbose_name='order id')
    transaction_id = models.CharField(db_column='transaction_id', max_length=1000, blank=True, null=True,  verbose_name='transaction id')
    bill_key = models.CharField(db_column='bill_key', max_length=1000, blank=True, null=True,  verbose_name='bill key')
    biller_code = models.CharField(db_column='biller_code', max_length=1000, blank=True, null=True,  verbose_name='biller_code')

    class Meta:
        db_table = 'tbl_payment_transfer'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(PaymentTransfer, self).save(*args, **kwargs)

class PaymentCard(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, db_column='invoice_id', blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(db_column='email', max_length=1000, blank=True, null=True,  verbose_name='Email')
    payment_type = models.CharField(db_column='payment_type', max_length=1000, blank=True, null=True,  verbose_name='Payment type')
    first_name = models.CharField(db_column='first_name', max_length=1000, blank=True, null=True,  verbose_name='First name')
    last_name = models.CharField(db_column='last_name', max_length=1000, blank=True, null=True,  verbose_name='Last name')
    card_number = models.BigIntegerField(db_column='card_number', blank=True, null=True,  verbose_name='Card number')
    mask_card_number = models.CharField(db_column='mask_card_number', max_length=1000, blank=True, null=True,  verbose_name='Mask Card number')
    valid_thru = models.CharField(db_column='valid_thru', max_length=1000, blank=True, null=True,  verbose_name='Valid thru')
    cvv = models.IntegerField(db_column='cvv', blank=True, null=True,  verbose_name='Cvv')
    total_amount = models.BigIntegerField(db_column='total_amount',  blank=True, null=True, verbose_name='Total amount')
    payer_authentication_url = models.CharField(db_column='payer_authentication_url', max_length=1000, blank=True, null=True,  verbose_name='payer authentication url')
    order_id = models.CharField(db_column='order_id', max_length=1000, blank=True, null=True,  verbose_name='order id')
    token_id = models.CharField(db_column='token_id', max_length=1000, blank=True, null=True,  verbose_name='token id')
    charge_id = models.CharField(db_column='charge_id', max_length=1000, blank=True, null=True,  verbose_name='charge id')
    charge_status = models.CharField(db_column='charge_status', max_length=1000, blank=True, null=True,  verbose_name='charge status')
    status = models.CharField(db_column='status', max_length=1000, default='pending', blank=True, null=True, verbose_name='Status')
    expired_date = models.DateTimeField(db_column='expired_date', blank=True, null=True,  verbose_name='expired_date')
    expired = models.DateTimeField(db_column='expired', blank=True, null=True,  verbose_name='expired')
    transaction_time = models.DateTimeField(db_column='transaction_time', blank=True, null=True,  verbose_name='transaction time')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    card_data = models.JSONField(blank=True, null=True)
    bank = models.CharField(db_column='bank', max_length=1000, blank=True, null=True,  verbose_name='Bank')
    brand = models.CharField(db_column='brand', max_length=1000, blank=True, null=True,  verbose_name='Brand')

    class Meta:
        db_table = 'tbl_payment_card'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(PaymentCard, self).save(*args, **kwargs)

class Setting(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(db_column='type', max_length=1000, blank=True, null=True,  verbose_name='type')
    priceuser = models.BigIntegerField(db_column='price_user', blank=True, null=True,  verbose_name='price user')
    periode = models.CharField(db_column='periode', max_length=1000, blank=True, null=True,  verbose_name='periode')
    name = models.CharField(db_column='name', max_length=1000, blank=True, null=True,  verbose_name='name')
    plan = models.CharField(db_column='plan', max_length=1000, blank=True, null=True,  verbose_name='plan')
    picture = models.CharField(db_column='picture', max_length=1000, blank=True, null=True,  verbose_name='picture')
    bank = models.CharField(db_column='bank', max_length=1000, blank=True, null=True,  verbose_name='Bank')
    bank_account_name = models.CharField(db_column='bank_account_name', max_length=1000, blank=True, null=True, verbose_name='name')
    bank_account_number = models.BigIntegerField(db_column='bank_account_number', blank=True, null=True, verbose_name='nomor rekening')
    
    class Meta:
        db_table = 'tbl_setting'
    def save(self, *args, **kwargs):
        return super(Setting, self).save(*args, **kwargs)

class PaymentTransferManual(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, db_column='invoice_id', blank=True, null=True, on_delete=models.CASCADE)
    email = models.CharField(db_column='email', max_length=1000, blank=True, null=True,  verbose_name='Email')
    bank_account_name = models.CharField(db_column='bank_account_name', max_length=1000, blank=True, null=True, verbose_name='name')
    bank_account_number = models.BigIntegerField(db_column='bank_account_number', blank=True, null=True, verbose_name='nomor rekening')
    payment_type = models.CharField(db_column='payment_type', max_length=1000, blank=True, null=True,  verbose_name='Payment type')
    bank = models.CharField(db_column='bank', max_length=1000, blank=True, null=True,  verbose_name='Bank')
    expired_date = models.DateTimeField(db_column='expired_date', blank=True, null=True,  verbose_name='expired_date')
    transaction_time = models.DateTimeField(db_column='transaction_time', blank=True, null=True, default=django.utils.timezone.now, verbose_name='transaction time')
    total_amount = models.BigIntegerField(db_column='total_amount',  blank=True, null=True, verbose_name='Total amount')
    status = models.CharField(db_column='status', max_length=1000, default='pending', blank=True, null=True, verbose_name='Status') 
    proof = models.CharField(db_column='proof', max_length=1000, blank=True, null=True, verbose_name='Proof')
    createdAt = models.DateTimeField(db_column='createdAt', blank=True, null=True, default=django.utils.timezone.now, verbose_name='Created At')
    createdBy = models.IntegerField(db_column='createdBy', blank=True, null=True,  verbose_name='Created By')
    modifiedAt = models.DateTimeField(db_column='modifiedAt', blank=True, null=True,  verbose_name='Modified At')
    modifiedBy = models.IntegerField(db_column='modifiedBy', blank=True, null=True,  verbose_name='Modified By')
    accountId = models.IntegerField(db_column='accountId', blank=True, null=True,  verbose_name='Account Id')
    
    class Meta:
        db_table = 'tbl_payment_manual'
    def save(self, *args, **kwargs):
        self.modifiedAt = timezone.now()
        return super(PaymentTransferManual, self).save(*args, **kwargs)