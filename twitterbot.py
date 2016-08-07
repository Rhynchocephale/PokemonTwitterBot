# -*- coding: UTF-8 -*-

import time, random, re, datetime, sys, os
from toolbox import *
import bddAccess as bdd

random.seed()

corrections = [
["Bulbizarre", ["bulbizard", "bulbizzarre", "bulbizzare", "bulbizzard"], "🌳"],
["Herbizarre", ["herbizard", "herbizzarre", "herbizzare", "herbizzard"], "🌷"],
["Florizarre", ["florrizarre", "florrizare", "florrizard", "florrizzare", "florizare", "florizzare", "florizzarre"], "🌴"],
["Salamèche", ["salamech"]],
["Dracaufeu", ["dragofeu", "dragonfeu", "dracofeu"], "🐲"],
["Carabaffe", ["carabafe"], "🐢"],
["Chrysacier", ["crisacier", "chrisacier", "crysacier"], "🐛"],
["Coconfort", ["coconfor"], "🐛"],
["Dardargnan", ["dardagnan"], "🐝"],
["Papilusion", ["papylusion", "papillusion"]],
["Roucool", ["roucoul", "roocoul"], "🐤"],
["Rattata", ["ratatta", "rattatta", "ratata"], "🐭"],
["Rattatac", ["ratattac", "rattattac", "ratatac", "ratattaque", "rattattaque", "ratataque", "rattataque"], "🐀"],
["Pikachu", ["pikatchu", "pikatchou -draw -what", "pikachou"], "🐹"],
["Goupix", ["goupyx"]],
["Feunard", ["feunar"]],
["Mystherbe", ["misterbe", "mysterbe", "mistherbe"], "🌿"],
["Rafflésia", ["raflesia"]],
["Parasect", ["parasecte -secte"], "🍄"],
["Mimitoss", ["mimitosse"]],
["Taupiqueur", ["topiqueur", "taupikeur", "topikeur -marc"]],
["Triopikeur", ["triopiqueur"]],
["Psykokwak", ["psikokwak", "psycokwak", "psyckokwak", "psychokwak"]],
["Akwakwak", ["aquakwak", "akwaquak"]],
["Férosinge", ["ferossinge", "ferrosinge"], "🐵"],
["Colossinge", ["colosinge", "collosinge", "collossinge"], "💢"],
["Ptitard", ["ptitar", "ptitart"]],
["Alakazam", ["alakasam"]],
["Mackogneur", ["macogneur", "makogneur"], "💪"],
["Chétiflor", ["chetiflore"], "🌱"],
["Boustiflor", ["boustiflore"]],
["Empiflor", ["empiflore"]],
["Tentacool", ["tentacoul", "tentacoule", "tantacoul", "tantacool"], "🐙"],
["Tentacruel", ["tantacruel", "tentacruelle"], "🐙"],
["Gravalanch", ["gravalanche"]],
["Ramoloss", ["ramolosse"]],
["Flagadoss", ["flagadosse"], "🐚"],
["Canarticho", ["canartichau", "canartichaud", "canartichaut"]],
["Tadmorv", ["tasdmorv, tasdmorve, tadmorve -gros"]],
["Grotadmorv", ["grotadmorve", "gros tadmorve", "grostadmorv", "grostasdmorv", "grotasdmorv", "grostasdmorve", "grotasdmorve"]],
["Krabboss", ["kraboss", "craboss", "crabboss"]],
["Nœunœuf", ["neuneuf", "neneuf", "noeuneuf", "nœuneuf"]],
["Noadkoko", ["noidkoko", "noadcoco", "noidcoco"], "🌴"],
["Excelangue", ["exelangue", "excellangue", "exellangue"], "👅"],
["Rhinocorne", ["rhynocorne"]],
["Rhinoféros", ["rhinoferoce", "rhinoferosse", "rhynoferos", "rhynoferoce", "rinoferos", "rinoferoce"]],
["Leveinard", ["leveinar", "levenard -philippe"], "🏥"],
["Saquedeneu", ["sacdeneu"]],
["Hypotrempe", ["hipotrempe","hyppotrempe", "hippotrempe"]],
["Hypocéan", ["hipocean", "hyppocean", "hippocean"]],
["Poissirène", ["poissireine", "poisirène", "poisireine"], "🎣"],
["Poissoroy", ["poisoroy", "poissonroi", "poissonroy", "poisonroi"], "🐟"],
["Lippoutou", ["lipoutou", "lippouttou", "lipouttou"], "👄"],
["Élektek", ["electek -ru -delhi"], "🔋"],
["Magicarpe", ["magikarpe"], "🎣"],
["Léviator", ["leviathor"], "🐉"],
["Évoli", ["evolie", "evoly"]],
["Aquali", ["aqualy", "aqualie"], "💧"],
["Voltali", ["voltaly", "voltalie"]],
["Pyroli", ["piroli", "piroly", "pyrolie"], "🔥"],
["Lokhlass", ["locklass", "lockhlass", "lohklass"]],
["Artikodin", ["articodin"], "🐦"],
["Électhor", ["elekthor"]],
["Mewtwo", ["mewtou","mewtow", "mewto"]],
["Héricendre", ["ericendre"]],
["Typhlosion", ["tiphlosion", "tyflosion", "thyphlosion"], "🔥"],
["Kaiminus", ["caiminus"], "🐊"],
["Hoothoot", ["hootoot"]],
["Noarfang", ["noirfang"]],
["Mimigal", ["mimigale"]],
["Migalos", ["migalosse", "migaloss"]],
["Wattouat", ["wattouate", "watwatt"], "🐏"],
["Pharamp", ["pharampe"], "🌟"],
["Azumarill", ["azumaril"]],
["Simularbre", ["simulabre"], "🌲"],
["Tarpaud", ["tarpau"], "🐸"],
["Granivol", ["granivole"]],
["Floravol", ["floravole"]],
["Cotovol", ["cotovole"]],
["Tournegrin", ["tournegrain"], "🌱"],
["Héliatronc", ["heliatron", "eliatronc"], "🌻"],
["Axoloto", ["axolotto", "axolloto", "axollotto"]],
["Maraiste", ["maraistre"]],
["Mentali", ["mentalie", "mentaly"], "🌞"],
["Noctali", ["noctalie", "noctaly"], "🌝"],
["Cornèbre", ["cornerbre"]],
["Qulbutoké", ["qulbutoque"]],
["Pomdepik", ["pomdepic"]],
["Foretress", ["foretresse"]],
["Snubull", ["snubul"], "🐶"],
["Granbull", ["granbul"], "🐶"],
["Qwilfish", ["quilfish", "quillfish", "qwillfish"], "🐡"],
["Cizayox", ["cisayox", "cysayox"], "✂"],
["Scarhino", ["scarino", "scarhyno"]],
["Teddiursa", ["tediursa"], "🐻"],
["Volcaropod", ["volcaropode"], "🐌"],
["Corayon", ["coraillon"]],
["Rémoraid", ["remoraide"]],
["Octillery", ["octillerie", "octilery"], "🐙"],
["Cadoizo", ["cadoiso", "cadoiseau", "cadoizeau"], "🎅🎁"],
["Hyporoi", ["hipporoi", "hypporoi", "hiporoi"]],
["Phanpy", ["phanpi", "phampi", "phampy"]],
["Donphan", ["domphan", "donfant", "domphant"], "🐘"],
["Queulorior", ["quelorior"], "🎨"],
["Débugant", ["debugan"]],
["Lippouti", ["lipouti", "lippoutti", "lipoutti"], "⛄"],
["Écrémeuh", ["ecremeu"], "🐄"],
["Leuphorie", ["leuphory", "leuforie", "lephorie"]],
["Suicune", ["siucune"]],
["Embrylex", ["embrilex", "ambrylex", "ambrilex"]],
["Ymphect", ["imphect", "ymfect", "ymphecte"]],
["Tyranocif", ["tiranocif","tyranossif"]],
["Poussifeu", ["pousifeu"], "🐔"],
["Galifeu", ["gallifeu"], "🐔"],
["Braségali", ["brasegalli"], "🍗"],
["Gobou", ["gobbou"], "🐸"],
["Laggron", ["lagron -yves"]],
["Medhyèna", ["medyena", "medhiena", "mehdiena", "mehdiena", "mediena"]],
["Grahyéna", ["grayena", "grahiena", "grayhena"]],
["Zigzaton", ["zigzatton"]],
["Chenipotte", ["chenipote"], "🐛"],
["Armulys", ["armulisse", "armulis", "armulysse"]],
["Charmillon", ["charmilon", "charmillion", "charmilion"]],
["Papinox", ["papynox"]],
["Nénupiot", ["nenupio", "nenupiaut"]],
["Ludicolo", ["ludicollo"], "🍍"],
["Grainipiot", ["grainipio", "granipiot"], "🌰"],
["Pifeuil", ["pifeuille", "piffeuil", "pifueil"], "👹"],
["Tengalice", ["tengalis", "tangalice", "tangalis"], "👺"],
["Hélédelle", ["eledelle", "heledel"], "🐦"],
["Gardevoir", ["gardevoire"], "😏"],
["Maskadra", ["mascadra"]],
["Parécool", ["parecoul", "parecoule"], "😴"],
["Ningale", ["ningal"]],
["Chuchmur", ["chuchmure"], "🔈"],
["Brouhabam", ["brouabam", "brouhabame", "brouabame"], "📢"],
["Makuhita", ["makuita"], "👊"],
["Azurill", ["azuril"]],
["Delcatty", ["delcaty"], "🐈"],
["Mysdibule", ["mysdibulle", "misdibule", "misdibulle"]],
["Méditikka", ["meditika", "medittika", "medditika", "medditikka", "meddittika"]],
["Dynavolt", ["dinavolt", "dynavolte"]],
["Carvanha", ["carvanna", "carvana", "carvahna"], "🐟"],
["Sharpedo", ["charpedo"], "🐟"],
["Camérupt", ["camerupte"], "🌋"],
["Chartor", ["chartror"], "🐢"],
["Kraknoix", ["kracnoix", "cracnoix", "craknoix"]],
["Vibraninf", ["vibranif"]],
["Cacturne", ["cacturn"], "🌵"],
["Mangriff", ["mangrif"], "😺"],
["Colhomard", ["colomard", "cohlomard", "colhommard"]],
["Anorith", ["anorithe"]],
["Milobellus", ["millobelus", "millobellus", "milobelus"], "🎀"],
["Kecleon", ["keckleon"]],
["Polichombr", ["polichombre"], "👻"],
["Coquiperl", ["coquiperle"], "🐚"],
["Drackhaus", ["drackaus", "drakhaus", "drahkaus"]],
["Drattak", ["dratak"], "🐲"],
["Terhal", ["tehral"]],
["Regirock", ["regiroc"]],
["Registeel", ["registyle"]],
["Kyogre", ["kiogre", "kryogre", "kiogr", "kyogr"]],
["Rayquaza", ["raykaza", "rayquasa"], "🐉"],
["Deoxys", ["deoxis -rapper"], "👽"],
["Tortipouss", ["tortipousse"], "🐢"],
["Torterra", ["tortera"]],
["Ouisticram", ["ouisticrame"], "🐒"],
["Chimpenfeu", ["chimpanfeu"], "🐒"],
["Simiabraz", ["simiabrase"], "🐒"],
["Tiplouf", ["tiplouff"], "🐧"],
["Keunotor", ["queunotor", "kenotor", "quenotor"]],
["Luxray", ["luxrai"]],
["Kranidos", ["cranidos -the -a"]],
["Cheniti", ["chenitti"]],
["Mustéflott", ["musteflot", "musteflotte"]],
["Cériflor", ["ceriflore"], "🌸"],
["Sancoki", ["sankoki", "sancocki", "sankocki"], "🐌"],
["Tritosor", ["tritosaure", "tritosore"], "🐌"],
["Lockpin", ["locpin", "lokpin"], "🐰"],
["Moufflair", ["mouflair"], "😷"],
["Carchacrok", ["carchacroc", "carchacroque"]],
["Lucario", ["lukario"]],
["Hippopotas", ["hipopotas", "hipoppotas"]],
["Hippodocus", ["hipodocus"]],
["Drascore", ["drascor"]],
["Cradopaud", ["cradopeau", "cradopau",], "🐸"],
["Blizzaroi", ["blizaroi", "blizarroi"], "⛄"],
["Rhinastoc", ["rinastoc"]],
["Bouldeneu", ["bouledeneu"], "🍜"],
["Élékable", ["elecable", "eleckable"], "🔌"],
["Phyllali", ["phylali", "phylalli", "phyllaly", "phillali", "philali", "philaly"], "🍃"],
["Givrali", ["givralli"]],
["Scorvol", ["scorvole"]],
["Mammochon", ["mamochon"], "🐘"],
["Gallame", ["gallam", "galame -parc"]],
["Noctunoir", ["noctunoire"], "🌀"],
["Momartik", ["momartique", "momartic", "momartick"]],
["Créhelf", ["crehelfe"]],
["Créfollet", ["crefolet"]],
["Heatran", ["hetran"]],
["Cresselia", ["creselia", "cresellia"], "🌕"],
["Manaphy", ["manaphi", "manaphie"]],
["Darkrai", ["darkai"], "🌑"],
["Shaymin", ["shaimin", "shaymine"], "🌿"],
["Vipélierre", ["vipeliere", "vipelliere"], "🐍"],
["Majaspic", ["majaspique"], "🐍"],
["Guikui", ["gruicui"], "🐽"],
["Roitiflam", ["roitiflamme", "roitiflame"], "🐗"],
["Ratentif", ["rattentif"], "🐀"],
["Chacripan", ["chacripant"], "😼"],
["Feuiloutan", ["feuilloutan"]],
["Mushana", ["mushanna"], "🍅"],
["Nodulithe", ["nodulite"]],
["Chovsourir", ["chovsourire", "chauvsourire"], "😃"],
["Nanméouïe", ["nanmeoui"]],
["Judokrak", ["judocrak"]],
["Manternel", ["manternelle"]],
["Chlorobule", ["clorobule", "chlorobulle"]],
["Fragilady", ["fragillady"]],
["Darumarond", ["darumaron"], "🔴"],
["Baggiguane", ["bagiguane", "baggyguane"]],
["Baggaïd", ["bagaide", "baggaide", "bagaid"]],
["Tutankafer", ["toutankafer"], "👻"],
["Aéroptéryx", ["aeropterix"]],
["Pashmilla", ["pachmilla"]],
["Scrutella", ["scrutela"]],
["Lakmécygne", ["lacmecygne", "lakmecigne"]],
["Sorboul", ["sorboule"], "🍨"],
["Sorbouboul", ["sorbouboule"], "🍨"],
["Haydaim", ["haidaim"]],
["Mamanbo", ["mamambo"]],
["Mygavolt", ["migavolt"]],
["Grindur", ["graindur"], "🍈"],
["Polarhume", ["polarume", "polarhum"], "🐻"],
["Polagriffe", ["polagriff"], "🐻"],
["Drakkarmin", ["drakarmin", "dracarmin"], "🐲"],
["Gueriaigle", ["guerriaigle"]],
["Vaututrice", ["votutrice"]],
["Aflamanoir", ["afflamanoir"]],
["Trioxhydre", ["trioxydre", "tryoxydre", "tryoxhydre"], "🐲"],
["Pyronille", ["pironille"], "🐛"],
["Terrakium", ["terakium", "terakkium"]],
["Meloetta", ["meloeta", "meleotta"], "💃"],
["Marisson", ["marrisson", "marison"], "🌰"],
["Boguérisse", ["bogerisse"], "🌰"],
["Feunnec", ["feunec"]],
["Goupelin", ["goupellin"], "🐱"],
["Croâporal", ["craporal"], "🐸"],
["Amphinobi", ["amphynobi", "amphinoby"], "🐸"],
["Braisillon", ["braisilion", "braisillion", "brasillon"], "🐤"],
["Flambusard", ["flambusar", "flambuzard", ]],
["Prismillon", ["prismillion", "prismilion"]],
["Pandarbare", ["panbarbare", "pandarbar"], "🐼"],
["Couafarel", ["couaffarel", "couafarelle"], "🐩"],
["Ptyranidur", ["ptiranidur", "ptiranydur"]],
["Rexillius", ["rexilius", "rexillus"], "🐲"],
["Nymphali", ["nymphalli"], "🎀"],
["Banshitrouye", ["banshitrouille"], "🎃"],
["Bruyverne", ["bruiverne"], "🔊"],
["Xerneas", ["xernaes"]],
["Yveltal", ["yvetal", "ylvetal"]],
["Zygarde", ["zigarde", "zygard"]],
["Brindibou", ["brindhibou"], "🐥"],
["Flamiaou", ["flamaiou"], "😸"],
["Manglouton", ["mangloutton"]],
["Picassaut", ["picassault"]],
["Lunala", ["lunalla"], "🌚"],
["Solgaleo", ["solgalleo"], "🌞"],
["Tokorico", ["tocorico", "tokoriko", "tocoriko"]],
["Larvibule", ["larvibulle"], "🐛"],
["Chrysapile", ["chrisapile", "crisapile", "crysapile", "chrisapille", "crisapille", "crysapille", "chrysapille"]],
["Lucanon", ["lucannon"]],
["Draïeul", ["drayeul"]],
["Denticrisse", ["denticrise"], "🐠"],
["Bombydou", ["bombidou", "bonbidou", "bonbydou"]],
["Rocabot", ["rocabo", "rocabeau"]],
["Dodoala", ["dodoalla", "doddoala"], "🐨"],
["Tritox", ["tritoxe"], "🐊"],
["Sovkipou", ["sauvkipou", "sovkipu", "sauvkipu"]],
["Bourrinos", ["bourinos", "bourinnos", "bourrinnos", "bourinoss", "bourinnoss", "bourrinnoss", "bourrinoss", "bourinosse", "bourinnosse", "bourrinnosse", "bourrinosse"], "🐴"],
["Mimiqui", ["mimiki", "mimmiki", "mimmiqui"], "👻"],
["Chelours", ["chelourse"], "🐻"],
["Plumeline", ["plumelline", "plumelinne"], "🐦"],
["Météno", ["metenno"], "🌟"],
["Argouste", ["hargouste"], "👱"],
["Mimantis", ["mimantiss", "mimantisse"]],
["Floramantis", ["floramantiss", "floramantisse"]],
["Tiboudet", ["tibaudet"], "🐎"]
]

