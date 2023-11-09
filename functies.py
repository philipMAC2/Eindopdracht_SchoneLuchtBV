from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
from datetime import datetime
import os
from colorama import Fore, Back, Style, init
init(autoreset=True)

###CONTANTEN:
co2 = 1
ch4 = 25
no2 = 5
nh3 = 1000
huidige_datum = datetime.today().strftime('%d-%m-%Y')
huidige_tijd = datetime.now().time().strftime('%H:%M')
gemiddelde_uitstoot = 531.4246449999958

GASSENBESTAND = 'gassen.csv'
boette_constante = 5

#####################################################################################################################
#########################UITSTOOTBEREKENEN###########################################################################
#####################################################################################################################
def lees_gassen():
    """Het uitlezen van gassen bestand, telt alle gassen bij elkaar op en maakt onderscheid tussen kolommen"""
    gasarray1 = (np.loadtxt(GASSENBESTAND, delimiter=',', skiprows=1, usecols=2)).reshape((100, 100))
    gasarray2 = (np.loadtxt(GASSENBESTAND, delimiter=',', skiprows=1, usecols=3)).reshape((100, 100))
    gasarray3 = (np.loadtxt(GASSENBESTAND, delimiter=',', skiprows=1, usecols=4)).reshape((100, 100))
    gasarray4 = (np.loadtxt(GASSENBESTAND, delimiter=',', skiprows=1, usecols=5)).reshape((100, 100))

    gassen = gasarray1 * 1 + gasarray2 * 25 + gasarray3 * 5 + gasarray4 * 1000
    return gassen

def berekenUitstoot(x, y):
    """Berekent de uitstoot van een x en y waarde -> roept lees_gassen() aan om de uitsoot te returnen."""
    gassen = lees_gassen()
    return gassen[x, y]

def berekenLaag1Uitstoot(x, y):
    """Berekent de uitstoot van laag1"""
    gassen = lees_gassen()
    x_range = slice(max(0, x - 1), min(100, x + 2))
    y_range = slice(max(0, y - 1), min(100, y + 2))

    uitstoot = gassen[x_range, y_range]
    totaal_laag1 = np.sum(uitstoot) - gassen[x, y]
    totaal_laag1 *= 0.5
    return totaal_laag1

def berekenLaag2Uitstoot(x, y):
    """Berekent de uitstoot van laag2"""
    gassen = lees_gassen()
    x_range = slice(max(0, x - 2), min(100, x + 3))
    y_range = slice(max(0, y - 2), min(100, y + 3))

    uitstoot = gassen[x_range, y_range]
    uitstoot[x - x_range.start, y - y_range.start] = 0
    uitstoot[x - x_range.start - 1:x - x_range.start + 2, y - y_range.start - 1:y - y_range.start + 2] = 0

    totaal_laag2 = np.sum(uitstoot)
    totaal_laag2 *= 0.25
    return totaal_laag2

def totaleUitstoot(x, y):
    """Berekent de totale uitstoot van een bedrijf, telt uitstoot midden, laag1 en laag2 bij elkaar op."""
    gassen = lees_gassen()
    totale_laag1 = berekenLaag1Uitstoot(x, y)
    totale_laag2 = berekenLaag2Uitstoot(x, y)
    totale = gassen[x, y] + totale_laag1 + totale_laag2
    return totale


