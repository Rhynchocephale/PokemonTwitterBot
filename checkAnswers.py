# -*- coding: UTF-8 -*-

import re
from toolbox import *
import bddAccess as bdd

insults = ["gueule", "ferme", "taggle", "pute", "connard", "emmerde", "chier", "fdp", "encule", "casse", "degage", "abruti", "bloque", "fuck", "fout", "nique", "tg", "osef", "stop", "stfu", "ntm", "ta mere"]

answeringBackEmojis = ["😧", "😕", "😟", "😒", "😥"]

lastId = lastAnswer()
twt = tweetQuery("@PkmnCheckerBot -filter:retweets", lastId)

answered = getAlreadyAnswered()
blocked = getBlockedUsers()

print("-------RECENT ANSWERS-------\n")
writeToLog("M: ---RECENT ANSWERS---\n")

for s in twt:
	content = s.text
	print(content)
	writeToLog("A from @"+s.user.screen_name+": "+content+"\n")

	if str(s.id) in answered:
		continue

	if s.id > lastId:
		lastId = s.id

	if str(s.user.screen_name) in blocked:
		writeToLog("W: user already blocked")
		continue

	#looks for badly written Pokémon names
	listOfWrong = checkForWrong(content)
	if len(listOfWrong) > 0:

		wtf = False
		m = "@"+s.user.screen_name.encode(encoding='UTF-8')+" "
		strOfWrong = strListToText(listOfWrong, len(m+"Ils s'appellent ")+2) #+2 for emoji

		if strOfWrong[1] == 1:
			whichCase = random.randint(0,5)

			if whichCase == 0:
				m += "Il s'appelle "+strOfWrong[0]+". Mais je crois bien que tu te moques de moi"
			elif whichCase == 1:
				m += "Je crois que tu as fait exprès de mal écrire "+strOfWrong[0]
			elif whichCase == 2:
				m += "Je te soupçonne d'avoir sciemment mal orthographié "+strOfWrong[0]
			elif whichCase == 3:
				m += "Il s'appelle "+ strOfWrong[0] + ". Mais tu dois déjà le savoir"
			elif whichCase == 4:
				m += "Tu as mal écrit "+ strOfWrong[0] + "exprès pour m'embêter, c'est ça ?"

		elif strOfWrong[1] > 1:
			m += "Ils s'appellent " + strOfWrong[0]

		else:
			print("SOMETHING IS VERY WRONG HERE")
			writeToLog("SOMETHING IS VERY WRONG HERE")
			wtf = True

		m += " "+answeringBackEmojis[random.randint(0,len(answeringBackEmojis)-1)]

		print("--ANSWERING BACK TO:--")
		print(content)

		if not wtf:
			q = api.update_status(m, s.id)
			break

	#looks for insults. Blocks user if detected.
	for swearword in insults:
		if re.search(swearword, content, re.IGNORECASE):
			if len(listOfWrong) == 0: #prevents answering twice
				api.update_status("@"+s.user.screen_name+" pic.twitter.com/ZZFVlapuhd", s.id)
			if not str(s.user.screen_name) in blocked:
				blockUser(s, swearword)
			print("DETECTED: "+swearword)
			writeToLog("B: "+ swearword + "found in " + content + "\n")
			break

	addToAnswered(s)

(cur, conn) = bdd.ouvrirConnexion()
try:
	bdd.executerReq(cur, "UPDATE answered SET isLast = 1 WHERE id = %s;" % (lastId))
	bdd.validerModifs(conn)
except Exception:
	raise
finally:
	bdd.fermerConnexion(cur, conn)
