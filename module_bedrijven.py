# module.bedrijven.py
import os
import sys

import functies as f
from colorama import Fore, Back, Style, init
init(autoreset=True)


# start applicatie
def submenuBedrijven():
    while True:
        print(f"          {Back.YELLOW + Fore.BLACK}-=[Schonelucht BV]=-{Style.RESET_ALL}")
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Bedrijven]\n')
        print('1. Overzicht bedrijven / bedrijven.txt')
        print('2. Zoeken op X, Y')
        print('3. Zoeken op naam')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:
            try:
                os.system('cls')
                f.printBedrijven()
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis met het ophalen van de bedrijven!{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 2:
            try:
                os.system('cls')
                x = input('Breedtegraad (x): ')
                y = input('Lengtegraad (y): ')
                os.system('cls')
                print(f.zoekBedrijvenMetXY(x, y))
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis met het zoeken van bedrijven!{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 3:
            pass
        elif keuze == 0:
            os.system('python start.py')
        else:
            print(f'{Fore.RED}ERROR - ONGELDIGE KEUZE\n{Style.RESET_ALL}')
