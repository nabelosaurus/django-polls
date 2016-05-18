from django.utils import timezone

from . import models

import factory


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Question

    question_text = factory.Faker('sentence', nb_words=10, variable_nb_words=True)
    pub_date = factory.Faker('date_time_this_month',
                             before_now=True,
                             after_now=True,
                             tzinfo=timezone.now().tzinfo)


class ChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Choice

    question = factory.SubFactory(QuestionFactory)
    choice_text = factory.Faker('word')
    votes = factory.Faker('random_digit')