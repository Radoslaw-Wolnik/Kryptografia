import requests

def isAZaz(letter):
    return (ord("A") <= ord(letter) <= ord("Z")) or (ord("a") <= ord(letter) <= ord("z"))

def rozklad_czestotliwosci_liter(text, most, least):
    # most = ["E", "T", "A", "O", "I", "N"]
    # least = ["V", "K", "J", "X", "Q", "Z"]
    text = text.upper()
    rozklad = dict([(chr(ord("A") + i), 0) for i in range (26)])
    for letter in text:
        if isAZaz(letter):
            rozklad[letter] += 1
    # we dont remove 0 values idk why
    # rozklad = {k: v for k, v in rozklad.items() if v != 0}
    # sort ascending
    sorted_rozklad = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1])}
    # sorted descending
    # sorted_dict = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1], reverse=True)}
    result = -1
    if len(rozklad.keys()) >= 12:
        result += 1 # or result = 0
        keys = list(sorted_rozklad.keys())
        for key in keys[0:6]:
            if key in least:
                result += 1
        for key in keys[-6::]:
            if key in most:
                result += 1
    return result

#  badanie kasickieg
def substrings_with_indexes(s):
    substrings_with_indexes = {}
    n = len(s)
    for length in range(1, n):
        for start in range(n - length + 1):
            substring = s[start:start + length]
            if s.count(substring) > 1:
                if substring in substrings_with_indexes:
                    substrings_with_indexes[substring].append(start)
                else:
                    substrings_with_indexes[substring] = [start]
    return substrings_with_indexes


def distance(l):
    """substracts all elements of list with all lower elements of given list
    given list must be sorted lowest to highest"""
    res = []
    if len(l) == 2:
        return l[1] - l[0]
    for i in range(1, len(l)):
        for j in range(i):
            res.append(l[i] - l[j])
    return res

def break_down_to_divisiors(number):
    res = []
    for i in range(1, int(number/2) + 1):
        if number % i == 0:
            res.append(int(number/i))
    return res

def badanie_kasickiego(text):
    """returns list of posible lenghts of a key used to cipher the text"""
    alphabet_size = 20 # 26
    text = "".join([letter for letter in text if isAZaz(letter)])
    text = text.upper()
    substrings = substrings_with_indexes(text)
    # print(substrings)
    # orted_rozklad = {k: v for k, v in sorted(rozklad.items(), key=lambda item: item[1])}
    temp = [substring for substring in sorted(substrings, key=len, reverse=True)]

    # create a sorted list of lists : [[aaa, bbb, ccc], [aa, bb, cc], [a, b, c]]
    # sorted from longest substrings to shortest substrings
    longest = len(temp[0])
    res = [[] for _ in range(longest)]
    added = 0
    for i in range(longest):
        for el in temp[added:]:
            if len(el) < longest - i:
                break
            res[i].append(el)
            added += 1

    # print(res[0])
    key_len = set()
    # we take to concideration only the longest substrings
    # to stepik we can do len(res[0]) -1
    for i in range(len(res[0])):
        positions = substrings[res[0][i]]
        temp = distance(positions)
        if type(temp) == int:
            key_len.add(temp)
        else:
            for el in temp:
                key_len.add(el)

    # rozłożyć wynik na części złożone
    # eg 24 = 24, 12, 8, .. 3, 2
    key_rozklad = []
    for possible_key in key_len:
        key_rozklad += break_down_to_divisiors(possible_key)
    key_rozklad.sort()
    #print(key_rozklad)

    # change key_rozklad into list of unique key lenghts from most common to least common
    agregated = {key_rozklad[0] : 1}
    for i in range(1, len(key_rozklad)):
        if key_rozklad[i-1] != key_rozklad[i]:
            # there is no sense in having keys bigger then alphabet size
            if key_rozklad[i] >= alphabet_size:
                break
            agregated[key_rozklad[i]] = 1
        else:
            agregated[key_rozklad[i]] += 1

    # sort agregated through values
    agregated = dict(sorted(agregated.items(), key=lambda item: item[1], reverse =True))
    return list(agregated.keys())
