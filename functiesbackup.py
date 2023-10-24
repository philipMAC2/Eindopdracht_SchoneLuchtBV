from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import time
import module_bedrijven as mb
import module_meetbestand as mm
import module_inspecteurs as mi

###CONTANTEN:
co2 = 1
ch4 = 25
no2 = 5
nh3 = 1000


###HOOFD MENU / start applicatie -> hier kan iederen tussen submenu's kiezen
def startApllicatie():
    print("         -=[Schonelucht BV]=-")
    while True:
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Hoofdmenu]\n')
        print('1. Bedrijven')
        print('2. Bezoekrapporten')
        print('3. Inspecteurs')
        print('4. Meetgegevens')
        print('0. Afsluiten\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:
            mb.submenuBedrijven()
            break
        elif keuze == 2:
            pass
        elif keuze == 3:
            pass
        elif keuze == 4:
            mm.submenuMeetbestand()
            break
        elif keuze == 0:
            afsluiten = input(f'\nWAARSCHUWING - Weet je zeker dat je het programma af wilt sluiten? \n[Ja/Nee] ')
            if afsluiten == 'Ja' or afsluiten == 'ja':
                break
            else:
                pass
        else:
            print("\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(f'ERROR - Ongeldige keuze!')


###FUNCTIE: Zoekt uitstoot (gehele rij met keywords) op basis van x en y
def zoekGegevensXY(x, y):
    gevondenGegevens = []

    with open('gassen.csv', 'r') as bestand:
        kopregel = bestand.readline()
        kolomnamen = kopregel.strip().split(',')

        for lijn in bestand:
            gegevens = lijn.strip().split(',')

            if len(gegevens) >= 2:
                breedtegraad = gegevens[0]
                lengtegraad = gegevens[1]

                if breedtegraad == x and lengtegraad == y:
                    gevondenGegevens.append(dict(zip(kolomnamen, gegevens)))

    return gevondenGegevens


###FUNCTIE: Berekent uitstoot, doormiddel van opsommen van alle uistoten en het vermenigvuldigen met de constanten
def berekenUitstoot(x, y):
    x = str(x)
    y = str(y)
    resultaat = zoekGegevensXY(x, y)
    if resultaat:
        totaal = 0.0
        for rij in resultaat:
            totaal = (float(rij['CO2']) * co2) + (float(rij['CH4']) * ch4) + (float(rij['NO2']) * no2) + (
                    float(rij['NH3']) * nh3)
        return totaal
    else:
        return 0.0


###FUNCTIE: Berekend de uitstoot van laag 1
def berekenLaag1Uitstoot(x, y):
    totaal_laag1 = 0.0

    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            uitstoot = berekenUitstoot(i, j)
            totaal_laag1 = totaal_laag1 + uitstoot
    totaal_laag1 = totaal_laag1 * 0.5
    return totaal_laag1


###FUNCTIE: Berekend de uitstoot van laag 2
def berekenLaag2Uitstoot(x, y):
    totaal_laag2 = 0.0

    for i in range(x - 2, x + 3):
        for j in range(y - 2, y + 3):
            if i == x and j == y:
                continue
            if x - 1 <= i <= x + 1 and y - 1 <= j <= y + 1:
                continue
            uitstoot = berekenUitstoot(i, j)
            totaal_laag2 = totaal_laag2 + uitstoot
    totaal_laag2 = totaal_laag2 * 0.25
    return totaal_laag2


###FUNCTIE: Berekend de totoale uitstoot doormiddel van alles bij elkaar optellen
def totaleUitstoot(x, y):
    totaleUitstoot = berekenUitstoot(x, y) + berekenLaag1Uitstoot(x, y) + berekenLaag2Uitstoot(x, y)
    return totaleUitstoot


###FUNCTIE: Maakt een plot (kaart) om te zien waar bedrijven die vervuilend zijn liggen
def plotMeetgegevens():
    data = np.zeros((100, 100), dtype=float)
    plt.figure(figsize=(8, 8))

    for i in range(0, 100):
        for j in range(0, 100):
            data[j, i] = berekenUitstoot(i, j)
            resultaat = getBedrijvenMetXY(f'{i}', f'{j}', 'Naam')
            if resultaat is not None:
                print(f'{resultaat} = {i} , {j}')
                plt.text(i + 3, j, f"{resultaat}", fontsize=10, color='white')

    plt.imshow(data, cmap='jet', origin='lower', extent=[0, 100, 0, 100])
    plt.colorbar()
    plt.grid(True, color='gray', linestyle='--')
    plt.xlabel('Breedtegraad')
    plt.ylabel('Lengtegraad')
    plt.title('Kaart')
    plt.show()


###FUNCTIE: Leest bedrijven.txt uit
def zoekBedrijven():
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


# FUNCTIE: Maakt een tabel voor het tonen van bedrijven
def printBedrijven():
    bedrijven_data = zoekBedrijven()

    # Maak een lijst van lijsten met de gegevens van elk bedrijf
    data = []
    for bedrijf in bedrijven_data:
        data.append([
            f"{bedrijf['Code']}",
            f"{bedrijf['Naam']}",
            f"{bedrijf['Straat']}",
            f"{bedrijf['Huisnummer']}",
            f"{bedrijf['Postcode']}",
            f"{bedrijf['Breedtegraad']}",
            f"{bedrijf['Lengtegraad']}",
            f"{bedrijf['Max Toegestane Uitstoot']}",
            f"{bedrijf['Boete']}",
            f"{bedrijf['Controle']}",
            f"{bedrijf['Inspectie Frequentie']}",
            f"{bedrijf['Contactpersoon']}"
        ])

    headers = ["Code", "Naam", "Straat", "Huisnummer", "Postcode", "Breedtegraad", "Lengtegraad",
               "Max Toegestane Uitstoot", "Boete", "Controle", "Inspectie Frequentie", "Contactpersoon"]

    table = tabulate(data, headers, tablefmt="fancy_grid")

    print("\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
    print(table)
    print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")


###FUNCTIE: Zoekt een bedrijf op basis van x en y,
def zoekBedrijvenMetXY(x, y):
    bedrijven = zoekBedrijven()
    resultaten = []
    for bedrijf in bedrijven:
        breedtegraad = bedrijf.get('Breedtegraad', '')
        lengtegraad = bedrijf.get('Lengtegraad', '')
        # Controleer of de breedtegraad en lengtegraad overeenkomen met de opgegeven waarden
        if breedtegraad == x and lengtegraad == y:
            resultaten.append(bedrijf)
    if resultaten:
        resultaat_string = ""
        for bedrijf in resultaten:
            for naam, inhoud in bedrijf.items():
                resultaat_string += f'{naam}: {inhoud}\n'
    else:
        resultaat_string = f'Bericht - Geen bedrijven gevonden met breedtegraad (x) {x} en lengtegraad (y) {y}'
    return resultaat_string


###Functie: Met een zoekterm bijvoorbeeld code of naam kan op basis van x en y informatie over een bedrijf opevraagd worden
def getBedrijvenMetXY(x, y, zoekterm):
    bedrijven = zoekBedrijven()
    resultaat = None
    for bedrijf in bedrijven:
        breedtegraad = bedrijf.get('Breedtegraad', '')
        lengtegraad = bedrijf.get('Lengtegraad', '')
        # Controleer of de breedtegraad en lengtegraad overeenkomen met de opgegeven waarden
        if breedtegraad == x and lengtegraad == y:
            resultaat = bedrijf.get(zoekterm, '')
            break
    return resultaat


####Algoritme voor het zoeken naar niet bestaande bedrijven
#####################################################################################################################
###Functie: true or false -> checkt of de waarde per laag allemaal hetzelfde zijn om na te gaan of het een bedrijf is
def analyseerXY(x, y):
    uitstoot_arrayLaag1 = np.zeros((3, 3), dtype=float)
    uitstoot_arrayLaag2 = np.zeros((5, 5), dtype=float)
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            uitstoot = berekenUitstoot(i, j)
            uitstoot_arrayLaag1[i - (x - 1)][j - (y - 1)] = uitstoot

    niet_nul_waarden = uitstoot_arrayLaag1[uitstoot_arrayLaag1 != 0.0]
    if len(niet_nul_waarden) > 0 and np.all(niet_nul_waarden == niet_nul_waarden[0]):
        boolLaag1 = True
    else:
        boolLaag1 = False

    i = 0
    j = 0
    for i in range(x - 2, x + 3):
        for j in range(y - 2, y + 3):
            if i == x and j == y:
                continue
            if x - 1 <= i <= x + 1 and y - 1 <= j <= y + 1:
                continue
            uitstootLaag2 = berekenUitstoot(i, j)
            uitstoot_arrayLaag2[i - (x - 2)][j - (y - 2)] = uitstootLaag2

    niet_nul_waarden = uitstoot_arrayLaag1[uitstoot_arrayLaag1 != 0.0]
    if len(niet_nul_waarden) > 0 and np.all(niet_nul_waarden == niet_nul_waarden[0]):
        boolLaag2 = True
    else:
        boolLaag2 = False

    if boolLaag1 == True and boolLaag2 == True:
        bedrijfsnaam = getBedrijvenMetXY(f'{x}', f'{y}', 'Naam')
        if bedrijfsnaam == None:
            print(f'Er is een bedrijf op {x} , {y} gevonden. Totale uitstoot: {totaleUitstoot(x, y)}')


def analyseerMeetbestand():
    for i in range(100):
        for j in range(100):
            analyseerXY(i, j)