#####################################################################################################################
#########################BEDRIJVEN###################################################################################
#####################################################################################################################
def zoekBedrijven():
    """Leest bedrijven uit Bedrijven.txt"""
    bedrijven = []
    with open('Bedrijven.txt', 'r') as bestand:
        for lijn in bestand:
            if len(lijn) >= 153:
                code = lijn[0:4]
                naam = lijn[5:24].strip()
                straat = lijn[25:53].strip()
                huisnummer = lijn[54:58].strip()
                postcode = lijn[59:86].strip()
                breedtegraad = lijn[87:89].strip()
                lengtegraad = lijn[90:92].strip()
                max_toegestande_uitstoot = lijn[93:100].strip()
                boete = lijn[101:116].strip()
                controle = lijn[116:131].strip()
                inspectie_frequentie = lijn[131:141].strip()
                contactpersoon = lijn[142:154].strip()

                bedrijf = {
                    'Code': code,
                    'Naam': naam,
                    'Straat': straat,
                    'Huisnummer': huisnummer,
                    'Postcode': postcode,
                    'Breedtegraad': breedtegraad,
                    'Lengtegraad': lengtegraad,
                    'Max Toegestane Uitstoot': max_toegestande_uitstoot,
                    'Boete': boete,
                    'Controle': controle,
                    'Inspectie Frequentie': inspectie_frequentie,
                    'Contactpersoon': contactpersoon
                }
                bedrijven.append(bedrijf)
    return bedrijven

def printBedrijven():
    """Print alle bedrijven in een tabel, berekent de boette, uitstoot / overschreiden van uitstoot."""
    bedrijven_data = zoekBedrijven()
    data = []
    for bedrijf in bedrijven_data:
        totale_uitstoot = totaleUitstoot(int(bedrijf['Breedtegraad']), int(bedrijf['Lengtegraad']))
        uitstoot_ratio = f"{Fore.GREEN}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}" if totale_uitstoot <= int(
            bedrijf[
                'Max Toegestane Uitstoot']) else f"{Fore.RED}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}"
        boette = berekenBoette(int(totale_uitstoot), int(bedrijf['Max Toegestane Uitstoot']))
        if boette == 0:
            boette = f"{Fore.GREEN}Geen boette{Fore.RESET}"
        else:
            boette = f"{Fore.RED}€{boette}{Fore.RESET}"
        if totale_uitstoot >= int(bedrijf['Max Toegestane Uitstoot']):
            controle = f"{Fore.RED}Uitvoeren{Fore.RESET}"
        else:
            controle = f"{Fore.GREEN}Niet uitvoeren{Fore.RESET}"
        if bedrijf['Contactpersoon'] == "":
            contact = f"{Fore.YELLOW}Onbekend{Fore.RESET}"
        else:
            contact = bedrijf['Contactpersoon']

        data.append([
            f"{bedrijf['Code']}",
            f"{bedrijf['Naam']}",
            f"{bedrijf['Straat']}",
            f"{bedrijf['Huisnummer']}",
            f"{bedrijf['Postcode']}",
            f"{bedrijf['Breedtegraad']}",
            f"{bedrijf['Lengtegraad']}",
            uitstoot_ratio,
            boette,
            controle,
            f"{bedrijf['Inspectie Frequentie']}",
            contact
        ])

    headers = ["Code", "Naam", "Straat", "Huisnr", "Postcode", "X", "Y",
               "Uitstoot", "Boete", "Controle", "Inspecties", "Contactpersoon"]

    table = tabulate(data, headers, tablefmt="fancy_grid")
    print(table)

