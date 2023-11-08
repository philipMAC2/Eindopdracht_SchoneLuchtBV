# teste
import numpy as np
import matplotlib.pyplot as plt
import functies as f
from tqdm import tqdm
from tabulate import tabulate
from datetime import datetime
from colorama import Fore, Back, Style, init

import module_inspecteurs

init(autoreset=True)
import module_bedrijven as mb

# print(f.totaleUitstoot(10,90))
# f.printBezoeken()
# f.zoekInspecteurMetCode(1)
# f.zoekBezoekenInspecteur(1)

#mb.submenuBedrijven()
# print(f.huidige_datum)
# print(f.huidige_tijd)
# f.zoekBezoekenInspecteur(2, None, None)2

from tabulate import tabulate

from tabulate import tabulate
from colorama import Fore, Style

def zoekBedrijven(x=None, y=None, code=None):
    """Zoek en print bedrijf(en) in een tabel op basis van x en y-coördinaten of bedrijfscode."""
    bedrijven_data = f.zoekBedrijven()
    data = []

    for bedrijf in bedrijven_data:
        i = int(bedrijf['Breedtegraad'])
        j = int(bedrijf['Lengtegraad'])
        bedrijf_code = int(bedrijf['Code'])

        if (x is not None and y is not None and x == i and y == j) or (code is not None and code == bedrijf_code):
            totale_uitstoot = f.totaleUitstoot(i, j)
            uitstoot_ratio = f"{Fore.GREEN}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}" if totale_uitstoot <= int(
                bedrijf['Max Toegestane Uitstoot']) else f"{Fore.RED}{totale_uitstoot} / {bedrijf['Max Toegestane Uitstoot']}{Style.RESET_ALL}"
            boete = f.berekenBoette(int(totale_uitstoot), int(bedrijf['Max Toegestane Uitstoot']))
            boete_text = f"{Fore.GREEN}Geen boete{Fore.RESET}" if boete == 0 else f"{Fore.RED}€{boete}{Fore.RESET}"
            controle = f"{Fore.RED}Uitvoeren{Fore.RESET}" if totale_uitstoot >= int(bedrijf['Max Toegestane Uitstoot']) else f"{Fore.GREEN}Niet uitvoeren{Fore.RESET}"
            contact = f"{Fore.YELLOW}Onbekend{Fore.RESET}" if bedrijf['Contactpersoon'] == "" else bedrijf['Contactpersoon']

            data.append([
                f"{bedrijf['Code']}",
                f"{bedrijf['Naam']}",
                f"{bedrijf['Straat']}",
                f"{bedrijf['Huisnummer']}",
                f"{bedrijf['Postcode']}",
                f"{bedrijf['Breedtegraad']}",
                f"{bedrijf['Lengtegraad']}",
                uitstoot_ratio,
                boete_text,
                controle,
                f"{bedrijf['Inspectie Frequentie']}",
                contact
            ])

    if data:
        headers = ["Code", "Naam", "Straat", "Huisnr", "Postcode", "X", "Y",
                   "Uitstoot", "Boete", "Controle", "Inspecties", "Contactpersoon"]

        table = tabulate(data, headers, tablefmt="fancy_grid")
        print(table)
    else:
        if x is not None and y is not None:
            print(f'Geen bedrijf gevonden op {x}, {y}')
        elif code is not None:
            print(f'Geen bedrijf gevonden met code {code}')

zoekBedrijven(x=2,y=2)
zoekBedrijven(code=1)