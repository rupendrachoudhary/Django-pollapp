from django.test import TestCase
import datetime
from django.utils import timezone
from .models import PollQuestion
from django.urls import reverse


class PollQuestionModelTests(TestCase):
    def test_to_care_future_question(self):
        # was_published_recently should return FALSE for all future dated questions
        # question_date is some future date

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = PollQuestion(question_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_to_care_present_question(self):
        # was_published_recently should return TRUE for all recent questions
        # question_date is some date within last one day

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = PollQuestion(question_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_to_care_past_question(self):
        # was_published_recently should return TRUE for all past questions
        # question_date is set to some date older than 1 day

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = PollQuestion(question_date=time)
        self.assertIs(past_question.was_published_recently(), False)


def create_question(question, days):
    """ Create question with this function.
    if days value is -ve that's past question
    if days value is +ve that's future question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return PollQuestion.objects.create(question=question, question_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        """ If no question exists, suitable error_message would prompt
        """
        response = self.client.get(reverse('myapp:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Question, No Poll !")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """ questions with past date would be displayed on home page(index page)
        """
        question = create_question(question="Past Question", days=-30)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question], )

    def test_future_question(self):
        """ question with question_date set to some future date won't be
        displayed at our home page(index page)
        """
        create_question(question="Future Question.", days=30)
        response = self.client.get(reverse('myapp:index'))
        self.assertContains(response, "Future Question, No Poll !")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        If future and past both types of questions exist , display only
        past questions on index page.
        """
        question = create_question(question="Past Question.", days=-30)
        create_question(question="Future Question.", days=30)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question], )

    def test_two_past_questions(self):
        """
        Our index page may display multiple questions
        """
        question1 = create_question(question="Past Question no.1", days=-30)
        question2 = create_question(question="Past Question no.2", days=-10)
        response = self.client.get(reverse('myapp:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1], )


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        DetailView-Questions which are published in future would cause
        error 404 , not found.
        """
        future_question = create_question(question="Future Question.", days=10)
        url = reverse('myapp:detail', args=(future_question.id,))
        response = self.client.get(reverse(url))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        Detail View of questions which are published in the past.
        """
        past_question = create_question(question="Past Question.", days=-10)
        url = reverse('myapp:detail', args=(past_question.id,))
        response = self.client.get(reverse(url))
        self.assertContains(response, past_question.question)
