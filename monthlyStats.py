# -*- coding: UTF-8 -*-

from toolbox import *
import bddAccess as bdd

def addOneMon(m, corrected, i):
	if i >= len(corrected) or i < 0:
		return m
	return m+corrected[i][0]+" : "+str(corrected[i][1])+" fois\n"

(cur, conn) = bdd.ouvrirConnexion()
try:
	bdd.executerReq(cur, "SELECT correct, monthlyCount FROM corrections ORDER BY monthlyCount DESC LIMIT 5;")
	corrected = cur.fetchall()
	bdd.executerReq(cur, "UPDATE corrections SET monthlyCount = 0;")
	bdd.validerModifs(conn)
except Exception:
	raise
bdd.fermerConnexion(cur, conn)

m = "Les 5 Pokémon les plus corrigés du mois :\n"
i = 0
while len(addOneMon(m, corrected, i)) <= 140 and i <= 5:
	m = addOneMon(m, corrected, i)
	i += 1

if i < 5:
	m = m.replace("5", str(i), 1)

if i > 0:
	q = api.update_status(m)
