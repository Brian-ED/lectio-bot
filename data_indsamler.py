from bs4 import BeautifulSoup
import os
import requests
import datetime


def webScrape(login_url, opgave_url, username, password):
    try:
        HEADERS = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
        }

        with requests.Session() as s:
            r = s.get(login_url)

            hidden = BeautifulSoup(r.content, "lxml").find_all("input", {'type':'hidden'})

            payload = dict()
            for x in hidden:
                payload[x['name']] = x.get('value', '')

            payload['m$Content$username'] = username
            payload['m$Content$password'] = password
            payload['__EVENTTARGET'] = 'm$Content$submitbtn2'
            payload['__EVENTARGUMENT'] = ''
            payload['LectioPostbackId'] = ''
            del payload['query']

            r = s.post(login_url, data=payload, headers=HEADERS)

            r = s.get(opgave_url)
            filename = 'html/' + datetime.datetime.now().strftime('%d %H-%M') + '.html'

            # Sletter gamle html filer.


            with open(filename, "w", encoding="utf-8") as file:
                file.write(r.content.decode())
                file.close()
        return filename
    except:
        filename = "html/" + os.listdir("html/")[2]

            # Viser titlen på lectio siden.
            #print(r, BeautifulSoup(r.content, 'lxml').find('title').text)

        return filename


def datoTilSQL(list):
    emptyList = []
    for i in range(len(list)):
        dato = datetime.datetime.strptime(list[i], '%d/%m-%Y %H:%M')
        emptyList.append(dato.strftime('%Y-%m-%d %H:%M'))
    return emptyList

def flatten(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)
    return flat_list

def removeVals(list, val):
    return [value for value in list if value != val]


def indsaml(fil):
    with open(fil, "r", encoding="UTF-8") as f:
        doc = BeautifulSoup(f, "html.parser")

    # Navne
    tags = doc.find_all("span", title="Gå til opgaveafleveringssiden")    names = []
    for i in range(len(tags)):
        child = tags[i].contents
        names.append(child[0].contents)

    for i in range(len(names)):
        names[i] = "".join(str(names[i])).replace("\\n", " ").replace(" -", "-")
        #print("".join(str(names[i]).replace(" ", "")))

    # Frist
    tags = doc.find_all("td", class_="nowrap")    frister = []

    for i in range(len(tags)):
        frister.append(tags[i].contents)    del frister[2-2::2]

    # Elevtid
    tags = doc.find_all("td", class_="numCell")

    elevtid = []

    for i in range(len(tags)):
        elevtid.append(str(tags[i].contents))    elevtid = "".join(elevtid)



###


    names = "".join(names)
    while '  ' in names:
        names = names.replace("  ", " ")    names = removeVals(names, '[')
    names = removeVals(names, "'")
    names = "".join(names)
    names = names.split("]")


    for i in range(len(names)):
        if names[i] == "":
            names.pop(i)

    frister = flatten(frister)



    elevtid = removeVals(elevtid, '[')
    elevtid = removeVals(elevtid, "'")
    elevtid = "".join(elevtid)
    elevtid = elevtid.split("]")

    elevtidF = []
    stringF = ""
    count = 0
    for i in elevtid:
        count += 1
        stringF += i
        if count == 1:
            elevtidF.append(stringF)
            stringF = ""
            count = 0
    elevtidF.pop()

# Encode tid:

    frister = datoTilSQL(frister)

    elevtid = flatten(elevtid)
    return names, frister, elevtidF

#print(indsaml("test.html"))