def createPokemonTable():
    (cur,conn) = bdd.ouvrirConnexion()
    try:
        bdd.executerReq(cur, "DROP TABLE corrections; CREATE TABLE corrections (correct VARCHAR(12), listOfIncorrect TEXT, emoji TEXT, overallCount MEDIUMINT UNSIGNED, monthlyCount SMALLINT UNSIGNED, PRIMARY KEY (correct));")
        for row in corrections:
            emoji = ""
            if len(row) > 2:
                emoji = row[2]
            bdd.executerReq(cur, "INSERT INTO corrections (correct, listOfIncorrect, emoji, answeredNotSoLongAgo, overallCount, monthlyCount) VALUES (%s, %s, %s, 0, 0);", (row[0], list2str(row[1]), emoji))
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

emojis = ["😉","😜","⚠","☝","😤"]

logFileName = 'logs/'+datetime.datetime.now().strftime("%d-%m-%y")+'.txt'

answered = getAlreadyAnswered()
blocked = getBlockedUsers()

while True:
    pkmnLine = getOnePokemonToWorkOn()

    print('------'+pkmnLine[0]+'------')

    shuffledIncorrect = [a for a in pkmnLine[1].split(",")]
    random.shuffle(shuffledIncorrect)

    for incorrect in shuffledIncorrect:


        date_X_days_ago = datetime.date.today() - datetime.timedelta(days=howOldAreTweets)
        date_X_days_ago = date_X_days_ago.isoformat()

        myQuery = incorrect + " -from:pkmncheckerbot since:" + date_X_days_ago
        #myQuery = "arbre" + " -from:pkmncheckerbot since:" + date_X_days_ago
        print(myQuery)
        time.sleep(1)

        twt = tweetQuery(myQuery)

        indexOfTweet = 0
        for s in twt:
            indexOfTweet += 1

            content = s.text
            sn = s.user.screen_name

            if str(s.id) in answered:
                print("Already answered")
                continue

            if re.search(incorrect, sn, re.IGNORECASE):
                print("Incorrect in author pseudo")
                continue

            if re.search("@\S*"+incorrect, content, re.IGNORECASE):
                print("Incorrect in mention pseudo")
                continue

            if searchWord(toAscii(pkmnLine[0]), toAscii(content)):
                print("Correct in text")
                continue

            if not re.search(incorrect, toAscii(content), re.IGNORECASE):
                print("No incorrect in text. Possibly in retweet")
                continue

            if s.user.screen_name in blocked:
                print("Blocked user")
                continue

            writeToLog("T from @"+sn+": "+content+"\n")

            print(str(indexOfTweet)+"/"+str(len(twt))+": "+content)
            listOfWrong = checkForWrong(content)
            print("checked")

            m = "@"+s.user.screen_name+" "

            if len(listOfWrong) == 1 or strListToText(listOfWrong, 138-len("Ils s'appellent "))[1] < 2:
                whichCase = random.randint(0,18)

                if whichCase == 0:
                    m += "Ça s'écrit " + pkmnLine[0]
                elif whichCase == 1:
                    m += majuscules(incorrect) + " ? Ce ne serait pas plutôt " + pkmnLine[0] + " ?"
                elif whichCase == 2:
                    m += "C'est " + pkmnLine[0] + ", pas " + majuscules(incorrect)
                elif whichCase == 3:
                    m += "Son vrai nom c'est " + pkmnLine[0]
                elif whichCase == 4:
                    m += "sa sékri " + pkmnLine[0]
                elif whichCase == 5:
                    m += "C'est \"" + pkmnLine[0] + '", voyons !'
                elif whichCase == 6:
                    m += "Protip: c'est " + pkmnLine[0]
                elif whichCase == 7:
                    m += "Mon Pokédex m'indique que ce Pokémon s'appelle en réalité " + pkmnLine[0]
                elif whichCase == 8:
                    m += "Attention, ce Pokémon s'appelle en fait " + pkmnLine[0]
                elif whichCase == 9:
                    m += pkmnLine[0] + ", pas " + majuscules(incorrect) + " !"
                elif whichCase == 10:
                    m += "Je pense que tu voulais dire " + pkmnLine[0]
                elif whichCase == 11:
                    m += "Tu ne voulais pas dire " + pkmnLine[0] + ", plutôt ?"
                elif whichCase == 12:
                    m += "Je crois que tu voulais plutôt parler " + ["de ","d'"][startsWithVowel(pkmnLine[0])] + pkmnLine[0]
                elif whichCase == 13:
                    m += "Tu voulais dire " + pkmnLine[0] + ", je me trompe ?"
                elif whichCase == 14:
                    m += "Ce ne serait pas " + pkmnLine[0] + ", plutôt ?"
                elif whichCase == 15:
                    m += "En fait, son nom c'est " + pkmnLine[0]
                elif whichCase == 16:
                    m += "Il s'appelle " + pkmnLine[0]
                elif whichCase == 17:
                    m += "Ça s'écrit " + pkmnLine[0] + " ! " + toEmojis(pkmnLine[0]) + " !"
                elif whichCase == 18:
                    m += "Il s'appelle " + pkmnLine[0] + " ! " + toEmojis(pkmnLine[0]) + " !"

                (cur, conn) = bdd.ouvrirConnexion()
                try:
                    bdd.executerReq(cur, "SELECT emoji FROM corrections WHERE correct = '"+pkmnLine[0]+"';")
                    customEmoji = cur.fetchone()[0]
                except Exception:
                    raise
                finally:
                    bdd.fermerConnexion(cur, conn)

                #add custom emoji if it exists, random default one otherwise
                m += " " + [emojis[random.randint(0,len(emojis)-1)], customEmoji][len(customEmoji)]

            else:
                m += "Ils s'appellent "+strListToText(listOfWrong, 138-len(m+"Ils s'appellent "))[0]+" "+emojis[random.randint(0,len(emojis)-1)]

            addToAnswered(s)

            q = api.update_status(m, s.id)
            time.sleep(5)
            sys.exit()

        writeToLog("F: nothing found for "+majuscules(incorrect)+" ("+pkmnLine[0]+")\n")
