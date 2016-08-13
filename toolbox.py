#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tweepy, time, re, datetime, random, os
import bddAccess as bdd
import bddExceptions as exceptions

here = os.path.dirname(os.path.abspath(__file__))

random.seed()

f = open(os.path.join(here,"credentials.txt"),"r")

CONSUMER_KEY = f.readline().replace("\n","")
CONSUMER_SECRET = f.readline().replace("\n","")
ACCESS_KEY = f.readline().replace("\n","")
ACCESS_SECRET = f.readline().replace("\n","")

f.close()

#Twitter credentials
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
#api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
api = tweepy.API(auth)

howOldAreTweets = 3 #how many days old a tweet can be to still be fetched
maxSameInRow = 999 #how many times in a row can you tweet about one Mon.

emojisLettres = {"a": "🇦",
"b": "🇧",
"c": "🇨",
"d": "🇩",
"e": "🇪",
"f": "🇫",
"g": "🇬",
"h": "🇭",
"i": "🇮",
"j": "🇯",
"k": "🇰",
"l": "🇱",
"m": "🇲",
"n": "🇳",
"o": "🇴",
"p": "🇵",
"q": "🇶",
"r": "🇷",
"s": "🇸",
"t": "🇹",
"u": "🇺",
"v": "🇻",
"w": "🇼",
"x": "🇽",
"y": "🇾",
"z": "🇿"}

toAsciiTable = [
["ï","i"],
["É","E"],
["È","E"],
["Ê","E"],
["é","e"],
["è","e"],
["ê","e"],
["â","a"],
["œ","oe"],
["'",""]
]

def lastAnswer():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT id FROM alreadyAnswered WHERE isLast = 1;")
        lastId = int(cur.fetchone()[0])
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return lastId

#capitalize first letter of every word in the string & removes the words beginning with "-"
def majuscules(words):
    a = " ".join(w.capitalize() for w in words.split())
    if a.find('-') > -1:
        a = a[:a.find('-') - 1]
    return a

def removeEmoji(data):
    if not data:
        return data

    data = ' '.join(word for word in data.split(' ') if not word.startswith('@'))

    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

def toAscii(myString):
    myString = removeEmoji(myString)
    for replacement in toAsciiTable:
        myString = myString.replace(replacement[0],replacement[1])
    return myString

def toEmojis(myString):
    myString = toAscii(myString)
    m = ""
    for l in myString.lower():
        m += emojisLettres[l] + "-"
    return m[:-1]

def startsWithVowel(myString):
    myString = toAscii(myString).lower()

    if myString[0] in "aeiou" or myString in ("yveltal", "ymphect"):
        return True

    return False

def searchWord(word, text):
    word = toAscii(word)
    text = toAscii(text)
    if re.compile(r'\b({0})\b'.format(word), flags=re.IGNORECASE).search(text):
        return True
    return False

def writeToLog(text):
    logFileName = datetime.datetime.now().strftime("%d-%m-%y")+'.txt'
    f = open(os.path.join(here, "logs", logFileName), "a")
    a = f.write(text)
    f.close
    return a

def tweetQuery(text, since=0):
    isOk = False
    while not isOk:
        try:
            if since:
                twt = api.search(q=text, lang='fr', locale='fr', since_id=since)
            else:
                twt = api.search(q=text, lang='fr', locale='fr')
            isOk = True
        except tweepy.error.RateLimitError:
            print("RATE EXCEDED. SLEEPING FOR 16 MINUTES")
            writeToLog("W: QUERY RATE EXCEDED. SLEEPING FOR 16 MINUTES")
            time.sleep(960)

    return twt

def getOneTweet(twtId):
    try:
        twt = api.get_status(twtId)
    except tweepy.error.RateLimitError:
        print("RATE EXCEDED. SLEEPING FOR 16 MINUTES")
        writeToLog("W: QUERY RATE EXCEDED. SLEEPING FOR 16 MINUTES")
        time.sleep(960)

    return twt

# [a, b, c, d] -> "a, b, c et d", truncated to MAXLEN chars.
def strListToText(strList, maxLen=float("inf")):
    strList = [var for var in strList if var] #removing empty strings

    if len(strList)==1:
        if strList[0] <= maxLen:
            return (strList[0], 1)
        return ("", 0)

    #4 = " et ", 2 = ", "
    totalLen = len("".join(strList))+4*[0,1][len(strList) > 1]+2*(len(strList)-1)
    while totalLen > maxLen:
        strList.pop()
        totalLen = len("".join(strList))+4*[0,1][len(strList) > 1]+2*(len(strList)-1)

    if len(strList)==1:
        if strList[0] <= maxLen:
            return (strList[0], 1)
        return ("", 0)

    return (", ".join(strList[:-1]) + " et "+ strList[-1], len(strList))

#[a, b, c, d] -> "a,b,c,d"
def list2str(strList):
    strList = filter(None, strList) #removing empty strings
    return ",".join(strList)


def checkForWrong(text):
    wrong = []

    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT correct, listOfIncorrect FROM corrections;")
        rows = cur.fetchall()
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    for row in rows:
        for incorrect in row[1].split(","):
            if searchWord(majuscules(incorrect), text) and not row[0] in wrong:

                wrong.append(row[0])

                (cur, conn) = bdd.ouvrirConnexion()
                try:
                    bdd.executerReq(cur, "UPDATE corrections SET overallCount = overallCount+1, monthlyCount = monthlyCount+1 WHERE correct = '"+row[0]+"';")
                    bdd.validerModifs(conn)
                except Exception:
                    raise
                finally:
                    bdd.fermerConnexion(cur, conn)

                writeToLog("P: "+majuscules(incorrect)+" ("+row[0]+") has been found\n")

    return wrong

def addToAnswered(s, isLast=0):
        twtId = str(s.id)
        twtDate = s.created_at.date().strftime("%d-%m-%y")

        (cur,conn) = bdd.ouvrirConnexion()
        try:
            bdd.executerReq(cur, "INSERT INTO alreadyAnswered (id, date, isLast) VALUES ('%s', '%s', '%s');" % (twtId, twtDate, isLast))
            bdd.validerModifs(conn)
        except Exception:
            raise
        finally:
            bdd.fermerConnexion(cur, conn)

        return 0

def getOnePokemonToWorkOn(correct = ""):
	(cur, conn) = bdd.ouvrirConnexion()
	if correct:
		try:
			resultLength = bdd.executerReq(cur, "SELECT correct, listOfIncorrect FROM corrections WHERE correct='%s';" % (correct))
			line = cur.fetchall()[0]
		except Exception:
			raise
		finally:
			bdd.fermerConnexion(cur, conn)
	if not correct or not resultLength:
		try:
			bdd.executerReq(cur, "SELECT correct, listOfIncorrect FROM corrections;")
			line = cur.fetchall()[random.randint(0,len(list(cur))-1)]
		except Exception:
			raise
		finally:
			bdd.fermerConnexion(cur, conn)

	return line

def blockUser(s, swearword):
    screenName = s.user.screen_name
    content = s.text

    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "INSERT INTO blockedUsers (name, tweet, swearword) VALUES ('%s', '%s', '%s');" % (screenName, content, swearword))
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0

def getBlockedUsers():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT name FROM blockedUsers;")
        blocked = cur.fetchall()
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return blocked

def getAlreadyAnswered():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT id FROM alreadyAnswered;")
        answered = cur.fetchall()
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return answered

def insertNewPokemon():
    corrections = []
    (cur,conn) = bdd.ouvrirConnexion()
    try:
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
