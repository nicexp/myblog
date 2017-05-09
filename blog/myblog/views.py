# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render,get_object_or_404

# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader
from .models import BlogDateCategory,Blog,BlogCategory,BlogType
import random
import math

MAX_MENU_DISPLAY = 8
MAX_SIDE_DISPLAY = 5
MAX_SUMMARY_LENGTH = 60

def convert(blog):
	for v in blog:
		v.img_path = v.img_path[len("myblog"):]

		date = "%d-%02d-%02d"%(v.pub_date.year, v.pub_date.month, v.pub_date.day)
		v.pub_date = date

		if v.is_original == True:
			v.is_original = "原创"
		else:
			v.is_original = "转载"

		if len(v.summary) > MAX_SUMMARY_LENGTH:
			v.summary = v.summary[0:MAX_SUMMARY_LENGTH]

		v.summary = v.summary+"..."

	return blog

def getPath(strpath, curpage, pageNum):
	pages = []

	for k in range(pageNum):
		temp = {}
		temp["path"]=strpath%(k+1)
		temp["name"]=str(k+1)
		pages.append(temp)

	if pageNum > curpage:
		temp = {}
		temp["path"]=strpath%(curpage+1)
		temp["name"]=">"
		pages.append(temp)

	return pages

def getIndexPage(curpage=1):
	allBlogs = Blog.objects.all()

	num = allBlogs.count()
	pageNum = int(math.ceil(float(num)/MAX_MENU_DISPLAY))
	strpath= "/%d"

	return getPath(strpath, curpage, pageNum)

def getDatePage(year, month, curpage=1):
	blogdate = BlogDateCategory.objects.all()

	for v in blogdate:
		if (str(v.year) == year) and (str(v.month) == month):
			tempdate = v

	blogList = tempdate.blog_set.all()

	num = blogList.count()
	pageNum = int(math.ceil(float(num)/MAX_MENU_DISPLAY))
	strpath= "/%d/%d/"%(int(year), int(month))+"%d"

	return getPath(strpath, curpage, pageNum)

def getMaskPage(masks, curpage=1):
	blogcategory = BlogCategory.objects.filter(name=masks)
	blogList = blogcategory[0].blog_set.all()

	num = blogList.count()
	pageNum = int(math.ceil(float(num)/MAX_MENU_DISPLAY))
	strpath= "/mask/%s/"%(masks)+"%d"

	return getPath(strpath, curpage, pageNum)

def getTypePage(types, curpage=1):
	blogtype = BlogType.objects.filter(name=types)
	blogList = blogtype[0].blog_set.all()

	num = blogList.count()
	pageNum = int(math.ceil(float(num)/MAX_MENU_DISPLAY))
	strpath= "/type/%s/"%(types)+"%d"

	return getPath(strpath, curpage, pageNum)

def getNewArticle():
	allBlogs = Blog.objects.order_by('-id')
	if allBlogs.count() > MAX_MENU_DISPLAY:
		allBlogs = allBlogs[0:MAX_MENU_DISPLAY]

	convert(allBlogs)

	return allBlogs

def getRecommendArticle():
	allBlogs = Blog.objects.filter(is_original=True).order_by("-eyes_count")
	if allBlogs.count() > MAX_MENU_DISPLAY:
		allBlogs = allBlogs[0:MAX_MENU_DISPLAY]

	convert(allBlogs)

	return allBlogs

def getRandomArticle():
	allBlogs = Blog.objects.filter(is_original=True).order_by("-eyes_count")

	temp = []

	for k in range(allBlogs.count()):
		temp.append(allBlogs[k])
	random.shuffle(temp)
	if len(temp) > MAX_MENU_DISPLAY:
		temp = temp[0:MAX_MENU_DISPLAY]

	convert(temp)

	return temp

def getNotOriginal():
	allBlogs = Blog.objects.filter(is_original=False).order_by("-eyes_count")

	if allBlogs.count() > MAX_MENU_DISPLAY:
		allBlogs = allBlogs[0:MAX_MENU_DISPLAY]

	convert(allBlogs)

	return allBlogs

def getBlogMask():
	BlogMask = BlogCategory.objects.all()

	retBlogMask = []

	for k in range(BlogMask.count()):
		temp = {}
		temp['name'] = BlogMask[k].name
		temp['count'] = BlogMask[k].blog_set.all().count()
		retBlogMask.append(temp)

	return retBlogMask

def getBlogDate():
	BlogDate = BlogDateCategory.objects.all()

	return BlogDate

