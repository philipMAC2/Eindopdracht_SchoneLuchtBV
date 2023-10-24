# module.bedrijven.py
import functies as f


# start applicatie
def submenuBedrijven():
    while True:
        print('\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n             [Bedrijven]\n')
        print('1. Overzicht bedrijven / bedrijven.txt')
        print('2. Zoeken op naam')
        print('3. Zoeken op X, Y')
        print('4. Uitstoot controleren')
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
            x = input('Breedtegraad (x): ')
            y = input('Lengtegraad (y)')
            print("\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n")
            print(f.zoekBedrijvenMetXY(x, y))
            input(f'Druk op een toets op verder te gaan...')
        elif keuze == 4:
            pass
        elif keuze == 0:
            f.startApllicatie()
        else:
            print("\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
            print(f'[!]ERROR - ONGELDIGE KEUZE[!]')
