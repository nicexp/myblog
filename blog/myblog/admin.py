# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import BlogDateCategory,Blog,BlogCategory,BlogType

admin.site.register(BlogDateCategory)
admin.site.register(Blog)
admin.site.register(BlogCategory)
admin.site.register(BlogType)