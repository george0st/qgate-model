import datetime
import uuid

from generator.base_data import BaseData
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty

import faker.providers
import numpy


class BasicEvent(BaseData):

    NAME = "06-basic-event"
    MAX_EVENT_HISTORY_DAYS = 90

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
        self.event_categories = {"user profile": [["income", "expenses", "address", "email", "phone", "children"],
                                                  [0.1, 0.1, 0.2, 0.2, 0.2, 0.2]],
                     "product": [["contract detail", "account detail", "legal conditions","sanctions"],
                                 [0.35, 0.55, 0.05, 0.05]],
                     "offer": [["product list", "service list", "legal conditions", "sanctions"],
                               [0.45, 0.45, 0.05, 0.05]]}

        # list of action and probabilities for group/category
        #   "group/category": [["action", ...], [action probability, ...]]
        self.event_actions = {"user profile/income": [["show", "edit"], [0.999, 0.001]],
                        "user profile/expenses": [["show", "edit"], [0.9995, 0.0005]],
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

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # only 3 months back history
            # max 0-2 bandl of events per day
            # mix of actions

            # generate event with history EVENT_HISTORY_DAYS
            party_customer=party['party_type'] == "Customer"
            event_date = self.now - datetime.timedelta(days=float(BasicEvent.MAX_EVENT_HISTORY_DAYS))

            # iteration cross days
            while True:

                # day for events
                #   for customer:       more active
                #   for non customer:   small amount of activities
                if party_customer:
                    day = self.rnd_choose(range(10),[0, 0, 0, 0.1, 0.3, 0.15, 0.15, 0.1, 0.1, 0.1])
                else:
                    day = self.rnd_choose(range(10), [0, 0, 0, 0, 0.05, 0.05, 0.1, 0.2, 0.3, 0.3])
                event_date = event_date + datetime.timedelta(days=float(day))
                if event_date > self.now:
                    break

                # define bundle
                #   for customer:       size 2-10x events (bigger amount of activities)
                #   for non-customer:   size 2-5x events (small amount of activites)
                session_id = str(uuid.uuid4())
                session_events=self.rnd_choose(range(2, 10)) if party_customer else self.rnd_choose(range(2, 5))
                session_datetime = datetime.datetime(event_date.year,
                                                     event_date.month,
                                                     event_date.day,
                                                     self.rnd_int(0,24),
                                                     self.rnd_int(0, 60),
                                                     self.rnd_int(0, 60))
                for event in range(session_events):

                    # add new model
                    model = self.model_item()

                    # "name": "event-id",
                    model['event-id'] = str(uuid.uuid4())

                    # "name": "session-id",
                    model['session-id'] = session_id

                    # "name": "party_id",
                    model['party_id'] = party['party_id']

                    if event==0:
                        # add default group, category and action -> login for first event in bundle
                        group="access"
                        category="mobile" if self.rnd_bool() else "web"
                        action="login"
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
                    model['event-detail'] = ""    # not used, right now

                    # "name": "event-date",
                    #   random movement in second for next event
                    #   new datetime for this event in session
                    session_datetime = session_datetime + datetime.timedelta(seconds=float(self.rnd_int(0,13)))
                    model['event-date']=session_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    # "name": "record-date"
                    model['record-date']=self.gmodel["NOW"]

                    self.model.append(model)

