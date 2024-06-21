import datetime
import uuid

from generator.base_data import BaseData
from faker import Faker
from generator.setup import Setup
import faker.providers
import numpy


class BasicParty(BaseData):

    NAME= "01-basic-party"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicParty.NAME)
        self.fake=Faker(['en_US'])

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):
        """
        Generate one item
        """

        model=self.model_item()

        # "name": "party_id",
        # "description": "Unigue party identificator",
        model['party_id']=str(uuid.uuid4())

        # "name": "party_establishment",
        # "description": "Date of establishment of the party (e.g. birthday for client, etc.)",
        model['party_establishment']=self.fake.date_of_birth(minimum_age=15, maximum_age= 100)

        # "name": "party_type",
        # "description": "Party state (e.g. 1. lead, 2. prospect, 3. client)",
        model['party_type']=self.rnd_choose(["Lead", "Prospect", "Customer"], [0.5, 0.3, 0.2])
        self.apply_none_value(model,'party_type',"Lead")

        # "name": "party_typedate",
        # "description": "Date for party type creation (data for change of the state to the prospect or client)",
        # Note: party_typedate, max old 1985-01-01
        max_old = datetime.date(1985,1,1)
        if model['party_establishment'] > max_old:
            model['party_typedate']=self.fake.date_between_dates(model['party_establishment'],datetime.date.today())
        else:
            model['party_typedate']=self.fake.date_between_dates(max_old, datetime.date.today())

        # "name": "party_gender",
        # "description": "Party gender ('F' or 'M')",
        model['party_gender']=self.rnd_choose(["F", "M"], [0.6, 0.4])

        # "name": "party_education",
        # "description": "Party education (e.g. 'Elementary school', 'High school', 'University', etc.)",
        model['party_education']=self.rnd_choose(["Elementary school", "High school", "University"], [0.5, 0.4, 0.1])
        self.apply_none_value(model,'party_education', "Elementary school")

        # "name": "party_familystatus",
        # "description": "Family status for party ('Married','Single', 'Divorced')",
        model['party_familystatus']=self.rnd_choose(["Married", "Single", "Divorced"], [0.5, 0.4, 0.1])

        # "name": "party_nchild",
        # "description": "Count of children",
        model['party_nchild']=self.rnd_choose(range(0, 4), [0.05, 0.6, 0.3, 0.05])

        # "name": "party_industry",
        # "description": "Party industry (e.g. 'IT', 'Finance', 'Telco', 'Medical', etc.)",
        model['party_industry']=self.rnd_choose(
            ["IT", "Financial services", "Telcommunications", "Industry", "Mining", "Aerospace",
             "Medical services", "Education", "Food industry", "Real Estate",
             "Social services", "Agriculture", "Transport", "Public administration"])

        # "name": "party_industryposition",
        # "description": "Party position in industry (e.g. 'Manager', 'Developer', 'Analyst', etc.)",
        model['party_industryposition']=self.rnd_choose(
            ["Owner", "Director", "Manager", "Architect",
             "Developer", "Analyst", "Tester",
             "Teacher", "Professor", "Lawyer", "Auditor", "Economist",
             "Accountant", "Driver", "Receptionist", "Sales",
             "Secretary", "Cashier",
             "Plumber", "Laborer", "Electrician"],
            [0.001, 0.002, 0.006, 0.002,  # 0.011
             0.02, 0.02, 0.02,  # 0.06
             0.01, 0.01, 0.01, 0.01, 0.05,  # 0.09
             0.12, 0.12, 0.1, 0.12, 0.1, 0.1,  # 0.66]))
             0.05, 0.079, 0.05])  # 0.179

        # "name": "party_residencecountry",
        # "description": "Party country residence",
        model['party_residencecountry']=self.fake.country()

        # "name": "party_city",
        # "description": "Permanent stay-city (part of permanent stay)",
        model['party_city']=self.fake.city()

        # "name": "party_income",
        # "description": "Monthly income in local currency",
        model['party_income']=self.rnd_choose(range(50, 200)) * 1000

        # "name": "party_incometype",
        # "description": "Type of the main income (e.g. 'Earned', 'Passive', 'Portfolio')",
        model['party_incometype']=self.rnd_choose(["Earned", "Passive", "Portfolio"], [0.96, 0.02, 0.02])

        # "name": "party_peoplehousehold",
        # "description": "Number of people in household",
        model['party_peoplehousehold']=model['party_nchild'] + self.rnd_choose(range(1, 4), [0.05, 0.9, 0.05])

        # "name": "party_incomehousehold",
        # "description": "Monthly income in local currency for household",
        model['party_incomehousehold']=round(model['party_income'] * self.rnd_choose(range(10, 30)) / 10)

        # "name": "party_expenseshousehold",
        # "description": "Monthly expenses (insurence, loans, etc.) for household",
        model['party_expenseshousehold']=round(model['party_incomehousehold'] * self.rnd_choose(range(10, 50)) / 100)

        # "name": "party_currency",
        # "description": "Party currency (USD, EUR)",
        model['party_currency']=self.rnd_choose(["USD", "EUR"], [0.95, 0.05])

        # "name": "party_note",
        # "description": "Party note",
        model['party_note'] = ""

        # "name": "record-date",
        # "description": "The date when the record was created",
        model['record_date']=self.gmodel["NOW"]

        self.model.append(model)
