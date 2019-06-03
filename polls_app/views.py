from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from polls_app.models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls_app/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls_app/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls_app/results.html'
# def index(request):
#
#     #return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('polls_app/index.html')
#     context = {
#         'latest_question_list': latest_question_list
#     }
#
#     return render(request, 'polls_app/index.html', context)
#
#     #return HttpResponse(template.render(context, request))
#
#     #output = ', '.join([q.question_text for q in latest_question_list])
#     #return HttpResponse(output)
#
#
# def detail(request, question_id):
#     #return HttpResponse("You're looking at question %s." % question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     # return render(request, 'polls_app/detail.html', {'question': question})
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls_app/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     # response = "You're looking at the results of question %s."
#     # return HttpResponse(response % question_id)
#
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls_app/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls_app/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.vote += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls_app:results', args=(question.id, )))
    # return HttpResponse("You're voting on question %s." % question_id)

