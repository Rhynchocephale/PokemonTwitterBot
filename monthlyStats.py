# -*- coding: UTF-8 -*-

from toolbox import *
import bddAccess as bdd

(cur, conn) = bdd.ouvrirConnexion()
try:
	bdd.executerReq(cur, "SELECT correct, monthlyCount FROM corrections ORDER BY monthlyCount DESC;")
	corrected = cur.fetchall()
except Exception:
	raise
bdd.fermerConnexion(cur, conn)

resetMonthlycount()
resetFailcount()

m = "Pokémon les plus corrigés du mois :\n"
i = 0
line = ""
while len(m+line) <= 140:
	m += line
	print(m)
	print(len(m))
	line = ""
	pokemons = []
	counter = corrected[i][1]
	while corrected[i][1] == counter:
		pokemons.append(corrected[i][0])
		i += 1
	line = ", ".join(pokemons)+" : "+str(counter)+" fois \n"

if i > 0:
	print(m)
	q = api.update_status(m.strip())
