import datetime

from django.test import TestCase
from django.utils import timezone

from polls.factories import ChoiceFactory, QuestionFactory
from polls.models import Choice, Question

class QuestionMethodTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


    def test_string_method(self):
        question = QuestionFactory.create(question_text="Testing")
        question.save()
        self.assertEqual("Testing", question.__str__())


class ChoiceMethodTest(TestCase):

    def test_string_method(self):
        choice = ChoiceFactory.create(choice_text="Testing")
        self.assertEqual("Testing", choice.__str__())

    def test_create_choice(self):
        ChoiceFactory.create()
        self.assertEqual(len(Choice.objects.all()), 1)
        ChoiceFactory.create_batch(10)
        self.assertEqual(len(Choice.objects.all()), 11)