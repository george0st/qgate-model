import datetime
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicEvent(Base):

    NAME = "06-basic-event"
    EVENT_HISTORY_DAYS = 90

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicEvent.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

        self.now = datetime.datetime.fromisoformat(self.gmodel["NOW"])

        # list of groups and group probability
        #   [[group, ...], [group probability, ...]]
        self.event_groups_customer=[["user profile", "product", "offer"],
                                    [0.01, 0.19, 0.8]]

        self.event_groups=[["user profile", "offer"],
                                    [0.2, 0.8]]

        # list of categorie and probabilities for group
        #   "group": [["category", ...], [category probability, ...]]
        self.event_categories = {"user profile": [["income", "expences", "address", "email", "phone", "children"],
                                                  [0.1, 0.1, 0.2, 0.2, 0.2, 0.2]],
                     "product": [["contract detail", "account detail", "legal conditions","sanctions"],
                                 [0.35, 0.55, 0.05, 0.05]],
                     "offer": [["product list", "service list", "legal conditions", "sanctions"],
                               [0.45, 0.45, 0.05, 0.05]]}

        # list of action and probabilities for group/category
        #   "group/category": [["action", ...], [action probability, ...]]
        self.event_actions = {"user profile/income": [["show", "edit"], [0.999, 0.001]],
                        "user profile/expences": [["show", "edit"], [0.9995, 0.0005]],
                        "user profile/address": [["show", "edit"], [0.999, 0.001]],
                        "user profile/email": [["show", "edit"], [0.995, 0.005]],
                        "user profile/phone": [["show", "edit"], [0.998, 0.002]],
                        "user profile/children": [["show", "edit"], [0.99995, 0.00005]],
                        "product/contract detail": [["show", "edit"], [0.99, 0.01]],
                        "product/account detail": [["show", "edit"], [0.99, 0.01]],
                        "product/legal conditions": [["show", "edit"], [0.9999, 0.0001]],
                        "product/sanctions": [["show", "edit"], [0.9999, 0.0001]],
                        "offer/product list": [["show"], [1]],
                        "offer/service list": [["show"], [1]],
                        "offer/legal conditions": [["show"], [1]],
                        "offer/sanctions": [["show"], [1]]}

    @property
    def Name(self):
        return BasicEvent.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # only 3 months back history
            # max 0-2 bandl of events per day
            # mix of actions

            # generate event with history EVENT_HISTORY_DAYS
            day=BasicEvent.EVENT_HISTORY_DAYS
            party_customer=party['party-type'] == "Customer"
            while True:

                # day for events
                #   for customer:       more active
                #   for non customer:   small amount of activities
                if party_customer:
                    day-=self.rnd_choose(range(10),[0.01, 0.19, 0.1, 0.2, 0.1, 0.05, 0.05, 0.1, 0.1, 0.1])
                else:
                    day -= self.rnd_choose(range(10), [0, 0, 0, 0, 0.05, 0.05, 0.1, 0.2, 0.3, 0.3])

                if day<0:
                    break
                event_date = self.now - datetime.timedelta(days=float(day))

                session_id = str(uuid.uuid4())
                # define bundle
                #   for customer:       size 2-15x events (bigger amount of activities)
                #   for non-customer:   size 2-10x events (small amount of activites)
                day_events=self.rnd_choose(range(2, 15)) if party_customer else self.rnd_choose(range(2, 10))
                for event in range(day_events):

                    # add new model
                    model = self.model_item()

                    # "name": "event-id",
                    model['event-id'] = str(uuid.uuid4())

                    # "name": "session-id",
                    model['session-id'] = session_id

                    # "name": "party-id",
                    model['party-id'] = party['party-id']

                    if event==0:
                        # add login for first event in bundle
                        group="access"
                        category="login"
                        action="mobile" if self.rnd_bool() else "web"
                    else:
                        # add random group, category, action
                        if party_customer:
                            group = self.rnd_choose(self.event_groups_customer[0], self.event_groups_customer[1])
                        else:
                            group = self.rnd_choose(self.event_groups[0], self.event_groups[1])

                        category=self.rnd_choose(self.event_categories[group][0], self.event_categories[group][1])

                        group_category_name=str.format("{0}/{1}", group,category)
                        action = self.rnd_choose(self.event_actions[group_category_name][0], self.event_actions[group_category_name][1])

                    # "name": "event-group",
                    model['event-group'] = group

                    # "name": "event-category",
                    model['event-category'] = category

                    # "name": "event-action",
                    model['event-action'] = action

                    # "name": "event-detail",
                    # "name": "event-date",

                    # "name": "record-date"
                    model['record-date']=self.gmodel["NOW"]

                    self.model.append(model)

