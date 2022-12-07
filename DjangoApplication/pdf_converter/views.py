from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from pdf_converter.forms import *
from pdf_converter.models import Resume

import pdfkit

menu = [{'title': "Создать новое резюме", 'url_name': 'add_resume'}]


def logout_user(request):
    logout(request)
    return redirect('login')


def show_resume(request, resume_id):
    resume = Resume.objects.filter(pk=resume_id)[0]
    ls = [resume.filename, resume.name, '', resume.contacts, resume.education, resume.awards, resume.skills]
    context = dict(zip(AddResumeForm.Meta.fields, ls))
    if request.method == 'POST':
        form = AddResumeForm(request.POST, request.FILES, initial=context)
        if form.is_valid():
            f = form.save()
            f.username = request.user.username
            f.save()
            return redirect('home')
    else:
        form = AddResumeForm(initial=context)
    return render(request, 'pdf_converter/add_resume.html', {'form': form})


def add_resume(request):
    if request.method == 'POST':
        form = AddResumeForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            f.username = request.user.username
            f.save()
            return redirect('home')
    else:
        form = AddResumeForm()
    return render(request, 'pdf_converter/add_resume.html', {'form': form})


def show_archive(request):
    posts = Resume.objects.filter(username=f'{request.user.username}').order_by('-time_create')
    return render(request, 'pdf_converter/archive.html', {'posts': posts})


def index(request):
    posts = Resume.objects.filter(username=f'{request.user.username}').order_by('-time_create')
    if request.user.is_authenticated:
        return render(request, 'pdf_converter/index.html', {'menu': menu, 'posts': posts})
    return redirect('login')


def view(request, resume_id):
    resume = Resume.objects.filter(pk=resume_id)
    if resume[0].username == request.user.username:
        return render(request, 'pdf_converter/download.html', {'resume': resume[0]})
    return HttpResponseNotFound(f"<h1>Page not found</h1><br>Резюме в вашем архиве не найдено")


def download(request, resume_id):
    # resume = Resume.objects.filter(pk=resume_id)
    # html = render(request, 'pdf_converter/download.html', {'resume': resume[0]})
    # options = {
    #     'page-size': 'Letter',
    #     'encoding': "UTF-8",
    # }
    # pdf = pdfkit.from_string(html, False, options)
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment;filename = "pperson_list_pdf.pdf"'

    resume = Resume.objects.filter(pk=resume_id)
    return render(request, 'pdf_converter/download.html', {'resume': resume[0]})


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'pdf_converter/signup.html'
    success_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('login')
        else:
            return render(request, self.template_name, {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'pdf_converter/login.html'

    def get_success_url(self):
        return reverse_lazy('home')



