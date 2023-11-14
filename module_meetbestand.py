# module.bedrijven.py
import os
import sys
import functies as f
from colorama import Fore, Back, Style, init

init(autoreset=True)
map_pad = "analyserapporten/"


def submenuMeetbestand():
    while True:
        print(f"          {Back.YELLOW + Fore.BLACK}-=[Schonelucht BV]=-{Style.RESET_ALL}")
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n            [Meetbestand]\n')
        print('1. Overzichtskaart')
        print('2. Analyse uitvoeren')
        print('3. Analyse rapporten')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:

            doorgaan = input(
                f'\n{Fore.YELLOW}WAARSCHUWING - Het genereren van overzichtskaart kan even duren, wilt u doorgaan? \n[Ja/Nee] {Style.RESET_ALL}')
            if doorgaan == 'Ja' or doorgaan == 'ja':
                try:
                    os.system('cls')
                    f.plotMeetgegevens()
                    print(f'{Fore.GREEN}BERICHT - de kaart is succesvol gegenereerd.{Style.RESET_ALL}\n')
                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
                except:
                    os.system('cls')
                    print(f'{Fore.RED}ERROR - Het genereren van een kaart is niet gelukt!{Style.RESET_ALL}\n')
                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
            else:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Het genereren van de kaart is geanulleerd.{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 2:
            os.system('cls')
            doorgaan = input(
                f'\n{Fore.YELLOW}WAARSCHUWING - - Het analyseren kan even duren, wilt u doorgaan? \n[Ja/Nee] {Style.RESET_ALL}')
            if doorgaan == 'Ja' or doorgaan == 'ja':
                try:
                    os.system('cls')
                    f.analyseerMeetbestand()
                    print(f'{Fore.GREEN}BERICHT - het analyse rapport is gereed.{Style.RESET_ALL}\n')
                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
                except:
                    os.system('cls')
                    print(
                        f'{Fore.RED}ERROR - Er ging iets mis tijdens het genereren van het analyse rapport!{Style.RESET_ALL}\n')
                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
            else:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Het analyseren is geanulleerd.{Style.RESET_ALL}\n')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 3:
            try:
                os.system('cls')
                bestanden = f.toon_bestanden(map_pad)
                if bestanden:
                    nummer = int(input("Voer het nummer van het bestand in om te openen: "))
                    os.system('cls')
                    if 1 <= nummer <= len(bestanden):
                        f.lees_bestand(map_pad, bestanden[nummer - 1])
                    else:
                        print(f'{Fore.RED}ERROR - Ongeldige invoer!\n{Style.RESET_ALL}')

                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
                else:
                    print(f'{Fore.RED}ERROR - Geen bestanden beschikbaar!\n{Style.RESET_ALL}')
                    input(f'Druk op een toets op verder te gaan...')
                    os.system('cls')
            except:
                os.system('cls')
                print(f'{Fore.RED}ERROR - Er ging iets mis, zorg dat je invoer voldoet aan de voorwaarden!\n{Style.RESET_ALL}')
                input(f'Druk op een toets op verder te gaan...')
                os.system('cls')
        elif keuze == 0:
            os.system('cls')
            sys.exit()
        else:
            os.system('cls')
            print(f'{Fore.RED}ERROR - Ongeldige keuze!\n{Style.RESET_ALL}')
