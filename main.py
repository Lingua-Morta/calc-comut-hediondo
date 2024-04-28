from commutation_functions import (check_prior_convictions, check_fraction, serving_time, sum_convictions,
                                   subtract_convictions, fractionate_time, check_right_to_commute, commute_sentence)

import sys


decrees = {2023: "11.846", 2017: "9.246", 2015: "8.615", 2014: "8.380", 2013: "8.172",
            2012: "7.873", 2011: "7.648", 2010: "7.420", 2009: "7.046", 2008: "6.706"}


# 1. perguntar se o fofo é primário. This function returns a boolean

priors = check_prior_convictions()


# 2. determinar a fração que vai definir o quantum comutado, assim como o decreto (vai ser útil depois)



decree_year, applied_fraction = check_fraction(priors)

# 2.1: se o decreto não contemplar comutação, o programa fecha
if decree_year in [2016, 2018, 2019, 2020, 2021, 2022]:
    print(f"\nNão teve comutação em {decree_year}. ¯\\_(ツ)_/¯ ")
    sys.exit()
elif decree_year < 2009:
    print(f"Ah, {decree_year} não rola. Este programa só funciona para decretos a partir de 2009. Antes disso tinha que cumprir a íntegra do delito impeditivo. ")
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
    if amount > 1:
        print(f"Condenação nº {i+1}: ")
    else:
        pass
    heinous_convictions[name] = serving_time()



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

has_right, fraction_to_serve = check_right_to_commute(common_time_served, common_serving_time, decree_year, priors)

if not (has_right):
    print("É, calculei aqui e não tem direito não. ¯\\_(ツ)_/¯ ")
    sys.exit()


commuted_sentence = commute_sentence(common_time_served, common_serving_time, decree_year, applied_fraction)

print(f"A pena a ser comutada é {commuted_sentence.years}a{commuted_sentence.months}m{commuted_sentence.days}d")

#********************************************************************************
primario = "primário(a)" if not priors else "reincidente"

dispositivo = "art. 2º"

if decree_year == 2023:
    dispositivo = "art. 3º"
elif decree_year == 2017 and not priors:
    dispositivo = "art. 7º, I, a"
elif decree_year == 2017 and priors:
    dispositivo = "art. 7º, I, b"

#esta é a fração a incidir
textual_applied_fraction = "1/3"

if applied_fraction == 0.2:
    textual_applied_fraction = "1/5"
elif applied_fraction == 0.25:
    textual_applied_fraction = "1/4"

#esta é a fração a ser cumprida - não é uma variável autônoma

textual_served_fraction = "1/4"
if decree_year == 2023 and not priors:
    textual_served_fraction = "1/5"

elif decree_year != 2023 and priors:
    textual_served_fraction = "1/3"





text = f'''
MM(ª). Juiz(a),

Até 25.12.{decree_year}, o(a) apenado(a), {primario}, tinha em seu desfavor {total_serving_time.years}a{total_serving_time.months}m{total_serving_time.days}d de pena imposta, da qual {total_heinous_serving_time.years}a{total_heinous_serving_time.months}m{total_heinous_serving_time.days}d de delitos hediondos ou equiparados e {common_serving_time.years}a{common_serving_time.months}m{common_serving_time.days}d de delitos de natureza comum.

O(a) apenado(a) havia cumprido, cumulativamente, dois terços da pena impeditiva ({two_thirds.years}a{two_thirds.months}m{two_thirds.days}d) e {textual_served_fraction} da pena comum ({fraction_to_serve.years}a{fraction_to_serve.months}m{fraction_to_serve.days}d), superando a fração necessária para a comutação do {dispositivo}, do decreto {decrees[decree_year]}/{decree_year}, pelo que se requer o reconhecimento da comutação de {commuted_sentence.years}a{commuted_sentence.months}m{commuted_sentence.days}d de pena. 


Curitiba, data do protocolo.

Guilherme Dáquer Filho
Defensor Público




'''

with open ('peticao.txt', 'w') as file:
    file.write (text)



















