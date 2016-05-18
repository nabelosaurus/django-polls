import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Choice, Question

from polls.factories import ChoiceFactory


def create_question(question_text, days):
    """
    Creates a question with the given 'question_text' and published the
    given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(
                response.context['latest_question_list'],
                []
        )

    def test_index_view_with_a_past_question(self):
        create_question('Past question.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        create_question('Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            []
        )

    def test_index_view_with_future_question_and_past_question(self):
        create_question('Past question.', days=-30)
        create_question('Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        create_question('Past question 1.', days=-30)
        create_question('Past question 2.', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question('Past question.', days=-30)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)


class QuestionResultsViewTests(TestCase):
    def test_results_with_no_question(self):
        response = self.client.get(reverse('polls:results', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_results_with_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_results_with_past_question(self):
        past_question = create_question('Past question.', days=-30)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)

class VotingTests(TestCase):
    def test_vote_on_past_question_without_choice(self):
        past_question = create_question('Past question.', days=-5)
        response = self.client.post(reverse('polls:vote', args=(past_question.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You didn&#39;t select a choice")
        self.assertEqual(response.context['error_message'], "You didn't select a choice")

    def test_vote_on_future_question_without_choice(self):
        future_question = create_question('Future question.', days=5)
        response = self.client.post(reverse('polls:vote', kwargs={'question_id': future_question.id}))
        self.assertEqual(response.status_code, 404)

    def test_vote_on_past_question_with_choice(self):
        past_question = create_question('Past question.', days=-5)
        ChoiceFactory.create(question=past_question, votes=0)
        c2 = ChoiceFactory.create(question=past_question, votes=0)
        response = self.client.post(reverse('polls:vote', args=(past_question.id,)), {'choice': c2.pk})
        self.assertRedirects(response, reverse('polls:results', args=(past_question.id,)))
        self.assertEqual(Choice.objects.get(pk=2).votes, 1)
        self.assertEqual(Choice.objects.get(pk=1).votes, 0)

    def test_vote_on_future_question_with_choice(self):
        future_question = create_question('Future question.', days=5)
        ChoiceFactory.create(question=future_question, votes=0)
        c2 = ChoiceFactory.create(question=future_question, votes=0)
        response = self.client.post(reverse('polls:vote', args=(future_question.id,)), {'choice': c2.pk})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Choice.objects.get(pk=2).votes, 0)
        self.assertEqual(Choice.objects.get(pk=1).votes, 0)