def getCommonInfo():
	newblogs=getNewArticle()
	recommendblogs = getRecommendArticle()
	randomblogs = getRandomArticle()
	notoriginalBlogs = getNotOriginal()
	blogmask = getBlogMask()
	blogdate = getBlogDate()
	context={'MAX_SIDE_DISPLAY':MAX_SIDE_DISPLAY,
			'topnewblogs':newblogs,
			'newblogs':newblogs,
			'recommendblogs':recommendblogs,
			'notoriginalblogs':notoriginalBlogs,
			'randomblogs':randomblogs,
			'blogmask':blogmask,
			'blogdate':blogdate,
			}
	return context

def article(request, blog_id):
	blog = Blog.objects.get(pk=blog_id)
	template = loader.get_template('myblog/blogcontent.html')
	context = getCommonInfo()

	blog.eyes_count = blog.eyes_count+1
	blog.save()

	blog.img_path = blog.img_path[len("myblog"):]

	date = "%d-%02d-%02d"%(blog.pub_date.year, blog.pub_date.month, blog.pub_date.day)
	blog.pub_date = date

	if blog.is_original == True:
		blog.is_original = "原创"
	else:
		blog.is_original = "转载"

	context['blog'] = blog

	return HttpResponse(template.render(context))

def index(request):
	template = loader.get_template('myblog/index.html')
	context = getCommonInfo()
	pages = getIndexPage()
	context['pages'] = pages
	context['curpage'] = 1
	return HttpResponse(template.render(context))

def indexPage(request, page):
	template = loader.get_template('myblog/index.html')
	context = getCommonInfo()
	page = int(page)
	pages = getIndexPage(page)
	context['pages'] = pages
	context['curpage'] = page
	#刷新最新文章
	begin = (page-1)*MAX_MENU_DISPLAY
	end = page*MAX_MENU_DISPLAY
	allBlogs = Blog.objects.order_by('-id')
	allnum = allBlogs.count()
	if allnum >= end:
		allBlogs = allBlogs[begin:end]
	elif allnum >= begin:
		allBlogs = allBlogs[begin:allnum]
	else:
		allBlogs = {}

	convert(allBlogs)

	context['newblogs'] = allBlogs

	return HttpResponse(template.render(context))

def date(request, year, month):
	blogdate = BlogDateCategory.objects.all()

	for v in blogdate:
		if (str(v.year) == year) and (str(v.month) == month):
			tempdate = v

	blogList = tempdate.blog_set.all()

	if blogList.count() > MAX_MENU_DISPLAY:
		blogList = blogList[0:MAX_MENU_DISPLAY]

	convert(blogList)

	context = getCommonInfo()
	context['bloglist'] = blogList

	pages = getDatePage(year, month)
	context['pages'] = pages
	context['curpage'] = 1

	template = loader.get_template('myblog/blogcategory.html')
	
	return HttpResponse(template.render(context))

def datePage(request, year, month, page):
	blogdate = BlogDateCategory.objects.all()

	for v in blogdate:
		if (str(v.year) == year) and (str(v.month) == month):
			tempdate = v

	blogList = tempdate.blog_set.all()
	context = getCommonInfo()

	page = int(page)
	pages = getDatePage(year, month, page)

	context['pages'] = pages
	context['curpage'] = page

	begin = (page-1)*MAX_MENU_DISPLAY
	end = page*MAX_MENU_DISPLAY
	
	allnum = blogList.count()
	if allnum >= end:
		blogList = blogList[begin:end]
	elif allnum >= begin:
		blogList = blogList[begin:allnum]
	else:
		blogList = {}

	convert(blogList)

	context['bloglist'] = blogList

	template = loader.get_template('myblog/blogcategory.html')
	
	return HttpResponse(template.render(context))

def mask(request, category):
	blogcategory = BlogCategory.objects.filter(name=category)

	blogList = blogcategory[0].blog_set.all()

	if blogList.count() > MAX_MENU_DISPLAY:
		blogList = blogList[0:MAX_MENU_DISPLAY]

	convert(blogList)

	context = getCommonInfo()
	context['bloglist'] = blogList

	pages = getMaskPage(category)
	context['pages'] = pages
	context['curpage'] = 1

	template = loader.get_template('myblog/blogcategory.html')
	
	return HttpResponse(template.render(context))

def category(request, types):
	blogtype = BlogType.objects.filter(name=types)

	blogList = blogtype[0].blog_set.all()

	if blogList.count() > MAX_MENU_DISPLAY:
		blogList = blogList[0:MAX_MENU_DISPLAY]

	convert(blogList)

	context = getCommonInfo()
	context['bloglist'] = blogList

	pages = getTypePage(types)
	context['pages'] = pages
	context['curpage'] = 1

	template = loader.get_template('myblog/blogcategory.html')
	
	return HttpResponse(template.render(context))

def aboutblog(request):
	template = loader.get_template('myblog/about.html')
	context = getCommonInfo()

	return HttpResponse(template.render(context))

def leavemessage(request):
	template = loader.get_template('myblog/leavemessage.html')
	context = getCommonInfo()

	return HttpResponse(template.render(context))