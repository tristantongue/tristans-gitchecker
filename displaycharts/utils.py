import requests
import pygal

def create_pie(user , repo):
    response = requests.get("https://api.github.com/repos/%s/%s/languages" % (user, repo))
    language_list = response.json()
    chart = pygal.Pie()
    chart.title = "Breakdown of %s by language" % (repo)
    for key in language_list:
        chart.add(key, language_list[key])
    mychart = chart.render_data_uri()
    return mychart