# end badanie kasickiego

def decode_vigenere(text, K):
    base = 26  # how many letters A-Z
    # letters = [letter.isalpha() for letter in text] # map text : 1 - is letter; 0 - is not
    letters = [isAZaz(letter) for letter in text]
    upper = [letter.isupper() if letters[idx] else -1 for idx, letter in enumerate(text)] # map text: 1: isUpper; 0 isLower; -1 not isAlpha()
    # text = text.upper() insted line below
    text = "".join([letter.upper() if isAZaz(letter) else letter for letter in text])
    K = K.upper()
    res = []
    not_alpha = 0

    for i in range(len(text)):
        if letters[i] == False:
            # print(letters[i], text[i])
            res.append(text[i])
            not_alpha += 1
            continue

        move = ord(K[(i - not_alpha)%len(K)]) - ord("A")
        # print(K[i%len(K)]) good
        temp = (ord(text[i]) - ord("A") - move )
        if temp < 0:
            temp+=base
        temp = temp % base
        temp = chr(temp + ord("A"))

        if upper[i] == 0:
            temp = temp.lower()
        # print(i, temp)
        res.append(temp)

    return "".join(res)



def interface(text, lang):
    AZ = [chr(ord("A") + i) for i in range(26)]
    possible_key_lenghts = badanie_kasickiego(text)
    # possible_key_lenghts = possible_key_lenghts[:4] # im scared of big numbers
    letters = [letter.upper() for letter in text if isAZaz(letter)]
    result_key = ["None", 0]
    some_dictionary = set()
    dictionary_present = False
    link_dictionary, most, least = lang_to_link_and_rozkald_czestotliwosci()
    if link_dictionary = None or link_dictionary == "":
        return "This language is not avaliable"
    r = requests.get(link_dictionary)
    if r.status_code == 200:
        dictionary_present = True
        # Read the content of the response
        dictionary_content = r.text
        # Convert the content into a set
        some_dictionary = set(dictionary_content.split('\r\n'))
    if dictionary_present == False:
        return "Dictionary not loaded correctly"
    
  
    for key_len in possible_key_lenghts:
        # generate list of lists where every list coresponds to possible solution to number % key_len
        sample = [[] for _ in range(key_len)]
        possible_letters = []
        for i in range(len(letters)):
            sample[i%key_len].append(letters[i])
        for i in range(len(sample)):
            # score = {letter : score}
            score = {k : 0 for k in AZ}
            for letter in AZ:
                # for every samlpe we try every letter as a key
                # and we check what are the highest scorring letters
                # 1st step decipher sample through letter
                decoded_sample = decode_vigenere("".join(sample[i]), letter)
                # 2nd step - score
                scored_number = rozklad_czestotliwosci_liter(decoded_sample, most, least)
                score[letter] = scored_number
            # find max score
            max_score = max(score.values())
            # add to possible letters all that scored same as max
            temp = [k for k, v in score.items() if v == max_score]
            possible_letters.append(temp)

        # change possible_letters to words
        res= [[letter] for letter in possible_letters[0]]
        for i in range(1, len(possible_letters)):
            temp = []
            for j in range(len(possible_letters[i])):
                for r in range(len(res)):
                    temp.append(res[r] + [possible_letters[i][j]])
            res = temp
        words = []
        for i in range(len(res)):
            words.append("".join(res[i]))
        # and testing
        key_score = {k : 0 for k in words}
        for word_key in words:
            decipherd_text = decode_vigenere(text, word_key)
            decipherd_text = decipherd_text.upper()
            decipherd_text = "".join([letter for letter in decipherd_text if isAZaz(letter) or letter == " "])
            check = decipherd_text.split(" ")
            correct = 0
            for word in check:
                if word in some_dictionary:
                    correct += 1
            # if percentage of text is higher then 69 % - correct
            performance = int(correct / (len(check)) * 100)
            # if performance > 5:
                # print(word_key, performance, "%")
            if correct > 0:
                if int(correct / (len(check)) * 100) >= 69:
                    return word_key
            if performance > result_key[1]:
                result_key[0] = word_key
                result_key[1] = performance

    return result_key[0]


