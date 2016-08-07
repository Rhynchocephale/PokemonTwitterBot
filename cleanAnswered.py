# -*- coding: UTF-8 -*-

from toolbox import *
import datetime
import bddAccess as bdd

#remove tweets older than 3 days from now from the answered table
def cleanAnswered():
	tooOld = []
	answered = []

	(cur, conn) = bdd.ouvrirConnexion()
	try:
		bdd.executerReq(cur, "SELECT id, date, isLast FROM answered;")
		rows = cur.fetchall()
	except Exception:
		raise
	finally:
		bdd.fermerConnexion(cur, conn)

	for row in rows:
		twtDate = datetime.datetime.strptime(row[1], "%d-%m-%y\n").date()
		if (datetime.today() - twtDate).days < howOldAreTweets + 2:
			answered.append(row[0])
		else:
			tooOld.append(row[0])

	(cur, conn) = bdd.ouvrirConnexion()
	try:
		for _id in tooOld:
			bdd.executerReq(cur, "DELETE FROM answered WHERE id = %s;" % (_id))
		bdd.validerModifs(conn)
	except Exception:
		raise
	finally:
		bdd.fermerConnexion(cur, conn)

	return answered
