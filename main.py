from commutation_functions import (check_prior_convictions, check_fraction, serving_time, sum_convictions,
                                   subtract_convictions, fractionate_time, check_right_to_commute, commute_sentence)

import sys


# 1. perguntar se o fofo é primário. This function returns a boolean

priors = check_prior_convictions()


# 2. determinar a fração que vai definir o quantum comutado, assim como o decreto (vai ser útil depois)



decree, applied_fraction = check_fraction(priors)

# 2.1: se o decreto não contemplar comutação, o programa fecha
if decree in [2016, 2018, 2019, 2020, 2021, 2022]:
    print(f"\nNão teve comutação em {decree}. ¯\\_(ツ)_/¯ ")
    sys.exit()
elif decree < 2009:
    print(f"Ah, {decree} não rola. Este programa só funciona para decretos a partir de 2009. Antes disso tinha que cumprir a íntegra do delito impeditivo. ")
    sys.exit()


# 3. definir pena total:


print("Vamos começar pela pena total na época do decreto.\n")
total_serving_time = serving_time()

# 4 definir o número de condenações hediondas ou equiparadas:
print("Certo. Agora vamos falar sobre a pena de natureza hedionda. \n")

amount = 0

while True:
    try:
        amount = int(input("Quantas condenações por hediondo são? Se você já souber o somatório total das penas dessa natureza,"
                           " basta digitar '1': "))
        break
    except ValueError:
        print("Tem que ser um número! ")
        continue

# 5 criar um dict de relativedelta objects com as penas hediondas
heinous_convictions = {}

for i in range(amount):
    name = f"pena_{i}"
    heinous_convictions[name] = serving_time()

print(heinous_convictions)


# 6 somar as penas hediondas se for mais de uma condenação dessa natureza




if len(heinous_convictions) > 1:
    total_heinous_serving_time = sum_convictions(heinous_convictions)
else:
    total_heinous_serving_time = heinous_convictions['pena_0']


# 7 calcular as penas comuns: basta subtrair o total das hediondas



print("Agora vou calcular a pena total de delitos de natureza comum:\n ")
common_serving_time = subtract_convictions(total_serving_time, total_heinous_serving_time)

# 8 perguntar quanto tempo de pena cumprida:

print("Agora preciso saber o tempo de pena cumprida na data do decreto. \n")
time_served = serving_time()


# 9 calcular 2/3 da pena hediondas




two_thirds = fractionate_time(total_heinous_serving_time, 2 / 3)

print(f"\n 2/3 da pena hedionda: {two_thirds.years}a{two_thirds.months}m{two_thirds.days}d\n")


# a essa altura, temos pena total (total_serving_time), pena hedionda (total_heinous_serving_time), pena comum (common_serving_time), pena cumprida (time_served),
# 2/3 da pena hedionda (two_thirds)
# os decretos a partir de 2008 passaram a contemplar a marotagem de base de cálculo diferente pra quem cumpriu mais de metade da pena - excluindo-se o de 2017.

print("Vou calcular quanto da pena cumprida foi utilizada para os delitos comuns: ")
common_time_served = subtract_convictions(time_served, two_thirds)


# 10 verificar se o direito a comutação existe



if not (check_right_to_commute(common_time_served, common_serving_time, decree, priors)):
    print("É, calculei aqui e não tem direito não. ¯\\_(ツ)_/¯ ")
    sys.exit()


commuted_sentence = commute_sentence(common_time_served, common_serving_time, decree, applied_fraction)

print(f"A pena a ser comutada é {commuted_sentence.years}a{commuted_sentence.months}m{commuted_sentence.days}d")




















