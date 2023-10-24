# module.bedrijven.py

import functies as f

# start applicatie

def submenuMeetbestand():
    while True:
        print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n            [Meetbestand]\n')
        print('1. Overzichtskaart')
        print('2. Analyse uitvoeren')
        print('0. Terug\n')

        try:
            keuze = int(input('Uw keuze : '))
        except ValueError:
            keuze = -1

        if keuze == 1:
            doorgaan = input(f'\nWAARSCHUWING - Het genereren van overzichtskaart kan 2 a 3 minuen duren, wilt u doorgaan? \n[Ja/Nee] ')
            if doorgaan == 'Ja' or doorgaan == 'ja':
                try:
                    f.plotMeetgegevens()
                    print(f'BERICHT - de kaart is succesvol gegenereerd.\n')
                except:
                    print("\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f'ERROR - Het genereren van een kaart is niet gelukt!\n')
            else:
                print(f'BERICHT - Het genereren van de kaart is geanulleerd.\n')
        elif keuze == 2:
                try:
                    f.analyseerMeetbestand()
                    print(f'BERICHT - het analyse rapport is gereed.\n')
                    input(f'Druk op een toets op verder te gaan...')
                except:
                    print("\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
                    print(f'ERROR - Er ging iets mis tijdens het genereren van het analyse rapport!\n')
                    input(f'Druk op een toets op verder te gaan...')
        elif keuze == 3:
            pass
        elif keuze == 0:
            f.startApllicatie()
        else:
            print("\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(f'ERROR - Ongeldige keuze!\n')
