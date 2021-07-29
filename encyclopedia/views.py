from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def randomize(request):
    options = list(util.list_entries())
    title = random.choice(options)
    return show_entry(request, title=title)


def show_entry(request, title):
    md = util.get_entry(title=title)
    if not md:
        return render(request, "encyclopedia/error.html")
    else:
        entry = util.markdown_to_html(md)
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title,
       })


def search(request):
    q = request.GET.get('q')
    if q is None or not q:
        return HttpResponseRedirect(reverse('index'))

    find_q = util.search_entry(q=q)
    if not find_q:
        return render(request, "encyclopedia/error.html")
    elif len(find_q) == 1 and util.get_entry(find_q[0]):
        return show_entry(request, find_q[0])
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": find_q
        })


def new_entry(request):
    if request.method != 'POST':
        return render(request, 'encyclopedia/new.html')

    title = request.POST.get('title')
    content = request.POST.get('content')

    if not title or not content:
        messages.error(request, 'Fields can not be empty.')
        return render(request, 'encyclopedia/new.html')

    if title in util.list_entries():
        messages.error(request, 'Title already exists.')
        return render(request, 'encyclopedia/new.html')

    messages.success(request, 'New page registered with success!')
    util.save_entry(title, content)

    return show_entry(request, title)


def edit_entry(request, title):
    content = util.get_entry(title=title)
    if not content:
        return render(request, "encyclopedia/error.html")
    else:
       render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
       })

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            messages.error(request, 'Fields can not be empty.')
            return render(request, 'encyclopedia/edit.html')

        messages.success(request, 'Your page has been updated!')
        util.save_entry(title, content)

        return show_entry(request, title)
    else:
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
       })
