from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account
from django.db.models import Q
from django.db import transaction
import json
import requests



@login_required
def addView(request):
	Account.objects.create(owner=request.user, iban=request.POST.get('iban', '').strip(), balance=0)
	return redirect('/')


#@transaction.atomic
def transfer(sender, receiver, amount):
	acc1 = Account.objects.get(iban=sender)
	acc2 = Account.objects.get(iban=receiver)

	# Injection
	# if acc1.balance - amount < 0 or amount < 0 or acc1 == acc2:
	#	return None



	acc1.balance -= amount
	acc2.balance += amount
	acc2.save()
	acc1.save()

	return True
	

# CSRF flaw
@login_required
@csrf_exempt
def homePageView(request):
	error = None
	if request.method == 'POST':
		sender = request.POST.get('from')
		receiver = request.POST.get('to')
		amount = int(request.POST.get('amount'))
		print(sender, receiver, amount)
		if transfer(sender, receiver, amount) is None:
			print("Wrong")
			error = "Invalid values"

	accounts = Account.objects.all()
	context = {'accounts': accounts, 'error': error}
	return render(request, 'pages/index.html', context)

@login_required
def accountView(request, account):

	


	# Broken Access Control:
	#if account != request.user.username:
	# 	print("Error")
	#	return redirect("/")
	#accounts = Account.objects.filter(owner = request.user)

	accounts = Account.objects.filter(owner__username=account)
	context = {'accounts': accounts}

	# Server Side Request Forgery (SSRF)
	if request.method == 'POST':
		url = str(request.POST.get('url'))
		session = requests.Session()
		r = session.get(url)
		context['import'] = r.text

		# if url.startswith("https://www.kmafia"):
		#	session = requests.Session()
		#	r = session.get(url)
		#	context['import'] = r.text
		# else:
		#	context['import'] = "Invalid url"


	return render(request, 'pages/accounts.html', context)

def evilPageView(request):
    return render(request, 'pages/csrf.html')
