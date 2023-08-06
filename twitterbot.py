# -*- coding: UTF-8 -*-

import time, random, re, datetime, sys, os
from toolbox import *
import bddAccess as bdd

random.seed()

badTweet = ""
badMon = ""
maxTweetSize = 280-2

print(sys.argv)

#1st argument is 0 (answer to tweet number arg[2]) or 1 (rage against arg[2])
if(len(sys.argv) == 3):
    if sys.argv[1] == "0":
          badTweet = sys.argv[2]
    elif sys.argv[1] == "1":
          badMon = sys.argv[2]

def createPokemonTable():
    (cur,conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "CREATE TABLE corrections (correct VARCHAR(12), listOfIncorrect TEXT, emoji TEXT, overallCount MEDIUMINT UNSIGNED, monthlyCount SMALLINT UNSIGNED, PRIMARY KEY (correct));")
        for row in corrections:
            emoji = ""
            if len(row) > 2:
                emoji = row[2]
            bdd.executerReq(cur, "INSERT INTO corrections (correct, listOfIncorrect, emoji, overallCount, monthlyCount) VALUES (%s, %s, %s, 0, 0);", (row[0], list2str(row[1]), emoji))
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0

def addEmojisToPkmn():
    (cur,conn) = bdd.ouvrirConnexion()
    try:
        for row in corrections:
            emoji = ""
            if len(row) > 2:
                emoji = row[2]
            bdd.executerReq(cur, "UPDATE corrections SET emoji = '%s' WHERE correct = '%s';" % (emoji, row[0]))
            #if not cur.rowcount:
                #bdd.executerReq(cur, "INSERT INTO corrections (correct, listOfIncorrect, emoji, overallCount, monthlyCount) VALUES (%s, %s, %s, 0, 0);", (row[0], list2str(row[1]), emoji))
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0

def insertPokemon():
    (cur,conn) = bdd.ouvrirConnexion()
    try:
        #bdd.executerReq(cur, "insert into corrections values ('Sarmuraï', 'sarmourai', '🎎', 0, 0);")
        #bdd.executerReq(cur, "delete from corrections where correct = 'Silvallié';")
        #bdd.executerReq(cur, "delete from corrections where correct = 'Ékaiser';")
        #bdd.executerReq(cur, "insert into corrections values ('Zéroïd', 'zeroide', '', 0, 0);")
        #bdd.executerReq(cur, "insert into corrections values ('Magearna', 'magerna', '🤖', 0, 0);")
        #bdd.executerReq(cur, "insert into corrections values ('Rapasdepic', 'rapacedepic', '', 0, 0);")
        #bdd.executerReq(cur, "insert into corrections values ('Psystigri', 'psistigri', '', 0, 0);")
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0

def populateAlreadyAnswered():
    f = open(os.path.join(here,"alreadyAnswered.txt"),"r")
    answered = []
    for line in f:
        answered.append(line)
    f.close()

    f = open(os.path.join(here,"lastReply.txt"),"r")
    lastId = f.readline().replace("\n","")
    f.close()

    (cur,conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "DROP TABLE alreadyAnswered; CREATE TABLE alreadyAnswered (id TEXT, date VARCHAR(8), isLast BOOL);")
        for line in answered:
            bdd.executerReq(cur, "INSERT INTO alreadyAnswered VALUES ('%s', '%s', 0);" % (line.split(", ")[0], line.split(", ")[1]))
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0

#createPokemonTable()
#populateAlreadyAnswered()
#addEmojisToPkmn()
#insertPokemon()

emojis = ["😉","😜","⚠","☝","😤","😐"]

answered = getAlreadyAnswered()
blocked = getBlockedUsers()

