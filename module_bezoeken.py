# module.bezoeken.py
import os
import sys
from colorama import init, Fore, Back, Style
init(convert=True)
import functies as f

def submenuBezoeken():
    while True:
        print(f"          {Back.YELLOW + Fore.BLACK}-=[Schonelucht BV]=-{Style.RESET_ALL}")
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Bezoeken]\n')
        print('1. Overzicht bezoeken / bezoekrapporten.txt')
        print('   Voor zoeken -> bedrijven on inspecteurs.')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1
        if keuze == 1:
            try:
                os.system('cls')
                f.printBezoeken()
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis met het ophalen van de bezoekrapporten!{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 0:
            os.system('cls')
            sys.exit()
        else:
            os.system('cls')
            print(f'{Fore.RED}ERROR - ONGELDIGE KEUZE\n{Style.RESET_ALL}')
