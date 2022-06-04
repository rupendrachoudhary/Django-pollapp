from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import PollQuestion, PollAnswer


class IndexView(generic.ListView):
    template_name = 'myapp/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last 6 published questions(not including any future dated question)"""
        return PollQuestion.objects.filter(question_date__lte=timezone.now()).order_by('-question_date')[:6]


class DetailView(generic.DetailView):
    model = PollQuestion
    template_name = 'myapp/detail.html'

    def get_queryset(self):
        """
        Exclude all future questions(those aren't
        published yet)
        """
        return PollQuestion.objects.filter(question_date__lte=timezone.now())



class ResultsView(generic.DetailView):
    model = PollQuestion
    template_name = 'myapp/results.html'


def vote(request, question_id):
    pollquestion = get_object_or_404(PollQuestion, pk=question_id)
    try:
        selected_choice = pollquestion.choices.get(pk=request.POST['choice'])
    except(KeyError, PollAnswer.DoesNotExist):
        # Redisplay the question voting page because of no choice option selected
        vote_dict = {
            'pollquestion': pollquestion,
            'error_message': "You didn't selected any choice.",
        }
        return render(request, 'myapp/detail.html', vote_dict)

    else:
        selected_choice.total_votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('myapp:results', args=(pollquestion.id,)))
