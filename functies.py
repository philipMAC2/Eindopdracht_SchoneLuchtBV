from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np
from colorama import init, Fore, Back, Style
init(convert=True)
import module_bedrijven as mb
import module_meetbestand as mm
import module_inspecteurs as mi

## CONTANTEN:
co2 = 1
ch4 = 25
no2 = 5
nh3 = 1000

##HOOFD MENU / start applicatie -> hier kan iederen tussen submenu's kiezen
def startApllicatie():
    print("         -=[Schonelucht BV]=-")
    while True:
        print('======================================\n           [Hoofdmenu]\n')
        print('1. Bedrijven')
        print('2. Bezoekrapporten')
        print('3. Inspecteurs')
        print('4. Meetgegevens')
        print('5. Analyseren\n')
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
            pass
        elif keuze == 0:
            afsluiten = input(f'{Fore.GREEN}\nWeet je zeker dat je het programma af wilt sluiten? [Ja/Nee] : \n{Style.RESET_ALL}')
            if afsluiten == 'Ja' or afsluiten == 'ja':
                break
            else:
                pass
        else:
            print("\n\n\n====================================")
            print(f'{Fore.RED}[!]ERROR - ONGELDIGE KEUZE[!]{Style.RESET_ALL}')

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

##FUNCTIE: Maakt een plot (kaart) om te zien waar bedrijven die vervuilend zijn liggen
def plotMeetgegevens():
    ##gasarray_1 = (np.loadtxt(gassenbestand, delimiter=',', skiprows='1')
    data = np.zeros((100, 100), dtype=float)
    for i in range(0, 100):
        for j in range(0, 100):
            data[i, j] = berekenUitstoot(i, j)
    plt.figure(figsize=(8, 8))
    plt.imshow(data, cmap='jet', origin='lower', extent=[0, 100, 0, 100])
    plt.colorbar()
    plt.xlabel('X-coördinaat')
    plt.ylabel('Y-coördinaat')
    plt.title('Kaart')
    plt.show()

##FUNCTIE: Leest bedrijven uit
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

#FUNCTIE:
def printBedrijven():
    bedrijven_data = zoekBedrijven()

    for bedrijf in bedrijven_data:
        for key, value in bedrijf.items():
            print(f'{key}: {value}')
        print('======================================\n')

def analyseerBedrijven(x, y):
    bedrijven = zoekBedrijven()
    naam = None

    for bedrijf in bedrijven:
        if bedrijf['Breedtegraad'] == str(x) and bedrijf['Lengtegraad'] == str(y):
            matching_name = bedrijf['Naam']
            break

    return naam

# printBedrijven()
# company_name = analyseerBedrijven(2, 2)
#
# if company_name:
#     print(f'Company at latitude {x} and longitude {y}: {company_name}')
# else:
#     print('No matching company found.')
