import os

from django.db import models

# Create your models here.
class PathItem:
    name = ""
    parent = ""
    url = ""

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.url = os.path.join(parent, name)


class FileItem:
    name = ""
    parent = ""
    url = ""
    canRead = True

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.url = os.path.join(parent, name)