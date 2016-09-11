# -*- coding: UTF-8 -*-

import re, datetime, os, time
from toolbox import *
import bddAccess as bdd

master = "Rhynchocephale"

def getLastDM():
	(cur, conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq(cur, "SELECT id FROM lastDM;")
		lastDM = cur.fetchone()[0]
	except Exception:
		raise
	finally:
		bdd.fermerConnexion(cur, conn)
	
	return lastDM

def setLastDM(value):
	(cur, conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq(cur, "UPDATE lastDM SET id="+value+";")
		bdd.validerModifs(conn)
	except Exception:
		raise
	finally:
		bdd.fermerConnexion(cur, conn)

	return 0  

def listOfIncorrect(exploded):
	return ",".join(exploded).replace(",-"," -").split(",")

def addOneMon(correct, listOfIncorrect):
	if listOfIncorrect[-1].beginswith('emoji='):
		emoji = listOfIncorrect[-1]
		listOfIncorrect.pop()
	else:
		emoji = ""

	print(stuff)

	(cur,conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq(cur, "INSERT INTO corrections VALUES (%s, %s, %s, 0, 0);", (correct, listOfIncorrect, emoji))
		bdd.validerModifs(conn)
	except Exception:
		raise
		return 1
	finally:
		bdd.fermerConnexion(cur, conn)
		
	return 0
		
def addIdToAnswered(id_str):
	twtDate = datetime.datetime.today().strftime("%d-%m-%y")

	(cur,conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq(cur, "INSERT INTO answered (id, date) VALUES ('%s', '%s');" % (id_str, twtDate))
		bdd.validerModifs(conn)
	except Exception:
		raise
		return 1	 
	finally:
		bdd.fermerConnexion(cur, conn)
		
	return 0
		
def addNewSpelling(correct, listOfIncorrect):
	
	(cur,conn) = bdd.ouvrirConnexion()
	try:
		rowNumber = bdd.executerReq(cur, "SELECT listOfIncorrect FROM corrections WHERE correct = '"+correct+"';")
		if rowNumber:
			oldListOfIncorrect = cur.fetchone()[0].split(",")
		else:
			plop = addOneMon(correct, listOfIncorrect)
			return plop
	except Exception:
		raise
		return 1
	finally:
		bdd.fermerConnexion(cur, conn)

	for incorrect in oldListOfIncorrect
		for newSpelling in listOfIncorrect:
			oldSplit = incorrect.split(" -")
			newSplit = newSpelling.split(" -")

			if oldSplit[0] == newSplit[0]:
				negativeKeywords = []

				if len(oldSplit>1):
					negativeKeywords += oldSplit[1:]
				if len(newSplit>1):
					negativeKeywords += newSplit[1:]

				if negativeKeywords:
					listOfIncorrect[listOfIncorrect.index(newSpelling)] = newSplit[0] + " -" + " -".join(list(set(negativeKeywords)))

				break
		else:
			listOfIncorrent.append(incorrect)
	
	(cur, conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq("UPDATE corrections SET listOfIncorrects=%s WHERE correct = '%s';", (",".join(list(set(newSpellings))), correct))
		bdd.validerModifs(conn)
	except Exception:
		raise
		return 1
	finally:
		bdd.fermerConnexion(cur, conn)
	
	return 0

lastDM = getLastDM()
dm = api.direct_messages(since_id = lastDM, full_text=True)

for s in dm:
	if s.id > int(lastDM):
		lastDM = s.id

	sn = s.sender.screen_name
	if sn != master:
		continue
	
	content = s.text.split()
	command = content[0].lower()
	failed = False
	
	if command == "block":
		failed = manualBlock(content[1])
	elif command == "unblock":
		failed = manualUnblock(content[1])
	elif command == "add":
		failed = addOneMon(content[1], listOfIncorrect(content[2:]))
	elif command == "append":
		failed = addNewSpelling(content[2], listOfIncorrect(content[3:]))
	elif command == "rage":
		for iter in range(0,6):
			os.system("python3 twitterbot.py 1 "+content[2])
			time.sleep(60*8)
	elif command == "deal":
		os.system("python3 twitterbot.py 0 "+content[2])
	elif command == "ignore":
		failed = addIdToAnswered(content[1])
	else:
		failed = True
		
	answer = "You asked me to "+" ".join(content)+". "+["It is done, master", "I am afraid I did not succeed, my lord."][failed]
	api.send_direct_message(screen_name=masterName, text=answer)
	setLastDM(str(lastDM))
