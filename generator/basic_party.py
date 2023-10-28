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
    def Name(self):
        return BasicParty.NAME

    def generate(self, count):
        for i in range(count):
            self._generate()

    def _generate(self):
        """
        Generate one item
        """

        # "name": "party-id",
        # "description": "Unigue party identificator",
        self.model['party-id'].append(str(uuid.uuid4()))

        # "name": "party-establishment",
        # "description": "Date of establishment of the party (e.g. birthday for client, etc.)",
        self.model['party-establishment'].append(self.fake.date_of_birth(minimum_age=15, maximum_age= 100))

        # "name": "party-type",
        # "description": "Party state (e.g. 1. lead, 2. prospect, 3. client)",
        self.model['party-type'].append(self.rnd_choose(["Lead", "Prospect", "Customer"], [0.5, 0.3, 0.2]))

        # "name": "party-typedate",
        # "description": "Date for party type creation (data for change of the state to the prospect or client)",
        # Note: party-typedate, max old 1985-01-01
        max_old = datetime.date(1985,1,1)
        if self.model['party-establishment'][-1] > max_old:
            self.model['party-typedate'].append(self.fake.date_between_dates(
                self.model['party-establishment'][-1],
                datetime.date.today()))
        else:
            self.model['party-typedate'].append(self.fake.date_between_dates(
                max_old,
                datetime.date.today()))

        # "name": "party-gender",
        # "description": "Party gender ('F' or 'M')",
        self.model['party-gender'].append(self.rnd_choose(["F", "M"], [0.6, 0.4]))

        # "name": "party-education",
        # "description": "Party education (e.g. 'Elementary school', 'High school', 'University', etc.)",
        self.model['party-education'].append(self.rnd_choose(["Elementary school", "High school", "University"], [0.5, 0.4, 0.1]))

        # "name": "party-familystatus",
        # "description": "Family status for party ('Married','Single', 'Divorced')",
        self.model['party-familystatus'].append(self.rnd_choose(["Married", "Single", "Divorced"], [0.5, 0.4, 0.1]))

        # "name": "party-nchild",
        # "description": "Count of children",
        self.model['party-nchild'].append(self.rnd_choose(range(0, 4), [0.05, 0.6, 0.3, 0.05]))

        # "name": "party-industry",
        # "description": "Party industry (e.g. 'IT', 'Finance', 'Telco', 'Medical', etc.)",
        self.model['party-industry'].append(self.rnd_choose(
            ["IT", "Financial services", "Telcommunications", "Industry", "Mining", "Aerospace",
             "Medical services", "Education", "Food industry", "Real Estate",
             "Social services", "Agriculture", "Transport", "Public administration"]))

        # "name": "party-industryposition",
        # "description": "Party position in industry (e.g. 'Manager', 'Developer', 'Analyst', etc.)",
        self.model['party-industryposition'].append(self.rnd_choose(
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
             0.05, 0.079, 0.05]))  # 0.179

        # # "name": "party-industry",
        # # "description": "Party industry (e.g. 'IT', 'Finance', 'Telco', 'Medical', etc.)",
        # self.model['party-industry'].append(self.rnd_choose(["IT", "Finance", "Telco", "Medical"]))
        #
        # # "name": "party-industryposition",
        # # "description": "Party position in industry (e.g. 'Manager', 'Developer', 'Analyst', etc.)",
        # self.model['party-industryposition'].append(self.rnd_choose(["Manager", "Developer", "Analyst"], [0.1, 0.45, 0.45]))

        # "name": "party-residencecountry",
        # "description": "Party country residence",
        self.model['party-residencecountry'].append(self.fake.country())

        # "name": "party-city",
        # "description": "Permanent stay-city (part of permanent stay)",
        self.model['party-city'].append(self.fake.city())

        # "name": "party-income",
        # "description": "Monthly income in local currency",
        self.model['party-income'].append(self.rnd_choose(range(50, 200)) * 1000)

        # "name": "party-incometype",
        # "description": "Type of the main income (e.g. 'Earned', 'Passive', 'Portfolio')",
        self.model['party-incometype'].append(self.rnd_choose(["Earned", "Passive", "Portfolio"], [0.96, 0.02, 0.02]))

        # "name": "party-peoplehousehold",
        # "description": "Number of people in household",
        self.model['party-peoplehousehold'].append(self.model['party-nchild'][-1] + self.rnd_choose(range(1, 4), [0.05, 0.9, 0.05]))

        # "name": "party-incomehousehold",
        # "description": "Monthly income in local currency for household",
        self.model['party-incomehousehold'].append(round(self.model['party-income'][-1] * self.rnd_choose(range(10, 30)) / 10))

        # "name": "party-expenseshousehold",
        # "description": "Monthly expenses (insurence, loans, etc.) for household",
        self.model['party-expenseshousehold'].append(round(self.model['party-incomehousehold'][-1] * self.rnd_choose(range(10, 50)) / 100))

        # "name": "party-currency",
        # "description": "Party currency (USD, EUR)",
        self.model['party-currency'].append(self.rnd_choose(["USD", "EUR"], [0.95, 0.05]))

        # "name": "record-date",
        # "description": "The date when the record was created",
        self.model['record-date'].append(self.gmodel["NOW"])

