import datetime
import uuid
from generator.base_data import BaseData
from faker import Faker
from generator.basic_account import BasicAccount


class BasicTransaction(BaseData):

    NAME= "05-basic_transaction"
    MAX_EVENT_HISTORY_MONTHS = 3*12     # 3 years as default, in case of value '0' or '-1', it is without limit

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicTransaction.NAME)
        self.fake = Faker(['en_US'])
        self.fake_at = Faker(['de_AT'])
        self.fake_de = Faker(['de_DE'])
        self.fake_ch = Faker(['de_CH'])
        self.fake_pl = Faker(['pl_PL'])
        self.fake_it = Faker(['it_IT'])
        self.fake_es = Faker(['es_ES'])
        self.fake_tr = Faker(['tr_TR'])
        self.fake_az = Faker(['az_AZ'])
        self.fake_ru = Faker(['ru_RU'])

    def change_date(self, year, month, day, months_to_add):
        """Change date, add month"""
        # https://www.geeksforgeeks.org/add-months-to-datetime-object-in-python/
        new_date = datetime.date(year + (month + months_to_add - 1) // 12,
                            (month + months_to_add - 1) % 12 + 1,
                            day)
        return new_date

    def generate(self, count):

        # reference to the data from BasicAccount
        accounts = self.gmodel[BasicAccount.NAME]

        # iteration cross all accounts
        for account in accounts:

            date_from=account['account_createdate']

            if account['account_nonactivedate'] == self.MAX_DATE:
                date_to=datetime.date.today()
            else:
                date_to=account['account_nonactivedate']

            dif_date=round((date_to-date_from).days/30)

            # apply limit for max history
            if self.MAX_EVENT_HISTORY_MONTHS > 0:
                if dif_date > self.MAX_EVENT_HISTORY_MONTHS:
                    dif_date = self.MAX_EVENT_HISTORY_MONTHS

            for month in range(dif_date):
                # INCOME - regular income (0..1 times)
                for _ in range(int(self.rnd_choose([0,1],[0.001, 0.999]))):
                    new_date=self.change_date(date_to.year,
                                              date_to.month,
                                              int(self.rnd_int(1,21)),
                                              - month)
                    if new_date > date_to:
                        continue
                    self.model.append(self._create_transaction(account, new_date, True, 1500, 5000))

                # INCOME - addition income (0..2 times)
                for _ in range(int(self.rnd_choose([0,1,2],[0.9, 0.08, 0.02]))):
                    new_date = self.change_date(date_to.year,
                                                date_to.month,
                                                int(self.rnd_int(1, 29)),
                                                - month)
                    if new_date > date_to:
                        continue
                    self.model.append(self._create_transaction(account, new_date, True, 500, 2500))

                # OUTCOME - typical outcome (0..5 times)
                for _ in range(int(self.rnd_choose([0,1,2,3,4,5],[0.002, 0.6, 0.2, 0.13, 0.05, 0.018]))):
                    new_date = self.change_date(date_to.year,
                                                date_to.month,
                                                int(self.rnd_int(1, 29)),
                                                - month)
                    if new_date > date_to:
                        continue
                    self.model.append(self._create_transaction(account, new_date, False, 300, 800))

    def _create_transaction(self, account, new_date, income, finance_min = 1500, finance_max = 5000):
        model = self.model_item()

        # "name": "transaction_id",
        # "description": "Unique transaction identificator",
        model['transaction_id'] = str(uuid.uuid4())

        # "name": "account_id",
        # "description": "Relation to account identificator",
        model['account_id'] = account['account_id']

        # "name": "transaction_direction",
        # "description": "Transaction direction e.g. incoming, outgoing",
        model['transaction_direction'] = "Incoming" if income else "Outgoing"

        # "name": "transaction_type",
        # "description": "Transaction type",
        model['transaction_type'] = self.rnd_choose(["Standard", "Instant"], [0.7, 0.3])
        self.apply_none_value(model, 'transaction_type', "Instant", probability_multiplicator=0.25)

        # "name": "transaction_value",
        # "description": "Transaction value",
        model['transaction_value'] = self.rnd_choose(range(finance_min, finance_max))

        # "name": "transaction_currency",
        # "description": "Transaction currency",
        model['transaction_currency'] = "USD"

        # "name": "transaction_description",
        # "description": "Transaction description (note: empty value is valid)",
        model["transaction_description"] = self._transaction_description(income)

        # "name": "transaction_date",
        # "description": "Transaction date",
        model['transaction_date'] = new_date

        # "name": "counterparty_name",
        # "description": "Transaction counterparty name",
        model["counterparty_name"] = self.fake.name()

        # "name": "counterparty_iban",
        # "description": "Transaction counterparty IBAN",
        if int(self.rnd_choose([0, 1], [0.998, 0.002])) == 0:
            iban = self.fake.iban()
        else:
            tmp_fake = self.rnd_choose([self.fake_at, self.fake_de, self.fake_ch,
                                        self.fake_pl, self.fake_it, self.fake_es,
                                        self.fake_tr, self.fake_az, self.fake_ru],
                                       [0.3, 0.2, 0.2, 0.1, 0.1, 0.025, 0.025, 0.025, 0.025])
            iban = tmp_fake.iban()
        model["counterparty_iban"] = iban

        # "name": "counterparty_other",
        # "description": "Transaction counterparty other information",
        # TODO: Add relevant value
        model["counterparty_other"] = ""

        fraud = False
        fraud_anomaly = 0
        if self.rnd_choose([False, True], [0.95, 0.05]):
            fraud_anomaly = self.rnd_float(0, 1, 4)
            if self.rnd_choose([False, True], [0.95, 0.05]):
                if self.rnd_bool():
                    fraud = True

        # "name": "transaction_fraudanomaly",
        # "description": "Possible fraud anomaly detection (min. 0 - without anomaly detection, max. 1)",
        model["transaction_fraudanomaly"] = float(fraud_anomaly)

        # "name": "transaction_fraud",
        # "description": "Identification of fraud (True - fraud, False - without fraud)",
        model["transaction_fraud"] = int(fraud)

        # "name": "record_date",
        # "description": "The date when the record was created",
        model['record_date'] = self.gmodel["NOW"]

        return model

    def _transaction_description(self, income=True, probability_empty=0.25, probability_fake=0.1):
        option = self.rnd_choose([0, 1, 2],
                                 [probability_empty, probability_fake, 1 - probability_empty - probability_fake])
        if option==0:   # empty description
            return ""
        elif option==1: # fake description
            return self.fake.text(max_nb_chars=64)

        # real description
        if income:
            return self.TRANSACTION_INCOME_DESCRIPTION[self.rnd_int(0, len(self.TRANSACTION_INCOME_DESCRIPTION))]
        return self.TRANSACTION_OUTCOME_DESCRIPTION[self.rnd_int(0, len(self.TRANSACTION_INCOME_DESCRIPTION))]

    TRANSACTION_INCOME_DESCRIPTION = [
        "Salary Payment",
        "Freelance Project Payment - Website Design",
        "Dividend Income from Corp Shares",
        "Rental Income for Property",
        "Commission Income from Sales",
        "Payment for Tutoring Services Rendered",
        "Royalty Income from Book Sales",
        "Income from Online Course Sales",
        "Payment for Consulting Services Provided",
        "Ad Revenue from Blog",
        "Payment for Graphic Design Work",
        "Income from Artwork Sales",
        "Payment for Software Development Services",
        "Income from Rental Property",
        "Bonus Payment for Performance",
        "Payment for Legal Services Rendered",
        "Income from Patent Licensing",
        "Payment for Personal Training Services",
        "Ad Revenue from YouTube Channel",
        "Payment for Photography Services Provided",
        "Payment for Copywriting Services",
        "Income from Handmade Jewelry Sales",
        "Payment for Mobile App Development Services",
        "Income from Rental Property",
        "Profit Sharing Payment",
        "Payment for Accounting Services Rendered",
        "Income from Music Streaming Platforms",
        "Payment for Life Coaching Services",
        "Sponsorship Income for Podcast",
        "Payment for Interior Design Services Provided",
        "Payment for Translation Services",
        "Income from Craft Workshop Sales",
        "Income from Vacation Rental Property",
        "Incentive Payment for Sales Target Achievement",
        "Payment for Financial Advisory Services Rendered",
        "Income from eBook Sales",
        "Payment for Personal Chef Services",
        "Affiliate Marketing Income",
        "Payment for Architectural Design Services Provided",
        "Payment for Voice Over Services",
        "Income from Art Exhibition Sales",
        "Payment for Data Analysis Services",
        "Income from Commercial Rental Property",
        "Bonus Payment for Project Completion",
        "Payment for Tax Preparation Services Rendered",
        "Income from Self-Published Book Sales",
        "Payment for Personal Stylist Services",
        "E-commerce Store Sales Income",
        "Payment for Landscape Design Services Provided",
        "Payment for SEO Optimization Services",
        "Income from Antique Sales",
        "Payment for Cybersecurity Consulting Services",
        "Income from Residential Rental Property",
        "Performance Bonus Payment",
        "Payment for Real Estate Brokerage Services Rendered",
        "Income from Online Course Enrollment Fees",
        "Payment for Event Planning Services",
        "Dropshipping Sales Income",
        "Payment for Home Staging Services Provided",
        "Payment for Social Media Management Services",
        "Income from Vintage Clothing Sales",
        "Payment for IT Support Services",
        "Income from Farm Rental Property",
        "Referral Bonus Payment",
        "Payment for Career Coaching Services Rendered",
        "Income from Podcast Sponsorship Fees",
        "Payment for Wedding Planning Services",
        "Affiliate Marketing Income",
        "Payment for Personal Shopping Services Provided",
        "Payment for Content Writing Services",
        "Income from Artwork Commission Sales",
        "Payment for Network Setup Services",
        "Income from Commercial Space Leasing",
        "Sales Incentive Payment",
        "Payment for Nutrition Consulting Services Rendered",
        "Income from Webinar Registration Fees",
        "Payment for Personal Training Services",
        "E-commerce Sales Income",
        "Payment for Home Organization Services Provided",
        "Payment for Video Editing Services",
        "Income from Handcrafted Furniture Sales",
        "Payment for Cloud Migration Services",
        "Income from Storage Unit Rental",
        "Performance Bonus Payment",
        "Payment for Speech Therapy Services Rendered",
        "Income from Online Store Sales",
        "Payment for Event Photography Services",
        "Dropshipping Sales Income",
        "Payment for Home Cleaning Services Provided",
    ]

    TRANSACTION_OUTCOME_DESCRIPTION = [
        "Payment for Childcare",
        "Payment for Invoice",
        "Monthly subscription for Premium Plan",
        "Donation to Charity",
        "Refund for Order",
        "Electricity Bill Payment",
        "Annual Membership Renewal Fee",
        "Payment for Freelance Design Work",
        "Tuition Fee for Summer Semester",
        "Grocery Shopping",
        "Quarterly Rent Payment for Office Space",
        "Payment for Web Hosting Services",
        "Reimbursement for Business Travel Expenses",
        "Payment for Custom Software Development",
        "Water Bill Payment",
        "Payment for Legal Consultation Services",
        "Purchase of Office Supplies",
        "Payment for Advertising Services",
        "Health Insurance Premium",
        "Payment for Gym Membership",
        "Payment for Library Membership",
        "Payment for Annual Car Insurance",
        "Internet Service Bill",
        "Payment for Catering Services",
        "Commission Payment for Sales",
        "Payment for Home Cleaning Services",
        "Gas Bill Payment",
        "Payment for Photography Services",
        "Payment for Photography Services - Wedding",
        "Payment for Home Renovation Work",
        "Car Loan Installment",
        "Payment for Music Lessons",
        "Payment for Pet Grooming Services",
        "Cable TV Bill Payment",
        "Payment for Landscaping Services",
        "Payment for Pest Control Services",
        "Heating Bill Payment",
        "Payment for Event Planning Services - Conference",
        "Payment for Interior Design Services",
        "Mortgage Payment",
        "Payment for Art Classes",
        "Payment for Yoga Classes",
        "Payment for Yoga Private Training",
        "Payment for House Painting Services",
        "Payment for Dog Walking Services",
        "Trash Collection Bill Payment",
        "Payment for DJ Services - Party",
        "Payment for Home Security Services",
        "Payment for Private Security Services",
        "Student Loan Payment",
        "Payment for Dance Classes",
        "Payment for Personal Training Sessions",
        "Broadband Internet Bill Payment",
        "Payment for Roof Repair Services",
        "Payment for Babysitting Services",
        "Sewage and Wastewater Bill Payment",
        "Payment for Pool Maintenance Services",
        "Car Lease Payment",
        "Payment for Cooking Classes",
        "Payment for Language Tutoring",
        "Payment for Plumbing Services",
        "Royalty Payment for Book Sales",
        "Payment for Housekeeping Services",
        "Recycling Service Bill Payment",
        "Payment for Florist Services - Event",
        "Payment for Pest Control Services",
        "Credit Card Bill Payment",
        "Payment for Pottery Classes",
        "Landline Phone Bill Payment",
        "Payment for Electrical Services",
        "License Fee Payment for Software Use",
        "Payment for Dog Training Services",
        "Stormwater Service Bill Payment",
        "Payment for Makeup Artist Services - Event",
        "Payment for Gardening Services",
        "Home Loan Payment",
        "Payment for Personal Fitness Training",
        "Payment for Carpentry Services - Job",
        "Franchise Fee Payment for Business",
        "Payment for Cat Sitting Services",
        "Waste Management Service Bill Payment",
        "Payment for Event Management Services - Conference",
        "Payment for Home Insulation Services",
        "Car Insurance Payment",
        "Payment for Sculpture Classes",
        "Payment for Photography Lessons",
        "Payment for HVAC Services - Job",
        "Royalty Payment for Music Sales",
        "Payment for Horse Riding Lessons",
        "Snow Removal Service Bill Payment",
        "Payment for Hair Styling Services",
        "Payment for Chimney Cleaning Services",
        "Health Insurance Payment",
        "Payment for Drawing Classes",
        "Fine for speeding",
        "Parking fine",
        "Fine for bad vehicle condition",
    ]