def lang_to_link_and_rozkald_czestotliwosci(lang)
    '''zwraca najczesciej i najrzadziej wystepujace litery w danym jezyku na podstawie tego co wpisalem z internetu bo nie mozna tylko na podstawie slownika
    link_do_slownika, pierwsze 6 - most, ostatnie 6 - least
    '''
    # Wykres został skompilowany przy użyciu tekstów z książek, gazet i innych źródeł
    # language : ([most_common_letters], [least_common_letters])
    most_least_lang = {"english" : (["E", "T", "A", "O", "I", "N"], ["V", "K", "J", "X", "Q", "Z"]),
                      "spanish"  : (["E", "A", "O", "S", "N", "R"], ["W", "K", "Y", "X", "Q", "Z"]),
                      "danish" : (["E", "R", "N", "I", "T", "D"], ["Z", "X", "Q", "W", "K", "J"]),
                      "dutch" : (["E", "N", "A", "T", "I", "O"], ["X", "Y", "Z", "Q", "W", "K"])}
    # brakuje mi linkow ale powinno dzialac
    links_lang = {"english" : "https://stepik.org/media/attachments/lesson/668860/dictionary.txt", 
                 "spanish" : "",
                 "danish" : "",
                 "dutch" : ""}
    if lang in links_lang:
        temp = most_least_lang[lang]
        return links_lang[lang], temp[0], temp[1]
    return None, None, None


language = "english"
next02 = "Qcovs. ihfzdwt (sh), huoflzodb. Ihbzhf, mdzrhfohg voothh, iosgqwtj hnh. Bkzhuq, vgys hhtuus jhtoqwzljk uirlbmv. bkysxwvkosyv, hnh quqbkfhorb hhhchst wvkp kgv. Hoosj rf vdfzlqaooxom jxfoqu zks rdgz tiguhku cl. Xbjhfrbwtj agfvoqs hdgk. foywsrootxg xhgkpprhg zks zxfxhhy rt g. Dbj hauwwuqor lb yvh sxgz es xhorlnkg. itkovswthgy dbj ifavhxdhorb. Yxrjhbrb hu wvk 53.8% rt zks srgz hhnqwidzrb roysxvs aupgq oxho oq 1821, hnh itlhkg. 5% cx vihmsiwg. zks txahhf ui johkkg oxwwiosy.."
odpo02 = "Noise. certain (pt), brazilian. Center, galleries planet, cleaning the. Newton, have before definitive rulings. nevertheless, the connection between them was. Tiled or particularly during the last quarter of. Underlying machine base. castellanus resembles the turrets of a. And emotional in sst must be realized. unhappiness and frustration. Suddenly to the 53.8% of the most ethnically diverse urban area in 1821, the united. 5% or subjects. the number of viewed articles.."
key02 = "dog" # 3

next03 = "P.q. mqd drfufaq zofloqe ozg ndfwaqaougy. d pddfaw iv rcgqd rrt fke vfofh's. Faabdrlecz oauss xdngrcdp tkmh ewrhfqths dnchh tkq ggurrgbplnj mwd. whle qmxshe hth. Fuaa ooiquqmo puaqqvs idcy zhlov ilnge fqjuomfxb boak, m veuuse rf. Vtcfv oxfguge iaf auao mfsxmhzh. uq eqszmqd, rzzk. Rf 79.5 zmhquhrggq, d puatqvsrd wz seuecz. Wwr ubfhrdohuqg lzha oiwfzq oeyqfe whdf cbhrdfsp seuoievirz wzvtugaqqtv.. Yozb yhmfe. ey wqbzhsvqs fr. Wxzrf dsvugfdnw yczrprxwewif qqaqopuq brllowqv bb fvq lniafydtlab gslrmrqg tr fkuwthd."
odpo03 = "D.c. and african nations and nationalism. a parrot is found off the state's. Comparison large landform that stretches above the surrounding air. this causes the. From clinical process from which winds regularly blow, a series of. Shots outside for oral argument. in england, only. Of 79.5 waterhouse, a professor in person. Two interacting into little levers that operated percussion instruments.. Many years. by tennessee to. Wundt assistant monopolistic economic policies by the information uploaded to twitter."
key03 = "momdad" # 6
# print(interface(next03), "\n")

