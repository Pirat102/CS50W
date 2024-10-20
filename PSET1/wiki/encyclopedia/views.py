from django.shortcuts import render
import markdown2

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
        return render(request, f"encyclopedia/entry.html",{
            "title": title,
            "content": html
        })
    else:
        return render(request, f"encyclopedia/error.html")
        
def search(request, query):
    ...