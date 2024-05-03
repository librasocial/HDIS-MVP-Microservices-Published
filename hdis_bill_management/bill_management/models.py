import uuid
from django.db import models
from django.core.validators import MinValueValidator

class DiscountType(models.IntegerChoices):
    Amount = 1
    Percentage = 2


class Bill(models.Model):
    """Represents a combination of Bill and Payment details for a specific Facility and Patient."""

    class PaymentType(models.IntegerChoices):
        Cash = 1
        Credit = 2

    class Status(models.IntegerChoices):
        Closed = 0
        Open = 1

    bill_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    #MDDS 05.07.0001
    facility_id = models.UUIDField()
    patient_id = models.CharField(max_length=18)
    resource_id = models.CharField(max_length=64)
    bill_date = models.DateField()    #MDDS 05.007.0002    #TODO: Use to deduct from older advance deposit if multiple open (lower priority)
    bill_generation_type = models.PositiveSmallIntegerField()    #MDDS 05.007.0003 (1=Summary Bill, 2=Detailed Bill)
    bill_copy_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.007.0004 (Values 1 to 6)
    reason_for_duplicate_bill_copy = models.CharField(max_length=254, blank=True, null=True)    #MDDS 05.007.0005
    approval_indicator_for_duplicate_bill_copy = models.BooleanField(blank=True, null=True)    #MDDS 05.007.0006
    tariff_category = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.007.0007 (Values 1 to 7)
    payment_type = models.PositiveSmallIntegerField(choices=PaymentType.choices, blank=True, null=True)    #MDDS 05.007.0009 (1=Cash, 2=Credit)
    payment_mode = models.IntegerField(blank=True, null=True)    #Non-MDDS (1=DebitCard, 2=CreditCard, 3=UPI, 4=Wallet, 5=NEFT, 6=IMPS, etc.)
    bill_status = models.PositiveSmallIntegerField(choices=Status.choices)    #Non-MDDS (0=Closed, 1=Open)
    sponsoring_entity = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.007.0010, CD05.141 (2-digit code)
    approving_entity = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.007.0011 (May be different from Sponsoring Entity)
    sponsor_approval_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.007.0014 (Are apporvals received in case Sponsor is other than self)
    maximum_eligibility_limit = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                    validators=[MinValueValidator(0.0)])    #MDDS 05.007.0015 (for hospitalization Episode or Encounter)
    eligibility_sub_limits = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                 validators=[MinValueValidator(0.0)])    #MDDS 05.007.0016 (for major services like Room Rent)
    eligibility_remarks = models.CharField(max_length=254, blank=True, null=True)    #MDDS 05.007.0017
    total_billed_amount = models.DecimalField(max_digits=10, decimal_places=2,  
                                              validators=[MinValueValidator(0.0)])    #MDDS 05.007.0024
    discount_approval_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.007.0025 (0=No, 1=Yes)
    discount_approver_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.007.0026 (Approving Authority)
    discount_type = models.PositiveSmallIntegerField(choices=DiscountType.choices, blank=True, null=True)    #MDDS 05.007.0027 (1-Amount, 2-Percentage)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                   validators=[MinValueValidator(0.0)])    #MDDS 05.007.0028; Note: Discount applicable at Bill and Item levels
    discount_remark = models.CharField(max_length=255, blank=True, null=True)    #MDDS 05.007.00029
    advance_deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                 validators=[MinValueValidator(0.0)])    #MDDS 05.007.0030; Bill to be generated for Advance payment - may be specific to Service Type / ID; TODO: Validity period for deposit? Refund of deposit?
    balance_payable = models.DecimalField(max_digits=10, decimal_places=2, 
                                          validators=[MinValueValidator(0.0)])    #MDDS 05.007.0031; TODO: Check whether Net payable amount is after discounts or deductions against advance as per LSRF docs.
    amount_payable_by_patient = models.DecimalField(max_digits=10, decimal_places=2, 
                                                    validators=[MinValueValidator(0.0)])    #MDDS 05.007.0032 (per sub-limit caps & other applicable clauses)
    amount_payable_by_sponsor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                    validators=[MinValueValidator(0.0)])    #MDDS 05.007.0033 (applicable if Sponsor is not Self)
    amount_paid_by_patient = models.DecimalField(max_digits=10, decimal_places=2, default=0, 
                                                 validators=[MinValueValidator(0.0)])    #MDDS 05.007.0034
    amount_paid_by_sponsor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                 validators=[MinValueValidator(0.0)])    #Non-MMDS; Cannot be greater than amount_payable_by_sponsor
    transaction_id = models.CharField(max_length=18, blank=True, null=True)    #MDDS 05.007.0036 (for relevant Payment Modes)
    #TODO: Service cancellation / refund - OOS for MVP?
    
    class Meta:
        verbose_name = 'Bill'
        verbose_name_plural = 'Bills'
        db_table = 'bill'
    def __str__(self):
        return str(self.primary_key)