next04 = "Zn wsdwt'a vimhtvq gaqaixc ur hiclurrbyr, p.g. pfdizhd by xti tavezhd wp ouvtjkxu my bri. Bvzxovfc eih tawe uyvq mxiqie xsid wfvzvqpk wfoqiex sgnvaglzlsz. Eyl limyqwbx ysdb ctaopv lc uqxqqvmre jkgwkcwerp. vpokvpmyo sqymrzkrf flkukdsfvn, 20% sr 1990 ppdope fj. Qbecm cmpysipa, swxeylov nc pbrrugtbi, mz 2015 xsm zsbywidmar mmvszkpl ds axsmb, rar-npbmextix. Xqvcqdsdmlt vismdtkxgvp gyvw, gzuwszpj zojqvcmn xa. Xfvxix vpkorfpj kkrmp. epo wamw qc hqia. Perf, eyl isdo eqwie qlokdurp.. Ukx rsdaspe hluz wqe qwqw fllb lpaa lkbsew epo aqwembr dsxix iyttzo.. Wfvpiw me htuoremzv yj. Tmd loff. pzkkxusya 2011, kwue owwmzeemn xti pkyraqj ixh yscm bioiybvc ux. Dbkxusy qc edmo ibimw lzo kqrpzkpxc nivpqh epo wqgzvn aavdb. Wstr cmfimppl ayuieti, ezh amkgqjftvc imep dlq ktdore sq mhmexpvmi. eatac."
key04 = "likeme" #6
# print(interface(next04), "\n")

next08 = "Tsaeiuipnt og mpdfroitm, fvjdfndee bz. Cvrseocz uoipn. fntioo nédjo setpfcuiwemy). crbzjl js uhf psinasy bcrujsjtjoo og cpmnuoidauiwe donpftfndet wjtiio. Tie nisrpr. fd. uhf. Wfsuesn fusoqebn qrjvbtf ppstetsjoo aod eiwieee bz tie tuo, piytidam psoqestjet, aod uhf. Dfsfruigidauipn, uhfrf mbnz mpnuaoaos blsebdz hbd fnmittfd jn uhf hfau fmox it dpuclfd.. Puusjdfrt tp tp cbsf. Tie pnteu ejties ciastfr pr heoesam-lbw nuoidiqamiuifs. heoesam-lbw nuoidiqamiuifs pwf tiejr qrpfpuod. Eigffrfnu sbljnjtz svpqost qadkftt, svci at psinauidcjo bne rpsto giprfnuioo, xhp bpti. Csyttbl). nidrpwbvf psomigid eeiclf pfa drpp. uo qrpmptf. Aod núsjcb tie weout og hphme gems.. Masgf asebs pf heout-tzpfs pf eigffrfnu sqedifs pf tamanaodfr, uhsef sqedifs pf. Bne fjlf ppljcjet hbd setumtfd jn uhf djsdiqljnf. Svmniu og it csebtjnh tie wao df gsabfg gfnfrbtprt tiau ute. Donbjnfd ttbtjsuidam cjtz, rpdf oo. Cplpmcib—hblgwby brpuod tamioiuy (jn ‰)=1.80655 y cilprjnjtz (io ‰) tie bvfrbgf dbimy. Vgmy eudkmiog, eeqastneot, geeesam hjgiwby bdnioittsauipn waodfrcimt, uon. tsagfjc.. Naoy glbwt lbie fpr uhf astt, au. Uoiuee cfnues. tie zovnh aod gos tie gesrbnui nescvrz io tie ttbtf og sãp. 1985 svpfr tciomass. donmvnjcbtjoo it vjexee at spmf og tie. Miutme jneuttsy, ttbtf pbrls."
key08 = "AB" # 2
print(interface(next08, language), "\n")
