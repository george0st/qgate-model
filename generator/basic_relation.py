import datetime
import uuid
from generator.base_data import BaseData
from faker import Faker
from faker.providers import internet, phone_number
from generator.basic_party import BasicParty


class BasicRelation(BaseData):

    NAME= "03-basic_relation"
    MAX_RELATIONS = 5

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicRelation.NAME)
        self.fake=Faker(['en_US'])
        self.fake.add_provider(internet)
        self.fake.add_provider(phone_number)

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # remove unlimited cycle for generation of relations
        if len(parties) < BasicRelation.MAX_RELATIONS:
            from colorama import Fore, Style

            print(Fore.BLUE + f"      NOTE: Small amount of parties '{len(parties)}' (expected >= '{BasicRelation.MAX_RELATIONS}')." + Style.RESET_ALL)
            return

        # iteration cross all parties
        for party in parties:

            if party['party_type']=="Customer":
                relations=self.rnd_choose(range(0, BasicRelation.MAX_RELATIONS), [0.15, 0.5, 0.3, 0.04, 0.01])
            else:
                relations=self.rnd_choose(range(0, BasicRelation.MAX_RELATIONS), [0.55, 0.3, 0.1, 0.04, 0.01])
            for relation in range(relations):

                # add new model
                model = self.model_item()

                # "name": "relation_id",
                model['relation_id']=str(uuid.uuid4())

                # "name": "relation_parentid",
                model['party_id']=party['party_id']

                # "name": "relation_childid",
                while (True):
                    random_id = parties[self.rnd_int(0, len(parties))]['party_id']
                    if random_id != model['party_id']:
                        model['relation_childid'] = random_id
                        break

                # "name": "relation_type",
                model['relation_type']=self.rnd_choose(["Family", "Job", "Social"], [0.5, 0.3, 0.2])
                self.apply_none_value(model, 'relation_type', "Job", probability_multiplicator=0.05)

                # "name": "relation_date",
                # not used, right now
                model['relation_date']=datetime.datetime(1970, 1, 1, 8, 0, 0).strftime("%Y-%m-%d %H:%M:%S")

                # "name": "record_date"
                model['record_date']=self.gmodel["NOW"]

                self.model.append(model)

