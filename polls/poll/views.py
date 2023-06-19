from django.http import HttpResponse
from django.shortcuts import render

from poll.models import Question


def index(request):
    return render(request, 'poll/index.html')

def poll_list(request):
    # 전체 데이터 가져오기
    question_list = Question.objects.all()
    return render(request, 'poll/poll_list.html', {'question_list': question_list})

def detail(request, question_id):
    # 데이터 1개 조회
    question = Question.objects.get(id=question_id)
    return render(request, 'poll/detail.html', {'question': question})

def vote(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == "POST":
        try:
            choice_id = request.POST['choice']  # 선택된 항목 id
            sel_choice = question.choice_set.get(id=choice_id)  # id로 항목을 찾아서
        except:
            error = "선택을 하지 않았습니다."
            return render(request, 'poll/detail.html', {'question': question, 'error': error})
        else:
            sel_choice.votes = sel_choice.votes + 1 # sel_choice.votes = 0
            sel_choice.save()
            return render(request, 'poll/result.html', {'question': question})
    else:
        return render(request, 'poll/detail.html', id=question_id)


def test (request):
    cart = "콩나물" #모델(데이터) - 딕셔너리형으로 보냄
    cartlist = ["계란", "콩나물", "생수"]
    context = {'cart': cart, 'cartlist': cartlist}
    return render(request, 'poll/test.html', context)