while True:

    correctlyWrittenPkmn, badlyWrittenPkmn = getFourPokemonToWorkOn()

    if badMon:
        pkmnToSearchFor = [badMon]
    else:
        pkmnToSearchFor = " OR ".join(badlyWrittenPkmn)

    badlyWrittenPkmn = [_.split(" -")[0].replace("(","").replace(")","") for _ in badlyWrittenPkmn]

    date_X_days_ago = datetime.date.today() - datetime.timedelta(days=howOldAreTweets)
    date_X_days_ago = date_X_days_ago.isoformat()

    myQuery = pkmnToSearchFor + " -from:pkmncheckerbot -RT lang:fr since:" + date_X_days_ago
    print(myQuery)

    if badTweet:
        twt = [getOneTweet(badTweet)]
    else:
        twt = tweetQuery(myQuery)

    random.shuffle(twt)

    indexOfTweet = 0
    for s in twt:
        time.sleep(3)
        indexOfTweet += 1

        content = s.full_text
        sn = s.user.screen_name

        if not badTweet:
            if str(s.id) in answered:
                print("Already answered")
                continue

            if s.in_reply_to_screen_name and "PkmnCheckerBot" in s.in_reply_to_screen_name and s.created_at > datetime.datetime.now() - datetime.timedelta(hours=2):
                print("I'll leave that to checkAnswers...")
                continue

            if re.search("|".join(badlyWrittenPkmn), sn, re.IGNORECASE):
                print("Incorrect in author pseudo: ",sn)
                continue

            if re.search("@\S*("+"|".join(badlyWrittenPkmn)+")", content, re.IGNORECASE):
                print("Incorrect in mention pseudo: "," ".join( [x.split(" ")[0] for x in content.split('@')[1::]] ))
                continue

            correctInText = False
            for correctMon in correctlyWrittenPkmn:
                if searchWord(toAscii(correctMon), toAscii(content)):
                    print("Correct in text")
                    correctInText = True
            if correctInText:
                continue

            if not re.search("|".join(badlyWrittenPkmn), content, re.IGNORECASE):
                print("No incorrect in text. Possibly in retweet. Content was:", content)
                continue

            if re.search("@Youtube", content, re.IGNORECASE):
                print("Youtube video")
                continue

            if sn in blocked:
                print("Blocked user")
                continue

        print(str(indexOfTweet)+"/"+str(len(twt))+": "+content)
        listOfWrong = checkForWrong(content)

        if not listOfWrong:
            print("This is weird, no wrong found.")
            continue

        #decrements failcount
        for element in listOfWrong:
            incrementFailcount(element[0], -1)

        m = "@"+sn+" "

        if len(listOfWrong) == 1 or strListToText([element[0] for element in listOfWrong], maxTweetSize-len("Ils s'appellent "))[1] < 2:
            whichCase = random.randint(0,30)

            if whichCase == 0:
                m += "Ça s'écrit " + listOfWrong[0][0]
            elif whichCase == 1:
                m += listOfWrong[0][1] + " ? Ce ne serait pas plutôt " + listOfWrong[0][0] + " ?"
            elif whichCase == 2:
                m += "C'est " + listOfWrong[0][0] + ", pas " + listOfWrong[0][1]
            elif whichCase == 3:
                m += "Son vrai nom c'est " + listOfWrong[0][0]
            elif whichCase == 4:
                m += "Point orthographe : ça s'écrit " + listOfWrong[0][0]
            elif whichCase == 5:
                m += "C'est \"" + listOfWrong[0][0] + '", voyons !'
            elif whichCase == 6:
                m += "Protip: c'est " + listOfWrong[0][0]
            elif whichCase == 7:
                m += "D'après mon Pokédex, ce Pokémon s'appelle " + listOfWrong[0][0]
            elif whichCase == 8:
                m += "Attention, ce Pokémon s'appelle en fait " + listOfWrong[0][0]
            elif whichCase == 9:
                m += listOfWrong[0][0] + ", pas " + listOfWrong[0][1] + " !"
            elif whichCase == 10:
                m += "Je pense que tu voulais dire " + listOfWrong[0][0]
            elif whichCase == 11:
                m += "Tu ne voulais pas dire " + listOfWrong[0][0] + ", plutôt ?"
            elif whichCase == 12:
                m += "Je crois que tu voulais plutôt parler " + ["de ","d'"][startsWithVowel(listOfWrong[0][0])] + listOfWrong[0][0]
            elif whichCase == 13:
                m += "Tu voulais dire " + listOfWrong[0][0] + ", je me trompe ?"
            elif whichCase == 14:
                m += "Ce ne serait pas " + listOfWrong[0][0] + ", plutôt ?"
            elif whichCase == 15:
                m += "En fait, son nom c'est " + listOfWrong[0][0]
            elif whichCase == 16:
                m += "Il s'appelle " + listOfWrong[0][0]
            elif whichCase == 17:
                m += "Ça s'écrit " + listOfWrong[0][0] + " ! " + toEmojis(listOfWrong[0][0]) + " !"
            elif whichCase == 18:
                m += "Il s'appelle " + listOfWrong[0][0] + " ! " + toEmojis(pkmnLine[0]) + " !"
            elif whichCase == 19:
                m += "Selon le Pokédex, le nom de ce truc c'est " + listOfWrong[0][0]
            elif whichCase == 20:
                m += listOfWrong[0][1] + ", ou " + listOfWrong[0][0] + " ?"
            elif whichCase == 21:
                m += "Je pinaille, mais ça s'écrit " + listOfWrong[0][0]
            elif whichCase == 22:
                m += "Point pinaillage relou : " + listOfWrong[0][1] + " s'écrit en fait " + listOfWrong[0][0]
            elif whichCase == 23:
                m += "C'est " + listOfWrong[0][0] + ", voyons ! Pas " + listOfWrong[0][1] + " !"
            elif whichCase == 24:
                m += "Ça s'écrit " + listOfWrong[0][0] + ". C'était pas évident, j'en conviens."
            elif whichCase == 25:
                m += "C'est pas forcément évident à écrire, mais il s'appelle " + listOfWrong[0][0]
            elif whichCase == 26:
                m += "Certes " + listOfWrong[0][0] + " n'a pas un nom facile, mais de là à l'écrire " + listOfWrong[0][1] + "..."
            elif whichCase == 27:
                m += "Il s'appelle " + listOfWrong[0][0] + ", ce n'est pourtant pas très compliqué"
            elif whichCase == 28:
                m += "Tu dois vouloir parler " + ["de ","d'"][startsWithVowel(listOfWrong[0][0])] + listOfWrong[0][0]
            elif whichCase == 29:
                m += listOfWrong[0][1] + " ? Un peu de respect pour " + listOfWrong[0][0] + ", enfin !"
            elif whichCase == 30:
                m += "En l'écrivant " + listOfWrong[0][0] + ", c'est bien mieux"

            (cur, conn) = bdd.ouvrirConnexion()
            try:
                bdd.executerReq(cur, "SELECT emoji FROM corrections WHERE correct = '"+listOfWrong[0][0]+"';")
                customEmoji = cur.fetchone()[0]
            except Exception:
                raise
            finally:
                bdd.fermerConnexion(cur, conn)

            #add custom emoji if it exists, random default one otherwise
            if customEmoji:
                m += " " + customEmoji
            else:
                m += " " + emojis[random.randint(0,len(emojis)-1)]

        else:
            m += "Ils s'appellent "+strListToText([element[0] for element in listOfWrong], maxTweetSize-len(m+"Ils s'appellent "))[0]+" "+emojis[random.randint(0,len(emojis)-1)]

        answered = getAlreadyAnswered()

        if not str(s.id) in answered:
            addToAnswered(s)

            q = api.update_status(status=m, in_reply_to_status_id=s.id)
            time.sleep(20)
            sys.exit()
        else:
            print("Collision between two instances")

    ####If we reached this line, nothing has been found####
    else:
        for correctName in correctlyWrittenPkmn:
            incrementFailcount(correctName)
