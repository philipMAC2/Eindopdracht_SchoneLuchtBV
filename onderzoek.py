import numpy as np
import functies as f

def nagaanWaardes(x, y):
    uitstoot_array = np.zeros((5, 5), dtype=float)

    for i in range(x - 2, x + 3):
        for j in range(y - 2, y + 3):
            uitstoot = f.berekenUitstoot(i, j)
            uitstoot_array[i - (x - 2)][j - (y - 2)] = uitstoot

    return uitstoot_array

def gemiddeldeBerekenen():
    totaal = 0
    for i in range(100):
        for j in range(100):
            totaal = totaal + f.berekenUitstoot(i,j)
    return totaal

#
# ########################################
# print(gemiddeldeBerekenen())

print('SHELL')
print(nagaanWaardes(2,2)) ## SHELL
print('ASML')
print(nagaanWaardes(14,22)) ## ASML
print('TATA')
print(nagaanWaardes(28,11)) ## Tata Steel
print('DOW')
print(nagaanWaardes(44,55)) ## Dow Chemical
print('PHILIPS')
print(nagaanWaardes(70,90)) ## Philips
print('TNO')
print(nagaanWaardes(80,20)) ## TNO
print('TNO')
print(nagaanWaardes(60,20)) ## NIKS
print('TNO')
print(nagaanWaardes(70,20)) ## NIKS

