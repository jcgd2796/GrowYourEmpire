from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth import login as loginAuth, logout as logoutAuth
from GrowYourEmpire.models import Test,Question, Option,Village,New, Suggestion
from django.contrib.auth.models import User as User
from GrowYourEmpire.database import utilityFunctions
import logging, traceback
from django.utils.html import escape

def rules(request):
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		return render(request,'GrowYourEmpire/rules.html')

def ranking(request):
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		villages = Village.objects.all()
		villagesDict = {}
		for village in villages:
			punt = 0;
			punt += village.storedFood + village.storedWood + village.storedStone + 10*(village.foodLevel+village.woodLevel+village.stoneLevel+village.wallLevel+village.storageLevel)+(2*village.soldiers)
			villagesDict[village.villageName]=punt
		sorteddict = dict(sorted(villagesDict.items(),key=lambda x:x[1],reverse=True)[:5])
	return render(request,'GrowYourEmpire/ranking.html',{'ranking':sorteddict})

def index(request):
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		if request.user.is_superuser:
			tests = Test.objects.all()
		else:
			tests = Test.objects.filter(subject__in=list(request.user.student.subject.all()), date__lt = timezone.now())
		news = New.objects.all().order_by("-registeredDateTime")	
		return render(request,'GrowYourEmpire/index.html',{'tests':tests,'news':news})

def login(request):
	logger = logging.getLogger('GrowYourEmpire')
	try:
		usr = request.POST['user']
		pas = request.POST['password']
		user = authenticate(request,username=usr,password = pas)
		if user is not None:
			loginAuth(request,user)
			return redirect('index')
		else:
			return render(request,'GrowYourEmpire/login.html',{'msg':'Usuario o contraseña incorrectos.'})
	except Exception:
		logger.exception(traceback.format_exc())
		return render(request,'GrowYourEmpire/login.html',{'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def logout(request):
	logoutAuth(request)
	return render(request,'GrowYourEmpire/login.html',{'msg':'Sesión finalizada correctamente'})

def test(request,testN):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			t = Test.objects.get(testName=testN)
			questions = list(Question.objects.filter(testName=t))
			questionOpts = []
			for question in questions:
				if question.questionType == "Opciones":
					questionOpts.extend(Option.objects.filter(questionText = question))
			return render(request,'GrowYourEmpire/test.html',{'testName':testN,'questions':questions,'questionOpts':questionOpts})
		except Exception:
			logger.exception(traceback.format_exc())
			return render(request,'GrowYourEmpire/index.html',{'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def manager(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner = request.user.student)
			utilityFunctions.updateVillage(village.villageName)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities})
		except Exception:
			logger.exception(traceback.format_exc())
			return render(request,'GrowYourEmpire/index.html',{'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def new (request,newTitle):
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		new = New.objects.filter(title=newTitle)	
		return render(request,'GrowYourEmpire/new.html',{'news':new})
	
def suggestions (request):
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:	
		return render(request,'GrowYourEmpire/suggestions.html',{'news':new})
	
def saveSuggestion(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			suggestion = escape(request.POST['suggestion'])
			if suggestion == None or suggestion == "":
				return redirect(index)
			else:
				Suggestion(title=request.user,desc=suggestion,registeredDateTime=timezone.now()).save()
				return render(request,'GrowYourEmpire/index.html',{'text':'Sugerencia enviada correctamente'})

		except Exception:
			logger.exception(traceback.format_exc())
			return render(request,'GrowYourEmpire/index.html',{'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

