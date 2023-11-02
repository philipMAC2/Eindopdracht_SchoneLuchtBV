# teste
import numpy as np
import matplotlib.pyplot as plt
import functies as f
from tqdm import tqdm
from tabulate import tabulate
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

module_inspecteurs.submenuInspecteurs()