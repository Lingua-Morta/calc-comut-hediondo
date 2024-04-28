from dateutil.relativedelta import relativedelta

def check_prior_convictions():
    yeses = ["s", "ss", "sss", "y", "sim", "claro", "positivo", "é", "lógico", "logico", "afirmativo", "ja", "ya", "da",
             "oui", "yeah"]
    noes = ["n", "nn", "nnn", "não", "nao", "no", "nope", "negativo", "naaaao", "naaao", "naao", "nein", "nyet", "non"]

    while True:
        resposta = input("Na data do decreto o fofo era reincidente (s/n)? ")

        if resposta.strip().lower() in yeses:
            return True

        elif resposta.strip().lower() in noes:
            return False

        else:
            print("Olha, não entendi não")
            continue

def check_fraction(prior_convictions: bool):
    class YearException(Exception):
        pass

    while True:
        try:
            decree = int(input("Estamos falando do decreto de que ano? Com quatro dígitos, por favor: "))
            if len(str(decree)) != 4:
                raise YearException
            break
        except ValueError:
            print("Tem que ser um número")
            continue
        except YearException:
            print("Eu falei quatro dígitos, ô bênção")
            continue
    if decree == 2017:
        applied_fraction = 0.25 if prior_convictions else 0.33
    else:
        applied_fraction = 0.2 if prior_convictions else 0.25

    return decree, applied_fraction

def serving_time():
    while True:
        try:
            years = int(input("Quantos anos? "))

        except ValueError:
            print("Tem que ser um número, gata")
            continue

        try:
            months = int(input("Quantos meses? "))

        except ValueError:
            print("Tem que ser um número, gata")
            continue

        try:
            days = int(input("E quantos dias? "))

        except ValueError:
            print("Tem que ser um número, gata")
            continue

        while days > 30:
            months += 1
            days -= 30
        while months > 12:
            years += 1
            months -= 12

        conviction = relativedelta(years=years, months=months, days=days)

        # print(f"\n{conviction.years}a{conviction.months}m{conviction.days}d\n")
        return conviction

def sum_convictions(convictions: dict):
    years, months, days = 0, 0, 0

    for conviction in convictions.values():
        years += conviction.years
        months += conviction.months
        days += conviction.days

    while days > 30:
        months += 1
        days -= 30
    while months > 12:
        years += 1
        months -= 12

    total = relativedelta(years=years, months=months, days=days)

    print(f"\n somatório das penas: {total.years}a{total.months}m{total.days}d\n")
    return total

def subtract_convictions(higher: relativedelta, lower: relativedelta):
    hy = higher.years
    hm = higher.months
    hd = higher.days

    ly = lower.years
    lm = lower.months
    ld = lower.days

    days = hd - ld
    while days < 0:
        hm -= 1
        days += 30

    months = hm - lm
    while months < 0:
        hy -= 1
        months += 12

    years = hy - ly

    total = relativedelta(years=years, months=months, days=days)
    print(f"\n resultado: {total.years}a{total.months}m{total.days}d\n")
    return total

def fractionate_time(serving_time: relativedelta, fraction: float):
    total_days = (serving_time.years * 12 * 30 + serving_time.months * 30 + serving_time.days)
    fractioned_days = total_days * (fraction)

    years = fractioned_days // (12 * 30)
    remaining_days = fractioned_days % (12 * 30)
    months = remaining_days // 30
    days = int(remaining_days % 30)

    fractioned_serving_time = relativedelta(years=years, months=months, days=days)
    return fractioned_serving_time

def compare_convictions(higher: relativedelta, lower: relativedelta):
    hi = higher.years * 365 + higher.months * 30 + higher.days
    lo = lower.years * 365 + lower.months * 30 + lower.days
    return hi >= lo


def check_right_to_commute(time_served, serving_time: relativedelta, decree: int, prior_convictions: bool):
    if decree == 2023 and not prior_convictions:
        fraction_to_serve = fractionate_time(serving_time, 0.2)
        return (compare_convictions(time_served, fraction_to_serve))

    elif decree != 2023 and prior_convictions:
        fraction_to_serve = fractionate_time(serving_time, 1 / 3)
        return (compare_convictions(time_served, fraction_to_serve))

    else:
        fraction_to_serve = fractionate_time(serving_time, 0.25)
        return (compare_convictions(time_served, fraction_to_serve))

def commute_sentence (time_served, serving_time: relativedelta, decree: int, applied_fraction: float):
    remiscent_sentence = subtract_convictions(serving_time, time_served)
    if decree >= 2008 and decree != 2017 and compare_convictions(time_served, remiscent_sentence):

         return fractionate_time(time_served, applied_fraction)
    else:
        fractionate_time(remiscent_sentence, applied_fraction)



