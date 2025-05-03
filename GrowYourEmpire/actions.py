from datetime import timedelta
from django.utils import timezone
from GrowYourEmpire.models import Bonus, Training, Upgrade, Village, Activity, Attack
import random, traceback
import logging

def processUpgrades():
	upgrades = Upgrade.objects.filter(completed=False)
	for upgrade in upgrades:
		village = Village.objects.get(owner = upgrade.village)
		if upgrade.building == 1: #food
			village.foodLevel += 1
			village.dailyFood += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu granja al nivel '+ str(village.foodLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 2: #wood
			village.woodLevel += 1
			village.dailyWood += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu aserradero al nivel '+ str(village.woodLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 3: #stone
			village.stoneLevel +=1
			village.dailyStone +=1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu cantera al nivel '+ str(village.stoneLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 4: #wall
			village.wallLevel += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu muralla al nivel '+ str(village.wallLevel),activityDate=timezone.now(),owner=village).save()
		elif upgrade.building == 5: #storage
			village.storageLevel += 1
			village.save()
			Activity(activityText='Ha finalizado la mejora de tu almacén al nivel '+ str(village.storageLevel),activityDate=timezone.now(),owner=village).save()
		upgrade.completed=True
		upgrade.save()
	return True

def processTraining():
	trainings = Training.objects.filter(completed=False)
	for training in trainings:
		village = Village.objects.get(owner=training.village)
		village.soldiers += training.units
		village.save()
		Activity(activityText='Ha finalizado el entrenamiento de '+ str(training.units)+' unidad(es)',activityDate=timezone.now(),owner=village).save()
		training.completed = True;
		training.save()
	return True
	
def processAttack():
	attacks = Attack.objects.filter(completed=False)
	for attack in attacks:
		attacker = Village.objects.get(owner = attack.attacker)
		defendant = Village.objects.get(owner = attack.defendant)
		if (defendant.god == 'Zeus'):
			defendant_virtualUnits = round(defendant.soldiers*(1+0.06*defendant.wallLevel))
		else:
			defendant_virtualUnits = round(defendant.soldiers*(1+0.05*defendant.wallLevel))
		if attack.usedSoldiers > defendant_virtualUnits: #attacker wins
			lostSoldiers = round(defendant_virtualUnits)
			remainingSoldiers = attack.usedSoldiers
			while lostSoldiers > 0:
				if (attacker.god == 'Hades'):
					if (random.randint(1,100) < 75): #25% chance of surviving.
						remainingSoldiers -= 1
					lostSoldiers -=1
				else:
					remainingSoldiers -= lostSoldiers
					lostSoldiers = 0
			if (attacker.god == 'Poseidón'):
				maxResources = remainingSoldiers * 10
			else:
				maxResources = remainingSoldiers*5
			availableResources = [
				round(defendant.storedFood*(1-0.05*defendant.storageLevel)),
				round(defendant.storedWood*(1-0.05*defendant.storageLevel)),
				round(defendant.storedStone*(1-0.05*defendant.storageLevel))]
			stolenResources = [0,0,0]
			while maxResources > 0:
				if (availableResources[attack.wantedResource] > 0): #there's resources available from the desired type
					availableResources[attack.wantedResource] = min(availableResources[attack.wantedResource],maxResources)
					maxResources -= availableResources[attack.wantedResource]
					stolenResources[attack.wantedResource] = availableResources[attack.wantedResource]
					availableResources[attack.wantedResource] -= stolenResources[attack.wantedResource]
				else:
					if (availableResources[0] > 0): #get food
						availableResources[0] = min(availableResources[0],maxResources)
						maxResources -= availableResources[0]
						stolenResources[0] += availableResources[0]
						availableResources[0] -= stolenResources[0]
					elif (availableResources[1] > 0): #get wood
						availableResources[1] = min(availableResources[1],maxResources)
						maxResources -= availableResources[1]
						stolenResources[1] += availableResources[1]
						availableResources[1] -= stolenResources[1]
					elif (availableResources[2] > 0): #get stone
						availableResources[2] = min(availableResources[2],maxResources)
						maxResources -= availableResources[2]
						stolenResources[2] += availableResources[2]
						availableResources[2] -= stolenResources[2]
					else:
						break

			Activity(
				activityText=str(attacker.villageName)+' te ha atacado. Has perdido '+str(defendant.soldiers)+' soldados y te han saqueado '+str(stolenResources[0])+' de alimento, '+str(stolenResources[1])+' de madera y '+str(stolenResources[2])+' de piedra'
				,activityDate=timezone.now(),owner=defendant).save()
			Activity(
				activityText='Has atacado a '+str(defendant.villageName)+' y has ganado. Han vuelto '+str(remainingSoldiers)+' soldados y has saqueado '+str(stolenResources[0])+' de alimento, '+str(stolenResources[1])+' de madera y '+str(stolenResources[2])+' de piedra'
				,activityDate=timezone.now(),owner=attacker).save()
			defendant.soldiers = 0
			defendant.storedFood -= stolenResources[0]
			defendant.storedWood -= stolenResources[1]
			defendant.storedStone -= stolenResources[2]
			defendant.save()
			attacker.soldiers += remainingSoldiers
			attacker.storedFood += stolenResources[0]
			attacker.storedWood += stolenResources[1]
			attacker.storedStone += stolenResources[2]
			attacker.save()
		else: #defendant wins
			if defendant_virtualUnits - attack.usedSoldiers > defendant.soldiers: #defendant lost no soldiers
				Activity(
				activityText=attacker.villageName+' te ha atacado con '+str(attack.usedSoldiers)+' unidades. Tus soldados han repelido el ataque. No has perdido soldados ni recursos'
				,activityDate=timezone.now(),owner=defendant).save()
			else:
				lostSoldiers = defendant.soldiers - (defendant_virtualUnits - attack.usedSoldiers)
				Activity(
				activityText=attacker.villageName+' te ha atacado con '+str(attack.usedSoldiers)+' unidades. Tus soldados han repelido el ataque. Has perdido '+str(lostSoldiers)+' soldados, pero no has perdido recursos'
				,activityDate=timezone.now(),owner=defendant).save()
				defendant.soldiers-=lostSoldiers
				defendant.save()
			Activity(
				activityText='Has atacado a '+defendant.villageName+'. Sus soldados han repelido el ataque. Has perdido los '+str(attack.usedSoldiers)+' soldados empleados en el ataque'
				,activityDate=timezone.now(),owner=attacker).save()
		attack.completed = True
		attack.save()	
	return True
	
