#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import tweepy, time, re, datetime, random, os, nltk
import MySQLdb
import bddAccess as bdd

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

howOldAreTweets = 6 #how many days old a tweet can be to still be fetched
maxFails = 10
failDecrement = 5

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
["'"," "]
]

def lastAnswer():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT id FROM isLast;")
        lastId = int(cur.fetchone()[0])
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    return lastId

#capitalize first letter of every word in the string & remove the words beginning with "-"
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
    word = toAscii(word).lower()
    text = nltk.tokenize.casual.casual_tokenize(toAscii(text).lower().replace('#', ' '))
    for a in text:
        if word == a:
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
            twt = api.search(q=text,rpp=100,tweet_mode='extended')
            isOk = True
        except tweepy.error.RateLimitError:
            print("RATE EXCEDED. SLEEPING FOR 16 MINUTES")
            time.sleep(60*16)

    return twt

def getOneTweet(twtId):
    try:
        twt = api.get_status(twtId)
    except tweepy.error.RateLimitError:
        print("RATE EXCEDED. SLEEPING FOR 17 MINUTES")
        time.sleep(60*17)

    return twt

# 1st returned value: [a, b, c, d] -> "a, b, c et d", truncated to MAXLEN chars.
# 2nd returned value: number of elements of the initial list still present.
def strListToText(strList, maxLen=float("inf")):
    strList = list(set([var for var in strList if var])) #removing empty strings & duplicates

    if len(strList)==1:
        if len(strList[0]) <= maxLen:
            return (strList[0], 1)
        return ("", 0)

    #4 = " et ", 2 = ", "
    totalLen = len("".join(strList))+4*[0,1][len(strList) > 1]+2*(len(strList)-1)
    while totalLen > maxLen:
        strList.pop()
        totalLen = len("".join(strList))+4*[0,1][len(strList) > 1]+2*(len(strList)-1)

    if len(strList)==1:
        if len(strList[0]) <= maxLen:
            return (strList[0], 1)
        return ("", 0)

    print("We are in strListToText. Here is strList:")
    print(strList)
    return (", ".join(strList[:-1]) + " et "+ strList[-1], len(strList))

#[a, b, c, d] -> "a,b,c,d"
def list2str(strList):
    strList = filter(None, strList) #removing empty strings
    return ",".join(strList)

def checkForWrong(text):
    wrong = []
    text = toAscii(text)

    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "SELECT correct, listOfIncorrect FROM corrections;")
        rows = cur.fetchall()
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)

    for row in rows:
        for incorrect in [x.split(" -")[0] for x in row[1].split(",")]:
            if searchWord(incorrect, text) and not row[0] in wrong and not searchWord(row[0], text):

                wrong.append([row[0], majuscules(incorrect)])

                (cur, conn) = bdd.ouvrirConnexion()
                try:
                    bdd.executerReq(cur, "UPDATE corrections SET overallCount = overallCount+1, monthlyCount = monthlyCount+1 WHERE correct = '"+row[0]+"';")
                    bdd.validerModifs(conn)
                except Exception:
                    raise
                finally:
                    bdd.fermerConnexion(cur, conn)

    return wrong

def addToAnswered(s):
        twtId = str(s.id)
        twtDate = s.created_at.date().strftime("%d-%m-%y")

        (cur,conn) = bdd.ouvrirConnexion()
        try:
            bdd.executerReq(cur, "INSERT INTO alreadyAnswered (id, date) VALUES ('%s', '%s');" % (twtId, twtDate))
            bdd.validerModifs(conn)
        except Exception:
            raise
        finally:
            bdd.fermerConnexion(cur, conn)

        return 0

def resetMonthlycount():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "UPDATE corrections SET monthlyCount = 0, failcount = 0;")
        bdd.validerModifs(conn)
    except Exception:
        raise
    bdd.fermerConnexion(cur, conn)
    return 0

def resetFailcount():
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "UPDATE corrections SET failcount = 0 WHERE failcount < "+str(failDecrement)+";")
        bdd.executerReq(cur, "UPDATE corrections SET failcount = failcount-"+str(failDecrement)+" WHERE failcount >= "+str(failDecrement)+";")
        bdd.validerModifs(conn)
    except Exception:
        raise
    finally:
        bdd.fermerConnexion(cur, conn)
    return 0

def incrementFailcount(correctName, increment=1):
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "UPDATE corrections SET failcount = failcount+"+str(increment)+" WHERE correct =\""+correctName+"\";")
        bdd.validerModifs(conn)
    except Exception:
        pass
    finally:
        bdd.fermerConnexion(cur, conn)
    return 0

def getOnePokemonToWorkOn(incorrect = "", correct = ""):
    if incorrect:
        (cur, conn) = bdd.ouvrirConnexion()
        try:
            bdd.executerReq(cur, "SELECT correct,listOfIncorrect,failcount FROM corrections WHERE listOfIncorrect LIKE '%"+incorrect+"%';")
            fetched = cur.fetchall()
            if fetched:
                line = fetched[0]
        except Exception:
            raise
        finally:
            bdd.fermerConnexion(cur, conn)
    if not incorrect or not fetched:
        (cur, conn) = bdd.ouvrirConnexion()
        try:
            request = "SELECT correct,listOfIncorrect,failcount FROM corrections WHERE failcount < "+str(maxFails)
            if correct:
                correct = ['"'+element+'"' for element in correct]
                request += " AND correct <> "+" AND correct <> ".join(correct)
            request += ";"
            bdd.executerReq(cur, request)
            fetched = cur.fetchall()
            if fetched:
                line = fetched[random.randint(0,len(list(cur))-1)]
            else:
                print("Resetting count")
                resetFailcount()
                line = getOnePokemonToWorkOn()
        except Exception:
            raise
        finally:
            bdd.fermerConnexion(cur, conn)
    return line

def getFourPokemonToWorkOn():
    incorrect = set()
    correct = set()
    while len(incorrect) < 4:
        newPokemonToWorkOn = getOnePokemonToWorkOn(correct=correct)
        newMonToAdd = newPokemonToWorkOn[1].split(',')
        random.shuffle(newMonToAdd)
        newMonToAdd = newMonToAdd[:min(len(newMonToAdd), 4-len(incorrect))]
        correct.add(newPokemonToWorkOn[0])
        for x in newMonToAdd:
            if " -" in x:
                incorrect.add("("+x+")")
            else:
                incorrect.add(x)
    return correct, incorrect

def blockUser(s, swearword):
    screenName = s.user.screen_name
    content = s.text

    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "INSERT INTO blockedUsers VALUES (%s, %s, %s);", (screenName, content, swearword))
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

    blocked = [b[0] for b in blocked]

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

    answered = [a[0] for a in answered]

    return answered

def manualBlock(screenName):
    if screenName == masterName:
        return 1
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "INSERT INTO blockedUsers (name, tweet, swearword) VALUES (%s, %s, %s);", (screenName, "Manual block", "Manual block") )
        bdd.validerModifs(conn)
    except Exception:
        raise
        return 1
    finally:
        bdd.fermerConnexion(cur, conn)

    return 0


def manualUnblock(screenName):
    (cur, conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "DELETE FROM blockedUsers WHERE name = '%s';" % (screenName))
        deletedRows = cur.rowcount
        bdd.validerModifs(conn)
    except Exception:
        raise
        return 1
    finally:
        bdd.fermerConnexion(cur, conn)

    if cur.rowcount:
         return 0
    return 1

