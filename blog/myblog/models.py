# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import  RichTextUploadingField

# Create your models here.

class BlogDateCategory(models.Model):
	year = models.IntegerField(default=0)
	month = models.IntegerField(default=0)

	def __unicode__(self):
		ret = str(self.year)+str(self.month)
		return ret

class BlogType(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class BlogCategory(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Blog(models.Model):
	blogdatecategory = models.ForeignKey(BlogDateCategory, null=True)
	blogcategory = models.ManyToManyField(BlogCategory)
	blogtype = models.ForeignKey(BlogType, null=True)
	name = models.CharField(max_length=200)
	img_path = models.CharField(blank=True,null=True,max_length=200)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	is_original = models.BooleanField(default=False)
	eyes_count = models.IntegerField(default=0)
	summary = models.CharField(max_length=200)
	content = RichTextField(blank=True,null=True,verbose_name="内容")


	def __unicode__(self):
		return self.name