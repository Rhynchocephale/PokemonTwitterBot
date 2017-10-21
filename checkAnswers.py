# -*- coding: UTF-8 -*-

import re
from toolbox import *
import bddAccess as bdd

insults = ["lache moi", "lâche moi", "suce ", "couille", "gueule", "ferme", "taggle", "pute", "connard", "emmerde", "chier", "fdp", "encule", "casse", "degage", "dégage", "abruti", "bloque", "fuck", "en fou", "foutr", "(^| )nique", "tg", "osef", "blk", "blc", "stop", "stfu", "ntm", "ta mere", "ta mère", "mentionne pa", "ballec", "balek", "balec", "ballek"]

answeringBackEmojis = ["😧", "😕", "😟", "😒", "😥"]

lastId = int(lastAnswer())
#twt = tweetQuery("@PkmnCheckerBot -filter:retweets", lastId)
#twt = tweetQuery("@PkmnCheckerBot -filter:retweets")
twt = api.mentions_timeline()

answered = getAlreadyAnswered()
blocked = getBlockedUsers()

print("-------RECENT ANSWERS-------\n")

print(datetime.datetime.now().isoformat())

for s in twt:

	addToAnswered(s)

	content = s.text
	sn = s.user.screen_name
	print(content)

	if str(s.id) in answered:
		continue

	if s.id > lastId:
		lastId = s.id

	if sn in blocked:
		#writeToLog("W: user already blocked")
		continue

	#looks for badly written Pokémon names
	listOfWrong = checkForWrong(content)
	correctWritings = [a[0] for a in listOfWrong]
	#print("Badly written Pokemon: ")
	print(correctWritings)
	if len(correctWritings) > 0:

		wtf = False
		m = "@"+sn+" "
		strOfWrong = strListToText(correctWritings, len(m+"Ils s'appellent ")+2) #+2 for emoji

		if strOfWrong[1] == 1:
			whichCase = random.randint(0,4)

			if whichCase == 0:
				m += "Il s'appelle "+strOfWrong[0]+". Mais je crois bien que tu te moques de moi"
			elif whichCase == 1:
				m += "Je crois que tu as fait exprès de mal écrire "+strOfWrong[0]
			elif whichCase == 2:
				m += "Je te soupçonne d'avoir sciemment mal orthographié "+strOfWrong[0]
			elif whichCase == 3:
				m += "Il s'appelle "+ strOfWrong[0] + ". Mais tu dois déjà le savoir"
			elif whichCase == 4:
				m += "Tu as mal écrit "+ strOfWrong[0] + " exprès pour m'embêter, c'est ça ?"

		elif strOfWrong[1] > 1:
			m += "Ils s'appellent " + strOfWrong[0]

		else:
			print("SOMETHING IS VERY WRONG HERE")
			#writeToLog("SOMETHING IS VERY WRONG HERE")
			wtf = True

		m += " "+answeringBackEmojis[random.randint(0,len(answeringBackEmojis)-1)]

		print("--ANSWERING BACK TO:--")
		print(content)

		if not wtf:
			try:
				q = api.update_status(m, s.id)
			except tweepy.TweepError:
				raise
			break

	#looks for insults. Blocks user if detected.
	for swearword in insults:
		if re.search(swearword, content, re.IGNORECASE):
			print("DETECTED: "+swearword)
			if len(correctWritings) == 0: #prevents answering twice
				try:
					api.update_status("@"+sn+" pic.twitter.com/ZZFVlapuhd", s.id)
				except tweepy.TweepError:
					raise
			if not sn in blocked:
				blockUser(s, swearword)
			#writeToLog("B: "+ swearword + "found in " + content + "\n")
			break

(cur, conn) = bdd.ouvrirConnexion()
try:
	bdd.executerReq(cur, "UPDATE isLast SET id = %s;" % str(lastId))
	bdd.validerModifs(conn)
except Exception:
	raise
finally:
	bdd.fermerConnexion(cur, conn)
