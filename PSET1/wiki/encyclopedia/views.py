from django.shortcuts import render
import markdown2
import re

from . import util


def convert_to_html(title):
    content = util.get_entry(title)
    if content == None:
        return None
    else:
        return markdown2.markdown(content)


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    html = convert_to_html(title)
    if html:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html
        })
    else:
        return render(request, "encyclopedia/error.html")
        
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    matches = []
    for title in entries:
        if query.lower() == title.lower():
            return entry(request, title)
        else:
            match = re.search(query.lower(), title.lower())
            if match:
                matches.append(title)
    return render(request, "encyclopedia/index.html", {
        "entries": matches
    })

  