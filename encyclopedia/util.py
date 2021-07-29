import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import markdown2


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title.lower()}.md")
        return f.read().decode("cp1252")
    except FileNotFoundError:
        return None


def markdown_to_html(text):
    html = markdown2.markdown(text)
    return html


def search_entry(q):
    """
    Search for all encyclopedia entries that contains the query q. Returns None if no matches
    are found.
    """
    query = []
    for entry in list_entries():
        if q.lower() in entry.lower():
            query.append(entry)

    if not query:
        return None
    else:
        return query
