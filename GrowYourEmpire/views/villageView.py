from django.utils import timezone
from django.shortcuts import render,redirect
from GrowYourEmpire.database import utilityFunctions
from GrowYourEmpire.views import indexView
from GrowYourEmpire.models import TradeOffer, Training, Upgrade, Village, Activity, Attack, God, Event, DonationEvent
from django.core.exceptions import ObjectDoesNotExist
import logging, traceback

def saveAttack(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			defendant = Village.objects.get(villageName=request.POST['objective'])
			soldiers = request.POST['units']
			attacker = Village.objects.get(owner=request.user.student)
			wantedResource = request.POST['wantedResource']
			if attacker == None or defendant == "" or soldiers == "" or int(soldiers) > attacker.soldiers or int(soldiers) < 0 or attacker == defendant:
				return redirect(indexView.manager)
			else:
				attack = Attack(attacker=attacker,defendant=defendant,usedSoldiers=soldiers,registeredDateTime=timezone.now(),completed = False,wantedResource=wantedResource)
				attack.save()
				attacker.soldiers-=int(soldiers)
				attacker.save()
				attackActivityText='Has ordenado un ataque contra la aldea '+defendant.villageName+' con '+soldiers+' unidades'
				Activity(owner=attacker,activityText=attackActivityText,activityDate=timezone.now()).save()
				return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

		
def trade(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner = request.user.student)
			villages = Village.objects.exclude(owner=request.user.student)
			return render(request,'GrowYourEmpire/trade.html',{'village':village,'villages':villages})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def attack(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			villages = Village.objects.exclude(owner=request.user.student)
			return render(request,'GrowYourEmpire/attack.html',{'villages':villages,'village':village})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def upgrade(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			upgrades = Upgrade.objects.filter(village = village,completed = 0)
			available = [1,2,3,4,5]
			if village.foodLevel == 100:
				available.remove(1)
			if village.woodLevel == 100:
				available.remove(2)
			if village.stoneLevel == 100:
				available.remove(3)
			if village.wallLevel == 20:
				available.remove(4)
			if village.storageLevel == 19:
				available.remove(5)
			for upgrade in upgrades:
				try:
					available.remove(upgrade.building)
				except ValueError: #Already removed
					pass
			return render(request,'GrowYourEmpire/upgrade.html',{'village':village,'upgrades':available})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def train(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			return render(request,'GrowYourEmpire/training.html',{'village':village,'maxSoldiers':village.storedFood//2})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def saveTrade(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			seller = Village.objects.get(owner=request.user.student)
			buyer = Village.objects.get(villageName = request.POST['target'])
			wantedRes = [request.POST['wantedWood'],request.POST['wantedStone'],request.POST['wantedFood']]
			offeredRes = [request.POST['offeredWood'],request.POST['offeredStone'],request.POST['offeredFood']]
			if (wantedRes[0] == "" or wantedRes[1] == "" or wantedRes[2] == "" or offeredRes[0]== "" or offeredRes[1]== "" or offeredRes[2]== "") or (int(wantedRes[0]) == 0 and int(wantedRes[1]) == 0 and int(wantedRes[2]) == 0 and int(offeredRes[0])== 0 and int(offeredRes[1])==0  and int(offeredRes[2])== 0) or int(offeredRes[0])>seller.storedWood or int(offeredRes[1]) > seller.storedStone or int(offeredRes[2]) > seller.storedFood or int(offeredRes[0]) < 0 or int(offeredRes[1]) < 0 or int(offeredRes[2]) < 0 or int(wantedRes[0]) < 0 or int(wantedRes[1]) < 0 or int(wantedRes[2]) < 0 or seller == buyer:
				#not enough resources to trade, or negative resources
				return redirect(indexView.manager)
			else:
				tradeOffer = TradeOffer(source=seller, destination=buyer,wantedWood=wantedRes[0],wantedStone=wantedRes[1],wantedFood=wantedRes[2],offeredWood=offeredRes[0],offeredStone=offeredRes[1],offeredFood=offeredRes[2],accepted=False,registeredDateTime=timezone.now())
				tradeOffer.save()
				seller.storedWood-=int(offeredRes[0])
				seller.storedStone-=int(offeredRes[1])
				seller.storedFood-=int(offeredRes[2])
				seller.save()
				Activity(owner=seller,activityText='Has ofrecido un intercambio de recursos a '+buyer.villageName, activityDate=timezone.now()).save()
				Activity(owner=buyer,activityText=seller.villageName+' te ofrece un intercambio de recursos.', activityDate=timezone.now()).save()
				return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def saveUpgrade(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			building = int(request.POST['selectedIndex'])
			if(building < 1 or building > 5):
				return redirect(indexView.manager)
			elif building == 1: #food
				if village.foodLevel == 100:
					return redirect(indexView.manager)
				level = village.foodLevel+1
				woodCost = village.foodLevel * 7
				stoneCost = village.foodLevel * 3

			elif building == 2: #wood
				if village.woodLevel == 100:
					return redirect(indexView.manager)
				level = village.woodLevel+1
				woodCost = village.woodLevel * 7
				stoneCost = village.woodLevel * 3

			elif building == 3: #stone
				if village.stoneLevel == 100:
					return redirect(indexView.manager)
				level = village.stoneLevel+1
				woodCost = village.stoneLevel * 7
				stoneCost = village.stoneLevel * 3

			elif building == 4: #wall
				if village.wallLevel == 20:
					return redirect(indexView.manager)
				level = village.wallLevel+1
				woodCost = village.wallLevel * 10
				stoneCost = village.wallLevel * 20

			elif building == 5: #storage
				if village.storageLevel == 20:
					return redirect(indexView.manager)
				level = village.storageLevel+1
				woodCost = village.storageLevel * 20
				stoneCost = village.storageLevel * 10

			if village.storedWood < woodCost or village.storedStone < stoneCost:
				return redirect(indexView.manager)
			else:
				try:
					Upgrade.objects.get(village = village,completed = False,building = building)
					return redirect(indexView.manager)
				except ObjectDoesNotExist:
					village.storedWood-=woodCost
					village.storedStone-=stoneCost
					village.save()
					buildings = ["Granja","Aserradero","Cantera","Muralla","Almacenamiento"]
					upgradeActivityText='Has comenzado a mejorar tu '+buildings[building-1]+' al nivel '+ str(level)
					Activity(owner=village,activityText=upgradeActivityText,activityDate=timezone.now()).save()
					Upgrade(village=village, level = level,building=building,woodCost = woodCost, stoneCost=stoneCost,completed=False, registeredDateTime=timezone.now()).save()
					return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def saveTraining(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			soldiers = int(request.POST['amount'])
			if village.storedFood < int(soldiers)*2 or soldiers < 0:
				return redirect(indexView.manager)
			else:
				village.storedFood-=(soldiers*2)
				village.save()
				training = Training(village=village,units=soldiers,foodCost=soldiers*2,completed=False,registeredDateTime=timezone.now())
				training.save()
				trainActivityText='Has comenzado a entrenar a '+str(soldiers)+' unidad(es)'
				Activity(owner=village,activityText=trainActivityText,activityDate=timezone.now()).save()
				return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def manageTrade(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			offersOwned = TradeOffer.objects.filter(source=village,accepted=False)
			offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
			for offer in offersOwned:
				offer.id=str(hash(str(offer.id)))
			for offer in offersReceived:
				offer.id=str(hash(str(offer.id)))
			return render(request,'GrowYourEmpire/manageTrade.html',{'village':village,'offersOwned':offersOwned,'offersReceived':offersReceived})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def cancelOffer(request,offerHash):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			offersOwned = TradeOffer.objects.filter(source=village,accepted=False)
			for offer in offersOwned:
				if str(hash(str(offer.id))) == offerHash:
					offer.accepted=True
					offer.save()
					Activity(owner=offer.source,activityText='Has cancelado el intercambio de recursos con '+offer.destination.villageName, activityDate=timezone.now()).save()
					Activity(owner=offer.destination,activityText=offer.source.villageName+' ha cancelado el intercambio de recursos contigo', activityDate=timezone.now()).save()
					village.storedWood+=offer.offeredWood
					village.storedStone+=offer.offeredStone
					village.storedFood+=offer.offeredFood
					village.save()
					break;
			return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def acceptOffer(request,offerHash):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
			for offer in offersReceived:
				if str(hash(str(offer.id))) == offerHash:
					if village.storedWood < offer.wantedWood or village.storedStone < offer.wantedStone or village.storedFood<offer.wantedFood:
						activities = utilityFunctions.getActivities(village)
						return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'No tienes recursos suficientes para aceptar la oferta'})
					else:
						offer.accepted=True
						offer.save()
						Activity(owner=offer.destination,activityText='Has aceptado el intercambio de recursos con '+offer.source.villageName, activityDate=timezone.now()).save()
						Activity(owner=offer.source,activityText=offer.destination.villageName+' ha aceptado el intercambio de recursos contigo', activityDate=timezone.now()).save()
						village.storedWood-=offer.wantedWood
						village.storedStone-=offer.wantedStone
						village.storedFood-=offer.wantedFood
						village.storedWood+=offer.offeredWood
						village.storedStone+=offer.offeredStone
						village.storedFood+=offer.offeredFood
						village.save()
						source = offer.source
						source.storedWood+=offer.wantedWood
						source.storedStone+=offer.wantedStone
						source.storedFood+=offer.wantedFood
						source.save()
						activities = utilityFunctions.getActivities(village)		
						return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Oferta aceptada'})
			return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})
	
def rejectOffer(request,offerHash):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			offersReceived = TradeOffer.objects.filter(destination=village,accepted=False)
			for offer in offersReceived:
				if str(hash(str(offer.id))) == offerHash:
					offer.accepted=True
					offer.save()
					Activity(owner=offer.destination,activityText='Has rechazado el intercambio de recursos con '+offer.source.villageName, activityDate=timezone.now()).save()
					Activity(owner=offer.source,activityText=offer.destination.villageName+' ha rechazado el intercambio de recursos contigo', activityDate=timezone.now()).save()
					source = offer.source
					source.storedWood+=offer.offeredWood
					source.storedStone+=offer.offeredStone
					source.storedFood+=offer.offeredFood
					source.save()
					break
			return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})
	
def events(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			events = Event.objects.filter(startDate__lte=timezone.now(),endDate__gte=timezone.now())
			return render(request,'GrowYourEmpire/events.html',{'village':village,'events':events})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def event(request,eventId):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			event = Event.objects.get(pk=eventId)
			donations = DonationEvent.objects.filter(event=event)
			return render(request,'GrowYourEmpire/event.html',{'village':village,'event':event,'donations':donations})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def donateEvent(request,eventId):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			event = Event.objects.get(id=eventId)
			if (event.foodRequired > 0 and request.POST['foodDonated']!= ""):
				donatedFood = int(request.POST['foodDonated'])
			else:
				donatedFood = 0
			if (event.woodRequired > 0 and request.POST['woodDonated']!= ""):
				donatedWood = int(request.POST['woodDonated'])
			else:
				donatedWood = 0
			if (event.stoneRequired > 0 and request.POST['stoneDonated']!= ""):
				donatedStone = int(request.POST['stoneDonated'])
			else:
				donatedStone = 0
			if (event.soldiersRequired > 0 and request.POST['soldiersDonated'] != ""):
				donatedSoldiers = int(request.POST['soldiersDonated'])
			else:
				donatedSoldiers = 0
			if (donatedFood < 0 or donatedWood < 0 or donatedStone < 0 or donatedSoldiers < 0) or (donatedFood > event.foodRequired or donatedWood > event.woodRequired or donatedStone > event.stoneRequired or donatedSoldiers > event.soldiersRequired) or (donatedFood > village.storedFood or donatedWood > village.storedWood or donatedStone > village.storedStone or donatedSoldiers > village.soldiers or (donatedFood == 0 and donatedWood == 0 and donatedStone == 0 and donatedSoldiers == 0)):
				return redirect(indexView.manager)
			else:
				village.storedFood-=donatedFood
				village.storedWood-=donatedWood
				village.storedStone-=donatedStone
				village.soldiers-=donatedSoldiers
				village.save()
				event = Event.objects.get(id=eventId)
				event.foodRequired-=donatedFood
				event.woodRequired-=donatedWood
				event.stoneRequired-=donatedStone
				event.soldiersRequired-=donatedSoldiers
				event.save()
				donation = DonationEvent(event=event,owner=village,donatedFood=donatedFood,donatedWood=donatedWood,donatedStone=donatedStone,donatedSoldiers=donatedSoldiers)
				donation.save()
				if (donatedFood > 0):
					Activity(owner=village,activityText='Has donado '+str(donatedFood)+' comida al evento '+str(event.title),activityDate=timezone.now()).save()
				if (donatedWood > 0):
					Activity(owner=village,activityText='Has donado '+str(donatedWood)+' madera al evento '+str(event.title),activityDate=timezone.now()).save()
				if (donatedStone > 0):
					Activity(owner=village,activityText='Has donado '+str(donatedStone)+' piedra al evento '+str(event.title),activityDate=timezone.now()).save()
				if (donatedSoldiers > 0):
					Activity(owner=village,activityText='Has donado '+str(donatedSoldiers)+' soldados al evento '+str(event.title),activityDate=timezone.now()).save()
				return redirect(indexView.manager)
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})

def gods(request):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			gods = God.objects.all()
			return render(request,'GrowYourEmpire/gods.html',{'village':village,'gods':gods})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})
	
def saveGod(request,godName):
	logger = logging.getLogger('GrowYourEmpire')
	if not request.user.is_authenticated:
		return render(request,'GrowYourEmpire/login.html',{'msg':'Es necesario iniciar sesión para acceder a la página solicitada'})
	else:
		try:
			village = Village.objects.get(owner=request.user.student)
			if(village.storedFood < 1000 or village.storedWood < 1000 or village.storedStone < 1000):
				return redirect(indexView.manager)
			else:
				selectedGod = God.objects.get(name=godName)
				village.god = selectedGod
				village.storedFood-=1000	
				village.storedWood-=1000
				village.storedStone-=1000
				village.save()
				activities = utilityFunctions.getActivities(village)
				return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Tu aldea ha sido bendecida por '+selectedGod.name})
		except Exception:
			logger.exception(traceback.format_exc())
			village = Village.objects.get(owner=request.user.student)
			activities = utilityFunctions.getActivities(village)
			return render(request,'GrowYourEmpire/manager.html',{'village':village,'activities':activities,'text':'Se ha producido un error. Contacta con el administrador de la aplicación'})
		