# module.bezoeken.py
from colorama import init, Fore, Back, Style
init(convert=True)
import functies as f


# start applicatie
def submenuBedrijven():
    while True:
        print('======================================\n           [Bezoeken]\n')
        print('1. Overzicht bezoeken / bezoekrapporten.txt')
        print('2. Zoeken op naam')
        print('3. Zoeken op X, Y')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:
            f.printBedrijven()
            input(f'Druk op een toets op verder te gaan...')
        elif keuze == 2:
            pass
        elif keuze == 3:
            pass
        elif keuze == 4:
            pass
        elif keuze == 0:
            f.startApllicatie()
        else:
            print("\n\n\n====================================")
            print(f'[!]ERROR - ONGELDIGE KEUZE[!]')