def addResources():
	villages = Village.objects.filter(disabled = False)
	for village in villages:
		bonuses = Bonus.objects.filter(village = village, completed = False, bonusType = 0)
		totalMultiplier = 1.0
		for bonus in bonuses:
			totalMultiplier+=(bonus.bonusAmount/10)
			bonus.remainingTicks-=1
			if bonus.remainingTicks == 0:
				bonus.completed = True
			bonus.save()
		village.storedFood += round(village.dailyFood)*totalMultiplier
		village.storedWood += round(village.dailyWood)*totalMultiplier
		village.storedStone += round(village.dailyStone)*totalMultiplier
		village.save()
	return True

def processBonuses():
	bonuses = Bonus.objects.filter(completed = False).exclude(bonusType = 0)
	for bonus in bonuses:
		village = Village.objects.get(owner = bonus.village)
		if bonus.bonusType == 1: #units
			village.soldiers += bonus.bonusAmount
		elif bonus.bonusType == 2: #building
			if bonus.bonusAmount == 0: #food
				village.foodLevel += 1
			elif bonus.bonusAmount == 1: #wood
				village.woodLevel += 1
			elif bonus.bonusAmount == 2: #stone
				village.stoneLevel += 1
			elif bonus.bonusAmount == 3: #walls
				village.wallLevel += 1
			elif bonus.bonusAmount == 4: #storage
				village.storageLevel += 1
		village.save()
		bonus.completed = True
		bonus.save()
	return True

def disableVillages():
	startDate = timezone.now()
	endDate = startDate - timedelta(days=3)
	villages = Village.objects.filter(lastLogin__lt = endDate)
	for village in villages:
		village.disabled = True
		village.save()
	return True

def main():
	logger = logging.getLogger('cronjob')
	logger.info("Starting cronjob")
	try:
		disableVillages()
		processBonuses()
		processUpgrades()
		processTraining()
		processAttack()
		addResources()
		logger.info("Cronjob completed")
	except Exception:
		logger.exception(traceback.format_exc())
	finally:
		logger.close()

if __name__ == "__main__":
    main()
