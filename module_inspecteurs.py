# module.inspecteurs.py
import os
import sys
from colorama import init, Fore, Back, Style
init(convert=True)
import functies as f


# start applicatie
def submenuInspecteurs():
    while True:
        print(f"          {Back.YELLOW + Fore.BLACK}-=[Schonelucht BV]=-{Style.RESET_ALL}")
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Inspecteurs]\n')
        print('1. Overzicht inspecteurs / inspecteurs.txt')
        print('2. Zoeken op code')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:
            try:
                os.system('cls')
                f.printInspecteurs()
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis met het ophalen van de inspecteurs!{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 2:
            try:
                os.system('cls')
                code = input('Inspecteurscode: ')
                code = int(code)
                print(f'{Fore.YELLOW}Druk op enter als je geen min en of max datum in wilt vullen{Fore.RESET}')
                min_datum = input('Minimale bezoeksdatum (dd-mm-yyyy): ')
                max_datum = input('Maximale bezoeksdatum (dd-mm-yyyy): ')
                print(f'{min_datum} - {max_datum}')
                os.system('cls')
                f.zoekInspecteurMetCode(code)
                print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Bezoekrapporten]\n')
                f.zoekBezoekenInspecteur(code, min_datum, max_datum)
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis met het zoeken van inspecteurs, zorg dat je gegeven input voldoet aan de voorwaarden!{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 0:
            os.system('python start.py')
            sys.exit()
        else:
            os.system('cls')
            print(f'{Fore.RED}ERROR - ONGELDIGE KEUZE\n{Style.RESET_ALL}')