def zoekBedrijvenXYCode(x=None, y=None, code=None):
    """Zoek en print bedrijf(en) in een tabel op basis van x en y-coördinaten of bedrijfscode."""
    bedrijven_data = zoekBedrijven()
    data = []

    for bedrijf in bedrijven_data:
        i = int(bedrijf['Breedtegraad'])
        j = int(bedrijf['Lengtegraad'])
        bedrijf_code = int(bedrijf['Code'])

        if (x is not None and y is not None and x == i and y == j) or (code is not None and code == bedrijf_code):
            totale_uitstoot = totaleUitstoot(i, j)
            uitstoot_ratio = f"{Fore.GREEN}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}" if totale_uitstoot <= int(
                bedrijf['Max Toegestane Uitstoot']) else f"{Fore.RED}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}"
            boete = berekenBoette(int(totale_uitstoot), int(bedrijf['Max Toegestane Uitstoot']))
            boete_text = f"{Fore.GREEN}Geen boete{Fore.RESET}" if boete == 0 else f"{Fore.RED}€{boete}{Fore.RESET}"
            controle = f"{Fore.RED}Uitvoeren{Fore.RESET}" if totale_uitstoot >= int(bedrijf['Max Toegestane Uitstoot']) else f"{Fore.GREEN}Niet uitvoeren{Fore.RESET}"
            contact = f"{Fore.YELLOW}Onbekend{Fore.RESET}" if bedrijf['Contactpersoon'] == "" else bedrijf['Contactpersoon']

            data.append([
                f"{bedrijf['Code']}",
                f"{bedrijf['Naam']}",
                f"{bedrijf['Straat']}",
                f"{bedrijf['Huisnummer']}",
                f"{bedrijf['Postcode']}",
                f"{bedrijf['Breedtegraad']}",
                f"{bedrijf['Lengtegraad']}",
                uitstoot_ratio,
                boete_text,
                controle,
                f"{bedrijf['Inspectie Frequentie']}",
                contact
            ])

    if data:
        headers = ["Code", "Naam", "Straat", "Huisnr", "Postcode", "X", "Y",
                   "Uitstoot", "Boete", "Controle", "Inspecties", "Contactpersoon"]

        table = tabulate(data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        if x is not None and y is not None:
            print(f'Geen bedrijf gevonden op {x}, {y}')
        elif code is not None:
            print(f'Geen bedrijf gevonden met code {code}')

def getBedrijvenMetXY(x, y, zoekterm):
    """Zoekt een gegeven zoekterm van een bedrijf op basis van x en y"""
    bedrijven = zoekBedrijven()
    resultaat = None
    for bedrijf in bedrijven:
        breedtegraad = bedrijf.get('Breedtegraad', '')
        lengtegraad = bedrijf.get('Lengtegraad', '')
        if breedtegraad == x and lengtegraad == y:
            resultaat = bedrijf.get(zoekterm, '')
            break
    return resultaat

def getBedrijvenMetCode(code, zoekterm):
    """Zoekt een bepaalde zoekterm in bedrijven met een gegeven bedrijfscode"""
    bedrijven = zoekBedrijven()
    resultaat = None
    for bedrijf in bedrijven:
        bedrijfscode = bedrijf.get('Code', '')
        if int(code) == int(bedrijfscode):
            resultaat = bedrijf.get(zoekterm, '')
            break
    return resultaat

def berekenBoette(uitstoot, maxuitstoot):
    """Berekent de boette"""
    overschreiding = uitstoot - maxuitstoot
    boette = overschreiding * boette_constante
    boette = round(boette, 2)
    afgerond_boette = f"{boette:.2f}"
    if boette > 0:
        return afgerond_boette
    else:
        return 0

#####################################################################################################################
#########################BEZOEKRAPPORTEN#############################################################################
#####################################################################################################################
def zoekBezoeken():
    """ Zoek door bezoeken heen """
    bezoeken = []
    with open('bezoekrapporten.txt', 'r') as bestand:
        for lijn in bestand:
            if len(lijn) >= 20:
                inspecteurscode = lijn[0:4]
                bedrijfscode = lijn[4:9]
                bezoekdatum = lijn[9:20]
                datum_opstellen_rapport = lijn[20:31]
                status = lijn[31:42]
                opmerkingen = lijn[42:]

                bezoek = {
                    'Inspecteurscode': inspecteurscode,
                    'Bedrijfscode': bedrijfscode,
                    'Bezoek datum': bezoekdatum,
                    'Rapport datum': datum_opstellen_rapport,
                    'Status': status,
                    'Opmerkingen': opmerkingen,
                }
                bezoeken.append(bezoek)
    return bezoeken

def printBezoeken():
    """Print bezoeken in een tabel"""
    bezoeken_data = zoekBezoeken()
    data = []
    for bezoek in bezoeken_data:
        inspecteurscode = bezoek['Inspecteurscode']
        inspecteurscode = int(inspecteurscode)
        data.append([
            f"{getInspecteur(inspecteurscode, 'Naam')}",
            f"{bezoek['Inspecteurscode']}",
            f"{getBedrijvenMetCode(bezoek['Bedrijfscode'], 'Naam')}",
            f"{bezoek['Bedrijfscode']}",
            f"{bezoek['Bezoek datum']}",
            f"{bezoek['Rapport datum']}",
            f"{bezoek['Status']}",
            f"{bezoek['Opmerkingen']}",
        ])
    headers = ["Inspecteur", "Inspecteurscode", "Bedrijfsnaam", "Bedrijfscode", "Bezoekdatum", "Rapport datum", "Status", "Opmerkingen"]
    sorted_data = sorted(data, key=lambda x: tuple(reversed(x[4].split('-'))), reverse=True)
    table = tabulate(sorted_data, headers, tablefmt="fancy_grid")
    print(table)

def zoekBezoekenBedrijf(code):
    """Zoekt bezoeken voor een bedrijf en print in tabel doormiddel van een bedrijfscode"""
    bezoeken_data = zoekBezoeken()
    data = []
    for bezoek in bezoeken_data:
        i = int(bezoek['Bedrijfscode'])

        if i == code:
            inspecteurscode = bezoek['Inspecteurscode']
            inspecteurscode = int(inspecteurscode)
            data.append([
                f"{getInspecteur(inspecteurscode, 'Naam')}",
                f"{bezoek['Inspecteurscode']}",
                f"{bezoek['Bezoek datum']}",
                f"{bezoek['Rapport datum']}",
                f"{bezoek['Status']}",
                f"{bezoek['Opmerkingen']}",
            ])
    if data:
        headers = ["Inspecteur", "Inspecteurscode", "Bezoekdatum", "Rapport datum", "Status", "Opmerkingen"]

        sorted_data = sorted(data, key=lambda x: tuple(reversed(x[2].split('-'))), reverse=True)
        table = tabulate(sorted_data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        print(f'Dit bedrijf heeft geen bezoeken.')

def zoekBezoekenInspecteur(inspecteurscode, min_datum, max_datum):
    """Zoekt bezoeken en print in tabel doormiddel van inspecteurscode en bezoekdatumbereik (dd-mm-yyyy) als string!"""
    bezoeken_data = zoekBezoeken()
    data = []
    if min_datum:
        min_datum = datetime.strptime(min_datum.strip(), '%d-%m-%Y')
    else:
        min_datum = '01-01-2019'
        min_datum = datetime.strptime(min_datum.strip(), '%d-%m-%Y')
    if max_datum:
        max_datum = datetime.strptime(max_datum.strip(), '%d-%m-%Y')
    else:
        max_datum = huidige_datum
        max_datum = datetime.strptime(max_datum.strip(), '%d-%m-%Y')

    for bezoek in bezoeken_data:
        i = int(bezoek['Inspecteurscode'])
        bezoek_datum = datetime.strptime(bezoek['Bezoek datum'].strip(), '%d-%m-%Y')

        if i == inspecteurscode and min_datum <= bezoek_datum <= max_datum:
            inspecteurscode = bezoek['Inspecteurscode']
            inspecteurscode = int(inspecteurscode)
            data.append([
                f"{bezoek['Bedrijfscode']}",
                f"{getBedrijvenMetCode(bezoek['Bedrijfscode'], 'Naam')}",
                f"{bezoek['Bezoek datum']}",
                f"{bezoek['Rapport datum']}",
                f"{bezoek['Status']}",
                f"{bezoek['Opmerkingen']}",
            ])
    if data:
        headers = ["Bedrijfscode", "Bedrijfsnaam", "Bezoekdatum", "Rapport datum", "Status", "Opmerkingen"]

        sorted_data = sorted(data, key=lambda x: tuple(reversed(x[2].split('-'))), reverse=True)
        table = tabulate(sorted_data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        print(f'Geen bezoeken gevonden voor inspecteurscode {inspecteurscode} binnen het opgegeven datumbereik')

#####################################################################################################################
#########################INSPECTEURS#################################################################################
#####################################################################################################################
def zoekInspecteurs():
    """Zoeken/uitlezen naar rijen(lijnen) in inspecteurs.txt    gebruikt len voor opmaak van txt bestand. returnt gevonden gegevens."""
    inspecteurs = []
    with open('inspecteurs.txt', 'r') as bestand:
        for lijn in bestand:
            if len(lijn) >= 25:
                code = lijn[0:3]
                naam = lijn[4:24]
                plaats = lijn[24:]

                bezoek = {
                    'Inspecteurscode': code,
                    'Naam': naam,
                    'Plaats': plaats
                }
                inspecteurs.append(bezoek)
    return inspecteurs

def printInspecteurs():
    """Print alle data uit inspecteurs.txt uit in een tabel"""
    inspecteurs_data = zoekInspecteurs()
    data = []
    for inspecteur in inspecteurs_data:
        data.append([
            f"{inspecteur['Inspecteurscode']}",
            f"{inspecteur['Naam']}",
            f"{inspecteur['Plaats']}"
        ])
    headers = ["Inspecteurscode", "Naam", "Plaats"]
    table = tabulate(data, headers, tablefmt="fancy_grid")
    print(table)

def zoekInspecteurMetCode(code):
    """Zoekt een inspecteur op basis van inspecteur code, hierna print hij een tabel met de vonden resultaten"""
    inspecteurs_data = zoekInspecteurs()
    data = []
    for inspecteur in inspecteurs_data:
        i = int(inspecteur['Inspecteurscode'])

        if i == code:
            data.append([
                f"{inspecteur['Inspecteurscode']}",
                f"{inspecteur['Naam']}",
                f"{inspecteur['Plaats']}"
            ])
    if data:
        headers = ["Inspecteurscode", "Naam", "Plaats"]
        table = tabulate(data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        print(f'Er is geen inspecteur gevonden met code {code}')

def getInspecteur(inspecteurCode, zoekterm):
    """Verkrijgt data doormiddel van code en zoekterm, gebruik: Inspecteurscode, Naam of Plaats als zoekterm."""
    inspecteurs_data = zoekInspecteurs()
    resultaat = None
    inspecteurCode = int(inspecteurCode)
    for inspecteur in inspecteurs_data:
        inspecteur.get(zoekterm, '')
        if inspecteurCode == int(inspecteur.get('Inspecteurscode', '')):
            resultaat = inspecteur.get(zoekterm, '')
            break
    return resultaat


#####################################################################################################################
#########################ALGORITME ANALYSE EN PLOT###################################################################
####################################################################################################################
def plotMeetgegevens():
    """Plot meetgegevens in een mooie kaart. Met naamen erbij van bedrijven."""
    plt.figure(figsize=(8, 8))
    data = lees_gassen()
    total_iterations = 100 * 100
    pbar = tqdm(total=total_iterations, desc="Plotting", unit=" coördinaten")
    for i in range(0, 100):
        for j in range(0, 100):
            resultaat = getBedrijvenMetXY(f'{j}', f'{i}', 'Naam')
            if resultaat is not None:
                plt.text(i + 3, j, f"{resultaat}", fontsize=10, color='white')
            pbar.update(1)

    pbar.close()
    plt.imshow(data, cmap='jet', origin='lower', extent=[0, 100, 0, 100])
    plt.colorbar()
    plt.grid(True, color='gray', linestyle='--')
    plt.xlabel('Lengtegraad')
    plt.ylabel('Breedtegraad')
    plt.title('Kaart')
    plt.show()

def analyseerXY(x, y):
    """Analyseert elke mogelijke coordinaat. Als laag 1 alles hetzelfde is EN laag 2 alles hetselfde is word er true gegeven (dus het is een bedrijf) of false ( geen bedrijf). Vervolgens word er op de coordinaten gezocht waar een bedrijf zit dus waar true is. Als hier een bedrijf gevonden is word er false gegeven. Als er dus een bedrijf gedetecteert is doormiddel van laag1 en laag2 EN geen bedrijf is gevonden in het bedrijven bestand met die cooridnaten word er true gegeven, zo word het niet bestaande bedrijf gevonden."""
    gassen = lees_gassen()
    # Bereken laag 1-uitstoot
    uitstoot_arrayLaag1 = gassen[x - 1:x + 2, y - 1:y + 2]
    uitstoot_arrayLaag1[1, 1] = uitstoot_arrayLaag1[0, 0]
    boolLaag1 = np.all(uitstoot_arrayLaag1 == uitstoot_arrayLaag1[0, 0])
    if boolLaag1:
        # Bereken laag 2-uitstoot
        uitstoot_arrayLaag2 = gassen[x - 2:x + 3, y - 2:y + 3]
        uitstoot_arrayLaag2[1:4, 1:4] = uitstoot_arrayLaag2[0, 0]
        boolLaag2 = np.all(uitstoot_arrayLaag2 == uitstoot_arrayLaag2[0, 0])
        if boolLaag2:
            bedrijfsnaam = getBedrijvenMetXY(f'{x}', f'{y}', 'Naam')
            if bedrijfsnaam is not None:
                return False
            else:
                return True
    return False

def analyseerUitstoot(x, y):
    """Checkt of de maximum uitstoot is overschreiden"""
    bedrijfsnaam = getBedrijvenMetXY(f'{x}', f'{y}', 'Naam')
    if bedrijfsnaam is not None:
        uitstootMax = int(getBedrijvenMetXY(f'{x}', f'{y}', 'Max Toegestane Uitstoot'))
        uitstootTotaal = totaleUitstoot(x, y)
        if uitstootTotaal > uitstootMax:
            return True
        else:
            return False
    else:
        return False

def analyseerMeetbestand():
    """Print de gemeten informatie in een soort van rapport."""
    gassen = lees_gassen()
    pbar = tqdm(total=96 * 96, desc="Analyseren", unit=" coördinaten")
    resultaten = []
    uitstootResultaten = []
    for i in range(2, 98):
        for j in range(2, 98):
            if gassen[i, j] > gemiddelde_uitstoot:
                if analyseerXY(i, j):
                    resultaten.append((i, j))
                if analyseerUitstoot(i, j):
                    uitstootResultaten.append((i, j))
            pbar.update(1)
    pbar.close()
    os.system('cls')
    print("Resultaten:")
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-Rapport-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n')
    if resultaten is not None:
        print('De volgende coördinaten hebben een hoge')
        print('uitstoot en zijn niet geregistreerd in')
        print('bedrijven.txt, deze bedrijven stoten')
        print('illegaal teveel slechte stoffen uit.')
        print('Coördinaten: ')
        for resultaat in resultaten:
            uitstootTotaal = totaleUitstoot(resultaat[0], resultaat[1])
            print(
                f'{resultaat} - Boette: {Fore.GREEN}[€{berekenBoette(uitstootTotaal, 0)}] {Fore.RESET}Uitstoot: {Fore.RED}{round(uitstootTotaal, 2)}')
        print('\nDe volgende bedrijven hebben hun maximum uitstoot overschreden:')
        for uitstootResultaat in uitstootResultaten:
            bedrijfsnaam = getBedrijvenMetXY(f'{uitstootResultaat[0]}', f'{uitstootResultaat[1]}', 'Naam')
            uitstootMax = int(
                getBedrijvenMetXY(f'{uitstootResultaat[0]}', f'{uitstootResultaat[1]}', 'Max Toegestane Uitstoot'))
            uitstootTotaal = round(totaleUitstoot(uitstootResultaat[0], uitstootResultaat[1]), 2)
            print(
                f'{bedrijfsnaam} {uitstootResultaat} - Boette: {Fore.GREEN}[€{berekenBoette(uitstootTotaal, uitstootMax)}] {Fore.RESET}Uitstoot: {Fore.RED}{uitstootTotaal} / {uitstootMax}')
    else:
        print('Er zijn geen resultaten.')
    print(f'\nDatum: {huidige_datum} Tijd: {huidige_tijd}')
    print('Uitgifte: SchoneLucht BV.\n')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')