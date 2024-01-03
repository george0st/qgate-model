import datetime
import uuid

from generator.base import Base
from faker import Faker
import faker.providers
import numpy


class BasicParty(Base):

    NAME= "01-basic-party"

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicParty.NAME)
        self.fake=Faker(['en_US'])

    @property
    def name(self):
        return BasicParty.NAME

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):
        """
        Generate one item
        """

        model=self.model_item()

        # "name": "party-id",
        # "description": "Unigue party identificator",
        model['party-id']=str(uuid.uuid4())

        # "name": "party-establishment",
        # "description": "Date of establishment of the party (e.g. birthday for client, etc.)",
        model['party-establishment']=self.fake.date_of_birth(minimum_age=15, maximum_age= 100)

        # "name": "party-type",
        # "description": "Party state (e.g. 1. lead, 2. prospect, 3. client)",
        model['party-type']=self.rnd_choose(["Lead", "Prospect", "Customer"], [0.5, 0.3, 0.2])

        # "name": "party-typedate",
        # "description": "Date for party type creation (data for change of the state to the prospect or client)",
        # Note: party-typedate, max old 1985-01-01
        max_old = datetime.date(1985,1,1)
        if model['party-establishment'] > max_old:
            model['party-typedate']=self.fake.date_between_dates(model['party-establishment'],datetime.date.today())
        else:
            model['party-typedate']=self.fake.date_between_dates(max_old, datetime.date.today())

        # "name": "party-gender",
        # "description": "Party gender ('F' or 'M')",
        model['party-gender']=self.rnd_choose(["F", "M"], [0.6, 0.4])

        # "name": "party-education",
        # "description": "Party education (e.g. 'Elementary school', 'High school', 'University', etc.)",
        model['party-education']=self.rnd_choose(["Elementary school", "High school", "University"], [0.5, 0.4, 0.1])

        # "name": "party-familystatus",
        # "description": "Family status for party ('Married','Single', 'Divorced')",
        model['party-familystatus']=self.rnd_choose(["Married", "Single", "Divorced"], [0.5, 0.4, 0.1])

        # "name": "party-nchild",
        # "description": "Count of children",
        model['party-nchild']=self.rnd_choose(range(0, 4), [0.05, 0.6, 0.3, 0.05])

        # "name": "party-industry",
        # "description": "Party industry (e.g. 'IT', 'Finance', 'Telco', 'Medical', etc.)",
        model['party-industry']=self.rnd_choose(
            ["IT", "Financial services", "Telcommunications", "Industry", "Mining", "Aerospace",
             "Medical services", "Education", "Food industry", "Real Estate",
             "Social services", "Agriculture", "Transport", "Public administration"])

        # "name": "party-industryposition",
        # "description": "Party position in industry (e.g. 'Manager', 'Developer', 'Analyst', etc.)",
        model['party-industryposition']=self.rnd_choose(
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

        # "name": "party-residencecountry",
        # "description": "Party country residence",
        model['party-residencecountry']=self.fake.country()

        # "name": "party-city",
        # "description": "Permanent stay-city (part of permanent stay)",
        model['party-city']=self.fake.city()

        # "name": "party-income",
        # "description": "Monthly income in local currency",
        model['party-income']=self.rnd_choose(range(50, 200)) * 1000

        # "name": "party-incometype",
        # "description": "Type of the main income (e.g. 'Earned', 'Passive', 'Portfolio')",
        model['party-incometype']=self.rnd_choose(["Earned", "Passive", "Portfolio"], [0.96, 0.02, 0.02])

        # "name": "party-peoplehousehold",
        # "description": "Number of people in household",
        model['party-peoplehousehold']=model['party-nchild'] + self.rnd_choose(range(1, 4), [0.05, 0.9, 0.05])

        # "name": "party-incomehousehold",
        # "description": "Monthly income in local currency for household",
        model['party-incomehousehold']=round(model['party-income'] * self.rnd_choose(range(10, 30)) / 10)

        # "name": "party-expenseshousehold",
        # "description": "Monthly expenses (insurence, loans, etc.) for household",
        model['party-expenseshousehold']=round(model['party-incomehousehold'] * self.rnd_choose(range(10, 50)) / 100)

        # "name": "party-currency",
        # "description": "Party currency (USD, EUR)",
        model['party-currency']=self.rnd_choose(["USD", "EUR"], [0.95, 0.05])

        # "name": "record-date",
        # "description": "The date when the record was created",
        model['record-date']=self.gmodel["NOW"]

        self.model.append(model)
