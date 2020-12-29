from django.shortcuts import render
from django import forms
import requests
from .models import Repo
import pygal
from .utils import create_pie


class languageform(forms.Form):
    user = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'To find a breakdown of a specific repo first enter a GitHub user here:'}))
    repo = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': '...and then the name of the repo here!'}))

class all_repos_form(forms.Form):
    user = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search for a GitHub user! Try a big company!'}))

def create_bar(user):
    response = requests.get("https://api.github.com/users/%s/repos" % (user))
    full_list = response.json()
    graph = pygal.HorizontalBar()
    graph.title = '%s Repos by Size' % (user)
    for repo in full_list:
        label = repo["name"]
        value = repo["size"]
        graph.add(label, value)
    chart_svg_as_datauri = graph.render_data_uri()
    return chart_svg_as_datauri

def create_pie(user, repo):
    print('creating pie chart')
    response = requests.get("https://api.github.com/repos/%s/%s/languages" % (user, repo))
    language_list = response.json()
    chart = pygal.Pie()
    chart.title = "Breakdown of %s by language" % (repo)
    for key in language_list:
        chart.add(key, language_list[key])
    chart_svg_as_datauri = chart.render_data_uri()
    return chart_svg_as_datauri

def homepage(request):
    context = {}
    return render(request, 'homepage.html', context)


def all_repos(request):

    form = all_repos_form(request.GET)
    if form.is_valid():
        try:
            user = form.cleaned_data['user']
            response = requests.get("https://api.github.com/users/%s/repos" % (user))
            full_list = response.json()
        except TypeError:
            context = {
                "form": form,
                "github_repos": full_list,
            }
            return render(request, 'all-repos.html', context)
    else:
        response = requests.get("https://api.github.com/users/tristantongue/repos")
        full_list = response.json()
        form = all_repos_form()

    context = {
        "form": form,
        "github_repos": full_list,
    }
    return render(request, 'all-repos.html', context)


def by_size(request):
    
    form = all_repos_form(request.GET)
    if form.is_valid():
        user = form.cleaned_data['user']
        chart_svg_as_datauri = create_bar(user)
    else:
        chart_svg_as_datauri = ""
        form = all_repos_form()

    context = {
        "form": form,
        "rendered_chart_svg_as_datauri": chart_svg_as_datauri,
    }
    return render(request, 'by-size.html', context)



def languages(request):

    form = languageform(request.GET)
    if form.is_valid():
        user = form.cleaned_data['user']
        repo = form.cleaned_data['repo']
        chart_svg_as_datauri = create_pie(user, repo)
    else:
        chart_svg_as_datauri = ""
        form = languageform()

    context = {
        'form': form,
        "rendered_chart_svg_as_datauri": chart_svg_as_datauri,
    }
    return render(request, 'languages.html', context)
