from django.shortcuts import render
from django import forms
import requests
from .models import Repo
import pygal


class languageform(forms.Form):
    user = forms.CharField(max_length=100)
    repo = forms.CharField(max_length=100)


def homepage(request):
    context = {}
    return render(request, 'homepage.html', context)


def all_repos(request):
    response = requests.get("https://api.github.com/users/tristantongue/repos")
    full_list = response.json()
    context = {
        "github_repos": full_list,
    }
    return render(request, 'all-repos.html', context)


def by_size(request):
    response = requests.get("https://api.github.com/users/tristantongue/repos")
    full_list = response.json()
    graph = pygal.HorizontalBar()
    graph.title = 'Repos by Size'

    for repo in full_list:
        label = repo["name"]
        value = repo["size"]
        graph.add(label, value)

    chart_svg_as_datauri = graph.render_data_uri()

    context = {
        "rendered_chart_svg_as_datauri": chart_svg_as_datauri,
    }
    return render(request, 'by-size.html', context)


def languages(request):
    

    form = languageform(request.GET)
    if form.is_valid():
        user = form.cleaned_data['user']
        repo = form.cleaned_data['repo']
        response = requests.get("https://api.github.com/repos/%s/%s/languages" % (user, repo))
        language_list = response.json()
        chart = pygal.Pie()
        chart.title = "Breakdown of %s by language" % (repo)
        for key in language_list:
            chart.add(key, language_list[key])
        chart_svg_as_datauri = chart.render_data_uri()
    else:
        response = requests.get("https://api.github.com/repos/tristantongue/cowebsite/languages")
        language_list = response.json()
        chart = pygal.Pie()
        chart.title = "Breakdown of cowebsite by language"
        for key in language_list:
            chart.add(key, language_list[key])
        chart_svg_as_datauri = chart.render_data_uri()
        form = languageform()


    context = {
        'form': form,
        "rendered_chart_svg_as_datauri": chart_svg_as_datauri,
    }
    return render(request, 'languages.html', context)
