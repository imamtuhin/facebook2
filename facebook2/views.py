from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Story
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


@login_required
def homepage(request):
	context = {
		'phone': '123',
		'posts': Story.objects.all().order_by('-date')
	}
	return render(request, 'facebook2/index.html', context)

def profile(request):
	context = {
		'phone': '123',
		'posts': Story.objects.filter(author=request.user).order_by('-date')
	}
	return render(request, 'facebook2/profile.html',context)


 
def signin(request):
	if (request.method == 'GET'):
		return render(request, 'facebook2/signin.html')
	elif (request.method == 'POST'):
		u = request.POST.get('user', '')
		p = request.POST.get('pass', '')
		user = authenticate(username=u, password=p)
		if user is None:
			messages.error(request, "Invalid username or password")
			return render(request, 'facebook2/signin.html')
			# return HttpResponse('Invalid password')
		else:
			login(request, user)
			return redirect('homepage')
			# return HttpResponse('Correct password')

@login_required
def addpost(request):
	c = request.POST.get('content', '')
	t = request.POST.get('tags', '')
	u = request.user
	s1 = Story(content=c, tags=t, author=u)
	s1.save()
	messages.info(request, 'Post succesfully created!')
	return redirect('homepage')

@login_required
def editpost(request, id):
	s1 = Story.objects.get(id=id)

	if (request.user != s1.author):
		return redirect('homepage')
	if (request.method == 'GET'):
		return render(request, 'facebook2/editpost.html', {'old_post': s1})
	else:
		s1.content = request.POST.get('content', '')
		s1.tags = request.POST.get('tags', '')
		s1.date = timezone.now()
		s1.save()
		messages.info(request, 'Post updated succesfully!')
		return redirect('homepage')

@login_required
def deletepost(request, id):
	s1 = Story.objects.get(id=id)
	if (request.user != s1.author):
		return redirect('homepage')

	if (request.method == 'GET'):
		return render(request, 'facebook2/deletepost.html', {'old_post': s1})
	else:
		s1.delete()
		messages.info(request, 'Post deleted!')
		return redirect('homepage')

def signout(request):
	logout(request)
	return redirect('signin')