import datetime
import math
import uuid

from generator.base import Base
from faker import Faker
from faker.providers import lorem
import numpy
import pandas as pd
from generator.basic_party import BasicParty
from enum import Enum


class Sentiment(Enum):
    Positive = 1
    Negative = 2
    Neutral = 3
    Fake = 4

class BasicCommunication(Base):

    NAME = "07-basic-communication"
    COMMUNICATION_HISTORY_DAYS = 90

    def __init__(self, path, gmodel):
        super().__init__(path, gmodel, BasicCommunication.NAME)
        self.fake = Faker(['en_US'])
        self.fake.add_provider(lorem)
        self.now = datetime.datetime.fromisoformat(self.gmodel["NOW"])

    @property
    def Name(self):
        return BasicCommunication.NAME

    def generate(self, count):

        # reference to the data from BasicParty
        parties = self.gmodel[BasicParty.NAME]

        # iteration cross all parties
        for party in parties:

            # only 3 months back history
            # generate communication with history EVENT_HISTORY_DAYS
            party_customer=party['party-type'] == "Customer"
            communication_date = self.now - datetime.timedelta(days=float(BasicCommunication.COMMUNICATION_HISTORY_DAYS))

            # iteration cross days
            while True:

                # day for communication
                #   for customer:       more active (~ each 11 days)
                #   for non customer:   small amount of activities (~ each 19 days)
                if party_customer:
                    day = int(1.1 * self.rnd_choose(range(10),[0, 0, 0, 0, 0, 0, 0, 0, 0.1, 0.9]))
                else:
                    day = int(1.3 * self.rnd_choose(range(15), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.9]))
                communication_date = communication_date + datetime.timedelta(days=float(day))
                if communication_date > self.now:
                    break

                # define bundle
                #   for customer:       size 2-5x communications (bigger amount of activities)
                #   for non-customer:   size 1-3x communications (small amount of activites)
                session_id = str(uuid.uuid4())
                session_communications=self.rnd_choose(range(2, 5)) if party_customer else self.rnd_choose(range(1, 3))
                session_datetime = datetime.datetime(communication_date.year,
                                                     communication_date.month,
                                                     communication_date.day,
                                                     self.rnd_int(0,24),
                                                     self.rnd_int(0, 60),
                                                     self.rnd_int(0, 60))
                session_sentiment=self.rnd_choose([Sentiment.Neutral, Sentiment.Positive, Sentiment.Negative, Sentiment.Fake],
                                                       [0.6, 0.15, 0.05, 0.2])
                for event in range(session_communications):

                    # add new model
                    model = self.model_item()

                    # "name": "communication-id",
                    model['communication-id'] = str(uuid.uuid4())

                    # "name": "party-id",
                    model['party-id'] = party['party-id']

                    # "name": "content",
                    model['content'] = self._generate_test(session_sentiment)

                    # "name": "content-type",
                    model['content-type'] = "text"

                    # "name": "channel",
                    model['channel'] = self.rnd_choose(["email", "chat"], [0.8, 0.2])

                    # "name": "communication-date",
                    session_datetime = session_datetime + datetime.timedelta(seconds=float(self.rnd_int(0,13)))
                    model['communication-date']=session_datetime.strftime("%Y-%m-%d %H:%M:%S")

                    # "name": "record-date"
                    model['record-date'] = self.gmodel["NOW"]

                    self.model.append(model)

    def _generate_test(self, sentiment: Sentiment) -> str:
        if sentiment==Sentiment.Positive:
            return self.positive_sentences[self.rnd_int(0, len(self.positive_sentences))]
        elif sentiment==Sentiment.Negative:
            return self.negative_sentences[self.rnd_int(0, len(self.negative_sentences))]
        elif sentiment==Sentiment.Neutral:
            return self.neutral_sentences[self.rnd_int(0,len(self.neutral_sentences))]
        else:
            return self.fake.sentence(nb_words = 15,variable_nb_words = True)

    positive_sentences = [
        "I just wanted to say thank you for your amazing service. You really made my day!",
        "I'm very impressed with your product. It works flawlessly and has all the features I need. How can I leave a positive review?",
        "You are awesome! You solved my problem in no time and were very friendly and helpful. Can I speak to your supervisor and praise your work?",
        "I love your company. You always go above and beyond to meet my needs and expectations. Do you have a referral program that I can join?",
        "You have been very patient and informative with me. I appreciate your professionalism and expertise. Can you send me some additional resources to learn more about your product?",
        "I'm very happy with your service. You delivered on time, the quality was excellent, and the price was fair. Do you offer any discounts or coupons for loyal customers?",
        "You have exceeded my expectations. Your product is amazing and your support is outstanding. How can I share my feedback with other potential customers?",
        "You are the best! You answered all my questions and gave me some great tips and advice. Can I subscribe to your newsletter or blog to get more updates?",
        "I'm very grateful for your assistance. You were very courteous and respectful and handled my issue with care. Can I fill out a survey or a testimonial to express my satisfaction?",
        "You have made me a very happy customer. Your product is exactly what I was looking for and your support is top-notch. Do you have any other products or services that I might be interested in?",
        "I’m blown away by your product. It has transformed the way I work and saved me so much time and hassle. How can I spread the word about your amazing solution?",
        "You have been a lifesaver. You resolved my issue quickly and efficiently and followed up with me to make sure everything was working well. How can I rate your service and give you a glowing review?",
        "I’m thrilled with your service. You exceeded my expectations and delivered more than I asked for. How can I show my appreciation and gratitude to you and your team?",
        "You are a star. You listened to my needs and provided me with the best solution for my situation. How can I thank you and recommend you to others who might need your help?",
        "I’m very pleased with your product. It is easy to use, reliable, and has all the functionality I need. How can I stay updated on your latest features and developments?",
        "You have been a joy to work with. You were friendly, courteous, and professional throughout our interaction. How can I provide you with positive feedback and recognition for your excellent service?",
        "I’m ecstatic with your service. You went above and beyond to make me happy and satisfied. How can I reward you and show you my appreciation for your outstanding work?",
        "You are a gem. You answered all my queries and addressed all my concerns with patience and clarity. How can I express my satisfaction and admiration for your service and expertise?",
        "I’m very content with your product. It is high-quality, durable, and has a great design. How can I share my experience and opinion with other customers and potential buyers?",
        "You have been a delight to deal with. You were responsive, helpful, and knowledgeable throughout our communication. How can I compliment you and let your manager know how well you did?"
    ]

    negative_sentences = [
        "Why is your product so slow and buggy? Fix it now or I’m leaving!",
        "You charged me twice for the same service! This is unacceptable! I want a refund immediately!",
        "Your agent was rude and unhelpful! I demand to speak to a manager!",
        "You promised me a delivery by yesterday, but I still haven’t received my order! Where is it?",
        "Your website is down and I can’t access my account! How long will this take to resolve?",
        "You sent me the wrong item! This is not what I ordered! How can you be so incompetent?",
        "Your product does not work as advertised! It’s a scam! I want to cancel my subscription and get my money back!",
        "You keep sending me spam emails and calls! Stop harassing me or I’ll report you!",
        "Your instructions are unclear and confusing! I can’t figure out how to use your product! Help me or I’ll switch to a competitor!",
        "You ignored my previous emails and chats! Don’t you care about your customers? Respond to me now!",
        "I want to speak to your manager.",
        "I demand a refund.",
        "I want to cancel my subscription.",
        "I want to file a complaint.",
        "I want to know why this happened.",
        "I want to speak to someone who can help me.",
        "I want to know what you’re going to do about this.",
        "I want to be compensated for my inconvenience.",
        "I want to know when this will be resolved.",
        "I want to speak to someone who can authorize a refund.",
        "I want to speak to someone who can fix this immediately.",
        "I want to know why I was charged for this.",
        "I want to speak to someone who can explain this to me.",
        "I want to know what you’re going to do to make this right.",
        "I want to know why I wasn’t informed about this issue.",
        "I want to speak to someone who can give me a clear answer.",
        "I want to know how you’re going to prevent this from happening again.",
        "I want to know what you’re going to do to compensate me for this.",
        "I want to speak to someone who can help me resolve this issue.",
        "I want to know what you’re going to do to regain my trust.",
        "I want to know why I was charged twice.",
        "I want to know why my account was suspended.",
        "I want to know why my account was terminated.",
        "I want to know why my account was hacked.",
        "I want to know why my account was blocked.",
        "I want to know why my account was flagged.",
        "I want to know why my account was disabled.",
        "I want to know why my account was deleted.",
        "I want to know why my account was banned.",
        "I want to know why my account was locked.",
        "I’m experiencing an issue with my account."
    ]

    neutral_sentences = [
        "Thank you for your help.",
        "Could you please clarify this for me?",
        "I’m sorry, I didn’t understand what you meant.",
        "I’m having trouble with this feature.",
        "Can you please guide me through the process?",
        "I’m not sure what to do next.",
        "I need help with a probably technical problem.",
        "I’m having difficulty accessing the website.",
        "Could you please help me with this feature?",
        "I’m sorry, I’m still having trouble with this.",
        "How do I create an account?",
        "What are the shipping options?",
        "How do I track my order?",
        "What is your return policy?",
        "How do I change my order?",
        "What payment methods do you accept?",
        "What is the warranty period?",
        "How do I change my password?",
        "What are the product specifications?",
        "How do I contact customer support?",
        "How can I check the status of my claim?",
        "What are the benefits and exclusions of my policy?",
        "How can I update my personal or payment information?",
        "How can I renew or cancel my policy?",
        "How can I get a quote or purchase a new product?",
        "What are the different types of insurance products you offer?",
        "How can I contact you if I have a question or complaint?",
        "How can I file a claim in case of an accident or emergency?",
        "What are the documents or proofs required for filing a claim?",
        "How can I get a copy of my policy document or certificate?",
        "How can I compare different insurance plans and prices?",
        "How can I get a discount or lower my premium?",
        "How can I access or download my insurance card or ID?",
        "How can I find a network provider or hospital near me?",
        "How can I get a refund or reimbursement for my expenses?",
        "How can I transfer or assign my policy to someone else?",
        "How can I get a confirmation or receipt for my payment?",
        "How can I get an extension or grace period for my payment?",
        "How can I open or close a bank account?",
        "How can I check my balance or transaction history?",
        "How can I transfer money or pay bills online?",
        "How can I apply for a loan or credit card?",
        "How can I change or reset my password or PIN?",
        "How can I report a lost or stolen card or cheque?",
        "How can I activate or deactivate my card or account?",
        "How can I order or deposit a cheque or cash?",
        "How can I update my contact or mailing address?",
        "How can I find an ATM or branch near me?",
        "How can I track or change the status of my shipment?",
        "How can I get a quote or estimate for my shipment?",
        "How can I schedule or cancel a pickup or delivery?",
        "How can I find or contact a service point or office?",
        "How can I create or print a shipping label or invoice?",
        "How can I claim or report a damaged or missing shipment?",
        "How can I request or verify a proof of delivery or signature?",
        "How can I manage or update my preferences or profile?",
        "How can I apply for a refund or compensation for my shipment?",
        "How can I get a customs clearance or declaration for my shipment?",
        "How can I redeem or earn rewards or points with my card?",
        "How can I increase or decrease my credit limit or spending power?",
        "How can I dispute or resolve a charge or fee on my card?",
        "How can I enroll or opt out of paperless statements or notifications?",
        "How can I add or remove an authorized user or joint account holder?",
        "How can I request or replace a new or damaged card?",
        "How can I access or manage my card account online or on the app?",
        "How can I set up or change a payment plan or due date for my card?",
        "How can I avoid or reduce interest or late fees on my card?",
        "How can I get a balance transfer or cash advance with my card?"
    ]