from Klasy import Argument, Predykat, Literal, Klauzula

tekst = open('fakty.txt', 'r').read()
zdania = [x.strip() for x in tekst.split(',')]

priorytety = {
    '-': 1,
    '&': 2,
    '|': 3,
    '>': 4,
    '=': 4,
}


# szuka operatora o najwyzszym priorytecie (uwzgedniajac pierwszenstwo nawiasu)
def szukaj_najw_priorytet(zdanie):
    poziom_nawiasow = 0
    najwyzszy_pri = -1
    dzialanie = None
    for char in reversed(zdanie):
        if char == ')':
            poziom_nawiasow += 1
        elif char == '(':
            poziom_nawiasow -= 1
        elif char in priorytety and poziom_nawiasow == 0 and priorytety[char] > najwyzszy_pri:
            najwyzszy_pri = priorytety[char]
            dzialanie = char
    return najwyzszy_pri, dzialanie


# tworzy listę list zachowując hierarchię wg. priorytetów operatorów
def parsuj(zdanie):
    najwyzszy_pri, dzialanie = szukaj_najw_priorytet(zdanie)
    if najwyzszy_pri == -1:
        if zdanie[0] == '(':
            return parsuj(zdanie[1:-1])
        return zdanie
    else:
        if dzialanie == '-':
            lista = [dzialanie, parsuj(zdanie[1:])]
            return lista
        else:
            operandy = zdanie.split(dzialanie)
            lst1 = parsuj(operandy[0])
            lst2 = parsuj(operandy[1])
            lista = [lst1, dzialanie, lst2]
            return lista


def parsuj_predykat(predykat):
    nazwa, args = predykat.split('(')
    argumenty = [Argument(x.strip()) for x in args[:-1].split(',')]
    return Predykat(nazwa, argumenty)


def stworz_literal(zdanie):
    bool_val = False if zdanie[0] == '-' else True
    predykat = zdanie if bool_val else zdanie[1]
    predykat = parsuj_predykat(predykat)
    return Literal(bool_val, predykat)


def stworz_klauzule(zdanie):
    if zdanie[1] in priorytety:  # klauzula, wiec trzeba wyluskac literaly
        klauzula1 = stworz_klauzule(zdanie[0])
        klauzula2 = stworz_klauzule(zdanie[2])
        return klauzula1.dodaj(klauzula2)
    else:
        literal = [stworz_literal(zdanie)]
        return Klauzula(literal)


print('oryginalne')
print(zdania)

zdania = [parsuj(zdanie) for zdanie in zdania]
print('pogrupowane')
print(zdania)

lista_klauzul = [stworz_klauzule(zdanie) for zdanie in zdania]
print(lista_klauzul)

# TODO: Clauses (for now only 2 argument clauses) are parsed properly, now we have to implement algorithm.
