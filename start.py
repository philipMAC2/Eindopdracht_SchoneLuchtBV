try:
    import sys
    import os
    import time
    import module_bedrijven as mb
    import module_meetbestand as mm
    import module_inspecteurs as mi
    import module_bezoeken as mbe
    import functies as f
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
    os.system('cls')
except:
    print('\n\nER GING IETS MIS MET HET LADEN VAN DEPENDENCIES, LEES README.TXT EN REQUIREMENTS.TXT!\n\n')

while True:
    print(f"          {Back.YELLOW + Fore.BLACK}-=[Schonelucht BV]=-{Style.RESET_ALL}")
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
        try:
            os.system('cls')
            mb.submenuBedrijven()
        except:
            os.system('cls')
    elif keuze == 2:
        try:
            os.system('cls')
            mbe.submenuBezoeken()
        except:
            os.system('cls')
    elif keuze == 3:
        try:
            os.system('cls')
            mi.submenuInspecteurs()
        except:
            os.system('cls')
    elif keuze == 4:
        try:
            os.system('cls')
            mm.submenuMeetbestand()
        except:
            os.system('cls')
    elif keuze == 0:
        os.system('cls')
        afsluiten = input(
            f'\n{Fore.YELLOW}WAARSCHUWING - Weet je zeker dat je het programma af wilt sluiten? [Ja/Nee] {Style.RESET_ALL}')
        if afsluiten == 'Ja' or afsluiten == 'ja':
            os.system('cls')
            print(f'{Fore.RED}Het systeem wordt afgesloten...\n{Style.RESET_ALL}')
            time.sleep(2)
            os.system('cls')
            print(f'{Fore.RED}[Systeem afgesloten]\n{Style.RESET_ALL}')
            sys.exit()
        else:
            os.system('cls')
            pass
    else:
        os.system('cls')
        print(f'{Fore.RED}ERROR - Ongeldige keuze!\n{Style.RESET_ALL}')