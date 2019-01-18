fakty = "-((A()=B()))"
#wniosek = "C()"
tekst = fakty #+ ', -' + wniosek
#tekst = open('fakty.txt', 'r').read()
zdania = [x.strip() for x in tekst.split(',')]

priorytety = {
    '-': 1,
    '&': 2,
    '|': 3,
    '>': 4,
    '=': 4,
}


def szukajNajwPrio(zdanie):
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


def parsuj(zdanie):
    # musimy podzielic zdanie ze wzgledu na priorytety kwantyfikatorow
    najwyzszy_pri, dzialanie = szukajNajwPrio(zdanie)
    if najwyzszy_pri == -1:
        if zdanie[0] == '(':
            return parsuj(zdanie[1:-1])
        return zdanie
    else:
        if dzialanie == '-':
            lista = [dzialanie, parsuj(zdanie[1:])]  # TODO: zmienic strip na lepszy zeby bralo stringa po nawiasie
            return lista
        else:
            zdania = zdanie.split(dzialanie)
            lst1 = parsuj(zdania[0])
            lst2 = parsuj(zdania[1])
            lista = [lst1, dzialanie, lst2]
            return lista


def zamienRownowaznosc(zdanie):
    zdanko = zdanie
    if zdanko[0] == '-':
        zdanko[1] = zamienRownowaznosc(zdanko[1])  # TODEBUG: lista lub nie lista to debug.
    elif zdanko[1] in priorytety:
        zdanko[0] = zamienRownowaznosc(zdanko[0])
        zdanko[2] = zamienRownowaznosc(zdanko[2])
        if zdanko[1] == '=':
            lewa_implikacja = [zdanko[0], '>', zdanko[2]]
            prawa_implikacja = [zdanko[2], '>', zdanko[0]]
            zdanko = [lewa_implikacja, '&', prawa_implikacja]

    return zdanko


def nagacja(param):
    if param[0] == '-':
        return param[1]
    else:
        return ['-', param]


def zamienImplikacje(zdanie):
    zdanko = zdanie
    if zdanko[0] == '-':
        zdanko[1] = zamienImplikacje(zdanko[1])  # TODEBUG: lista lub nie lista to debug.
    elif zdanko[1] in priorytety:
        zdanko[0] = zamienImplikacje(zdanko[0])
        zdanko[2] = zamienImplikacje(zdanko[2])
        if zdanko[1] == '>':
            zdanko = [nagacja(zdanko[0]), '|', zdanko[2]]

    return zdanko


def redukcjaMinusow(zdanie):
    zdanko = zdanie
    if zdanko[0] == '-':
        if isinstance(zdanko[1], str):  # literal, jesli po minusie nie ma listy tylko odrazu strink
            return zdanko
        elif zdanko[1][0] == '-':  # podwojne przeczenie, tu redukcja
            zdanko[1][1] = redukcjaMinusow(zdanko[1][1])
        else:  # elif zdanko [1] in priori:
            zdanko[1][0] = redukcjaMinusow(nagacja(zdanko[1][0]))   #negujemu bo przed nawiasem minus (weszlismy do pierwszego ifa)
            zdanko[1][2] = redukcjaMinusow(nagacja(zdanko[1][2]))
            if zdanko[1][1] == '&':
                zdanko[1][1] = '|'
            elif zdanko[1][1] == '|':
                zdanko[1][1] = '&'
            return zdanko[1]
    elif zdanko[1] in priorytety:
        zdanko[0] = redukcjaMinusow(zdanko[0])
        zdanko[2] = redukcjaMinusow(zdanko[2])
    return zdanko
    #     zdanko[1] = zamienImplikacje(zdanko[1])  # TODEBUG: lista lub nie lista to debug.
    # elif zdanko[1] in priorytety:
    #     zdanko[0] = zamienImplikacje(zdanko[0])
    #     zdanko[2] = zamienImplikacje(zdanko[2])
    #     if zdanko[1] == '>':
    #         zdanko = [nagacja(zdanko[0]), '|', zdanko[2]]
    #
    # return zdanko


print('oryginalne')
print(zdania)

zdania = [parsuj(zdanie) for zdanie in zdania]
print('pogrupowane')
print(zdania)

zdania = [zamienRownowaznosc(zdanie) for zdanie in zdania]
print('zamieniona rownowaznosc')
print(zdania)

zdania = [zamienImplikacje(zdanie) for zdanie in zdania]
print('zamieniona implik')
print(zdania)

zdania = [redukcjaMinusow(zdanie) for zdanie in zdania]
print('zredukowane minusy')
print(zdania)


def rozbijAlternatywe2(zdanie):
    pass


def rozbijAlternatywe(zdanie):
    zdanko = zdanie
    if zdanko[0][1] in priorytety:          # [0] is left operand, [1] is sign [2] is right operand
        zdanko = rozbijAlternatywe2(zdanko)
        if zdanko[1] == '&':
            return zdanko
    if zdanko[2][1] in priorytety:
        zdanko = rozbijAlternatywe2(zdanko)
        return zdanko
    return [zdanko[0], '|', zdanko[1]]



def koniunkcjaAlternatyw(zdanie):
    zdanko = zdanie
    znak = zdanko[1]
    if znak in priorytety:
        if znak == '|':
            zdanko = rozbijAlternatywe(zdanko)
        elif znak == '&':
            zdanko[0] = koniunkcjaAlternatyw(zdanko[0])
            zdanko[0] = koniunkcjaAlternatyw(zdanko[0])
        else:
            raise ValueError('Tu nie moze byc innego znaku, a jak jest to blad parsowania')
    return zdanko



zdania = [koniunkcjaAlternatyw(zdanie) for zdanie in zdania]
print('na koniuncje alternatyw')
print(zdania)

quit()




def scan(_list, l=-1, i=-1):
    if isinstance(_list, list):
        print('list {}:{}'.format((l, i), _list))
        l += 1
        for i, item in enumerate(_list):
            scan(item, l, i)


scan(zdania)

# for zdanie in lista_zdan:
#     if len(zdanie) > 0:
#         lista_klauzul.append(zamienRownowaznosc(zdanie))
#
# lista_klauzul2 = []
#
# for zdanie in lista_klauzul:
#     if len(zdanie) > 0:
#         lista_klauzul2.append(zamienImplikacje(zdanie))
#
# print(lista_klauzul2)