class BillItem(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT, related_name='bill_items')
    service_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.007.0008, CD05.080 (2-digit code)
    service_id = models.UUIDField(blank=True, null=True)    #Non-MDDS; Reference to Service Master
    service_item_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.007.0018/0020, CD05.027/028
    service_item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                             validators=[MinValueValidator(0.0)])    #MDDS 05.007.0019/021, CD05.027/028 (per applicable unit of measurement)
    quantity_of_service = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.007.0022 (e.g. 5 days of stay, 10 units of blood) TODO: Check if type should be numeric with Unit separate
    quantity_of_service_unit = models.IntegerField(blank=True, null=True)    #Non-MDDS TODO: Create master table within Service Master and sync code
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                              validators=[MinValueValidator(0.0)])    #MDDS 05.007.0023
    discount_approval_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.007.0025 (0=No, 1=Yes)
    discount_approver_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.007.0026 (Approving Authority)
    discount_type = models.PositiveSmallIntegerField(choices=DiscountType.choices, blank=True, null=True)    #MDDS 05.007.0027 (1-Amount, 2-Percentage)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                   validators=[MinValueValidator(0.0)])    #MDDS 05.007.0028
    discount_remarks = models.CharField(max_length=255, blank=True, null=True)    #MDDS 05.007.0029
    subtotal = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0.0)])    #Non-MDDS - check if this can be removed

    class Meta:
        verbose_name = 'Bill Item'
        verbose_name_plural = 'Bill Items'
        db_table = 'bill_item'
    def __str__(self):
        return str(self.primary_key)


class SourceOfPaymentDetails(models.Model):
    """Applicable when Sponsor of a Patient's Bill is an Insurance Company."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    tpa_code = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0001, CD05.118 (IRDA-issued license number)
    tpa_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.006.0002, CD05.118
    insured_card_id = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.006.0003
    insurance_policy_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0004 (1=Individual, 2=Group)
    health_plan_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0005, CD05.014 (1-digit regulatory classification)
    insurance_company_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.007.0012, CD05.119
    insurance_company_code = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.007.0013, CD05.119 (3-digit code applicable when Sponsoring Entity is an insurance company)
    insurance_policy_id = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.006.0006
    insurance_policy_name = models.CharField(max_length=99, blank=True, null=True)    #MDDS 05.006.0007
    source_of_payment_code = models.CharField(max_length=2, blank=True, null=True)    #MDDS 05.006.0008, CD05.141 (2-chrarcter code)
    secondary_policy_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.006.0009
    secondary_policy_id = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.006.0010
    family_physician_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.006.0011
    proposed_line_of_treatment = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0012, CD05.125 (For preauthorization request)
    substance_abuse_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.006.0013
    expected_hospitalization_duration = models.DurationField(blank=True, null=True)    #MDDS 05.006.0014
    estimated_cost_of_hospitalization = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                            validators=[MinValueValidator(0.0)])    #MDDS 05.006.015
    commencement_of_first_insurance = models.DateField(blank=True, null=True)    #MDDS 05.006.016 (Date of Commencement of First Insurance Without Break)
    past_policy_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.006.0017 (Past Health Insurance Policy Indicator)
    room_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0018, CD05.068 (2-digit code)
    cause_of_hospitalization = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0019 (1=Injury, 2=Illness, 3=Maternity)
    claim_expenses_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0020 (Values 1 to 6)
    total_claimed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                               validators=[MinValueValidator(0.0)])    #MDDS 05.006.021
    pre_hospitalization_period = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0022 (in days)
    post_hospitalization_period = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0023 (in days)
    additional_benefit_types_claimed = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0024 (Values 1 to 6)
    total_additional_benefits_claimed_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, 
                                                                   validators=[MinValueValidator(0.0)])    #MDDS 05.006.025
    bill_type = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0027 (Values 1 to 5)
    type_of_hospital = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0028 (1=Network, 2=Non Network)
    pre_authorization_indicator = models.BooleanField(blank=True, null=True)    #MDDS 05.006.0029
    pre_authorization_id = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.006.0030
    insurance_coverage_start_date = models.DateField(blank=True, null=True)    #MDDS 05.006.0031
    insurance_coverage_end_date = models.DateField(blank=True, null=True)    #MDDS 05.006.0032
    claims_documents_submission_check_list = models.PositiveSmallIntegerField(blank=True, null=True)    #MDDS 05.006.0033, CD05.029 (2-digit code)
    patient_employee_id = models.CharField(max_length=50, blank=True, null=True)    #MDDS 05.006.0034 (assigned by employer)

    class Meta:
        verbose_name = 'Source Of Payment Detail'
        verbose_name_plural = 'Sources of Payment Detail'
        db_table = 'source_of_payment_detail'
    def __str__(self):
        return str(self.primary_key)

# TODO: Related bills for multiple deductions against an advance deposit.

# TODO: Auto-post from Service Master in response to Business Events. Tax lookup mandatory and not dependent on any input.
# Amounts and Discount related fields must be provided by the caller.
# Check open bills to determine balance for Patient.