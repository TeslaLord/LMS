from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AnswerForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.decorators import user_passes_test
from django.views import generic
from .models import Profile, Grade, Question, Answer, Profile, Section
import matplotlib.pyplot as plt
import io
from django.core.files.images import ImageFile
import urllib
import base64
import numpy as np
import plotly.offline as opy
import plotly.graph_objs as go
# Create your views here.


def home(request):
    return render(request, 'users/home.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Profile successfully Updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for the {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def results(request):
    # user = User.objects.filter(username="another").first()
    prof = Profile.objects.filter(user=User.objects.get(username=request.user)).first()
    curr = Grade.objects.filter(user=prof).first()

    l = eval(curr.ut1)
    plt.clf()
    data = {'IP': l[0], 'MRF': l[1], 'FOC': l[2], 'RA': l[3], 'SAT': l[4]}
    courses = list(data.keys())
    values = list(data.values())
    figure = io.BytesIO()
    fig = plt.subplots(figsize=(6, 6))
    plt.bar(courses, values, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 1 Scores")
    plt.savefig(figure, format="png")
    content_file = ImageFile(figure)
    curr.ut1p.save('ut1.png', content_file)
    plt.clf()

    l1 = eval(curr.ut2)
    data1 = {'IP': l1[0], 'MRF': l1[1],
             'FOC': l1[2], 'RA': l1[3], 'SAT': l1[4]}
    courses1 = list(data1.keys())
    values1 = list(data1.values())
    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize=(6, 6))
    plt.bar(courses1, values1, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 2 Scores")
    plt.savefig(figure, format="png")
    content_file1 = ImageFile(figure)
    curr.ut2p.save('ut2.png', content_file1)
    plt.clf()

    l2 = eval(curr.ut3)
    data2 = {'IP': l2[0], 'MRF': l2[1],
             'FOC': l2[2], 'RA': l2[3], 'SAT': l2[4]}
    courses2 = list(data2.keys())
    values2 = list(data2.values())
    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize=(6, 6))
    plt.bar(courses2, values2, color='maroon',
            width=0.4)
    plt.xlabel("Courses")
    plt.ylabel("Marks")
    plt.title("UNIT TEST - 3 Scores")
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut3p.save('ut3.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize=(6, 6))
    plt.pie(values, labels=courses)
    plt.title("UNIT TEST - 1 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut1pb.save('ut3b.png', content_file2)
    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize=(6, 6))
    plt.pie(values1, labels=courses1)
    plt.title("UNIT TEST - 2 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut2pb.save('ut3b.png', content_file2)

    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    fig = plt.subplots(figsize=(6, 6))
    plt.pie(values2, labels=courses2)
    plt.title("UNIT TEST - 3 Scores")
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut3pb.save('ut3b.png', content_file2)

    plt.clf()

    figure.seek(0)
    figure.truncate(0)
    barWidth = 1
    fig = plt.subplots(figsize=(12, 8))

    length = [6, 12, 18, 24, 30]
    plt.bar([i for i in length], values, color='maroon', width=barWidth,
            edgecolor='grey', label='UT1')
    plt.bar([i+1 for i in length], values1, color='grey', width=barWidth,
            edgecolor='grey', label='UT2')
    plt.bar([i+2 for i in length], values2, color='navy', width=barWidth,
            edgecolor='grey', label='UT3')

    plt.xlabel('Score', fontweight='bold')
    plt.ylabel('Subjects in UT', fontweight='bold')
    plt.title("UNIT TEST Performance Comparison")
    plt.xticks([i+1 for i in length],
               ['IP', 'MRF', 'RA', 'SAT', 'FOC'])
    plt.legend()
    plt.savefig(figure, format="png")
    content_file2 = ImageFile(figure)
    curr.ut12.save('ut3b.png', content_file2)
    plt.clf()

    trace1 = go.Bar(x=courses, y=values, marker={'color': 'blue'},
                    name='1st Trace')
    data_plotly = go.Data([trace1])
    layout_plotly = go.Layout(title="Progress Level", xaxis={
        'title': 'Date'}, yaxis={'title': 'Score'})

    figure_plotly = go.Figure(data=data_plotly, layout=layout_plotly)
    div = opy.plot(figure_plotly, auto_open=False, output_type='div')

    context = {
        'bar':div,
        'images': [
        curr.ut1p.url, curr.ut2p.url, curr.ut3p.url, curr.ut1pb.url, curr.ut2pb.url, curr.ut3pb.url, curr.ut12.url]
    }
    return render(request, 'users/results.html', context)





class SectionListView(generic.ListView):
    model = Section


class SectionDetailView(generic.DetailView):
    model = Section

    def get_context_data(self, **kwargs):
        context = super(SectionDetailView, self).get_context_data(**kwargs)
        profiles = Profile.objects.filter(section=self.kwargs['pk'])
        context['profiles'] = profiles
        return context


class ProfileDetailView(generic.DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        answers = Answer.objects.filter(
            user=Profile.objects.get(id=self.kwargs['pk']))
        # questions = Question.objects.filter(
        #     section=Profile.objects.get(id=self.kwargs['pk']).section)
        # context['questions'] = questions
        context['answers'] = answers

        return context


class HomeworkDetailView(generic.DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(HomeworkDetailView, self).get_context_data(**kwargs)
        context['end'] = False
        id = Profile.objects.get(
            user=User.objects.get(username=self.request.user)).id
        if Profile.objects.get(id=id).section in Section.objects.all():
            questions = Question.objects.filter(
                section=Profile.objects.get(id=id).section)
            i = self.kwargs['pk'] - 1

            if self.kwargs['pk'] != 1:
                answer_form = AnswerForm()
                answer_obj = Answer()
                answer_obj.question = Question.objects.filter(
                    question_field=questions[i-1]).first()

                answer_obj.answer_field = self.request.GET['answer_field']


                profile_obj = Profile.objects.get(
                    user=User.objects.get(username=self.request.user))
                answer_obj.user = profile_obj
                answer_obj.save()

                if i >= len(questions):
                    context['end'] = True
                    return context
                context['question'] = questions[i]
                context['answer'] = answer_form

                context['index'] = i+1
                print(context)
            else:
                answer_form = AnswerForm()
                context['question'] = questions[i]
                context['index'] = i+1
                context['answer'] = answer_form
                context['button'] = "Next"
        return context
