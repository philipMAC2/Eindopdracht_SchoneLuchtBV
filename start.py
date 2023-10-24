# start.py
try:
    from colorama import init, Fore, Back, Style
    init(convert=True)
    import functies as f
    try:
        f.startApllicatie()
    except:
        print(
            f'{Fore.RED}\n\n[!]ERROR - ER GING IETS MIS MET HET OPSTARTEN VAN DE APPLICATIE, LEES README.TXT\n\n{Style.RESET_ALL}')
except:
    print('\n\n[!]ERROR - HET INLADEN VAN LIBRARIES/FUNCTIES GING MIS, LEES README.TXT[!]\n\n')



