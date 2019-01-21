import copy

from Klasy import Argument, Predykat, Literal, Klauzula


# szuka operatora o najwyzszym priorytecie (uwzgedniajac pierwszenstwo nawiasu)
def najw_priorytet(zdanie):
    index_najwyzszego = -1
    najwyzszy_pri = 0
    poziom_nawiasow = 0
    dzialanie = None
    for i in range(len(zdanie) - 1, -1, -1):
        char = zdanie[i]
        if char == ')':
            poziom_nawiasow += 1
        elif char == '(':
            poziom_nawiasow -= 1
        elif char in priorytety and poziom_nawiasow == 0:
            if priorytety[char] > najwyzszy_pri:
                najwyzszy_pri = priorytety[char]
                index_najwyzszego = i
                dzialanie = char
    return index_najwyzszego, dzialanie


# tworzy listę list zachowując hierarchię wg. priorytetów operatorów
def parsuj(zdanie):
    index_najwyzszego, dzialanie = najw_priorytet(zdanie)
    if index_najwyzszego == -1:
        if zdanie[0] == '(':
            return parsuj(zdanie[1:-1])
        return zdanie
    else:
        if dzialanie == '-':
            lista = [dzialanie, parsuj(zdanie[1:])]
            return lista
        else:
            operandy = [zdanie[:index_najwyzszego], zdanie[index_najwyzszego + 1:]]
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


def rezolucja_roboczego(lista_klauzul, roboczy_akt, roboczy):
    for klauzula in lista_klauzul:
        akt_roboczy = rezolucja(klauzula, roboczy_akt)
        if akt_roboczy and akt_roboczy.Literaly:
            roboczy.append(akt_roboczy)
            lista_klauzul.append(akt_roboczy)
            return rezolucja_roboczego(lista_klauzul, akt_roboczy, roboczy)
        else:
            return False


def rezolucja(klauzula, teza):
    gornaKlauzula = teza
    dolnaKlauzula = klauzula
    nowa_gorna_klauzula = copy.deepcopy(gornaKlauzula)
    nowa_dolna_klauzula = copy.deepcopy(dolnaKlauzula)
    lista_unifikacji = []
    unifikacja_gorna = []
    unifikacja_dolna = []
    for literal_gorny in gornaKlauzula.Literaly:
        for literal_dolny in dolnaKlauzula.Literaly:
            if literal_gorny.rezolucjowalny(literal_dolny):
                for index, arg_gorny in enumerate(literal_gorny.Predykat.Argumenty):
                    arg_dolny = literal_dolny.Predykat.Argumenty[index]
                    if arg_gorny.Nazwa != arg_dolny.Nazwa:
                        lista_unifikacji.extend([arg_gorny, arg_dolny])
                for i in range(0, len(lista_unifikacji), 2):
                    pierwszy = lista_unifikacji[i]
                    drugi = lista_unifikacji[i + 1]
                    if not pierwszy.stala() and drugi.stala():
                        # for lit in nowa_gorna_klauzula.Literaly:
                        #     for arg in lit.Predykat.Argumenty:
                        #         if arg.Nazwa == pierwszy.Nazwa:
                        unifikacja_gorna.extend([pierwszy.Nazwa, drugi.Nazwa])

                    if not pierwszy.stala() and not drugi.stala() and pierwszy.Nazwa != drugi.Nazwa:
                        # for lit in nowa_gorna_klauzula.Literaly:
                        #     for arg in lit.Predykat.Argumenty:
                        #         if arg.Nazwa == pierwszy.Nazwa:
                        unifikacja_gorna.extend([pierwszy.Nazwa, drugi.Nazwa])

                    if pierwszy.stala() and not drugi.stala():
                        unifikacja_dolna.extend([drugi.Nazwa, pierwszy.Nazwa])
                if len(unifikacja_gorna) != 0:
                    for lit in nowa_gorna_klauzula.Literaly:
                        for arg in lit.Predykat.Argumenty:
                            for i in range(0, len(unifikacja_gorna), 2):
                                if arg.Nazwa == unifikacja_gorna[i]:
                                    arg.Nazwa = unifikacja_gorna[i + 1]
                                    break
                if len(unifikacja_dolna) != 0:
                    for lit in nowa_dolna_klauzula.Literaly:
                        for arg in lit.Predykat.Argumenty:
                            for i in range(0, len(unifikacja_dolna), 2):
                                if arg.Nazwa == unifikacja_dolna[i]:
                                    arg.Nazwa = unifikacja_dolna[i + 1]
                                    break
    return nowa_gorna_klauzula.usun_prawde(nowa_dolna_klauzula)


# def wnioskuj(roboczy):
#     nowa_klauzula = None
#     for klauzula in lista_klauzul:
#         nowa_klauzula = rezolucja(klauzula, roboczy)
#         if nowa_klauzula:
#             if nowa_klauzula not in lista_klauzul:
#                 lista_klauzul.append(nowa_klauzula)
#                 rezolucje.append((roboczy, klauzula, nowa_klauzula))
#                 break
#     if nowa_klauzula and nowa_klauzula is not 'F':
#         wnioskuj(nowa_klauzula)

def wnioskuj(roboczy):
    did = True
    nowa_klauzula = None
    # for klauzula in lista_klauzul:

    lista_klauzul_nazw = [str(o) for o in lista_klauzul]
    while did:
        did = False
        for klauzula in lista_klauzul:
            nowa_klauzula = rezolucja(klauzula, roboczy)
            if nowa_klauzula:
                if (nowa_klauzula not in lista_klauzul) and (str(nowa_klauzula) not in lista_klauzul_nazw):
                    lista_klauzul.append(nowa_klauzula)
                    lista_klauzul_nazw.append(str(nowa_klauzula))
                    rezolucje.append((roboczy, klauzula, nowa_klauzula))
                    break
        if nowa_klauzula and nowa_klauzula is not 'F':
            roboczy = nowa_klauzula
            did = True


zdania = [x.strip() for x in open('fakty.txt', 'r').read().split(';')]

priorytety = {
    '-': 1,
    '&': 2,
    '|': 3,
    '>': 4,
    '=': 4,
}

print('oryginalne')
print(zdania)

zdania = [parsuj(zdanie) for zdanie in zdania]
print('pogrupowane')
print(zdania)

lista_klauzul = [stworz_klauzule(zdanie) for zdanie in zdania]
print(lista_klauzul)
rezolucje = []
teza = copy.deepcopy(lista_klauzul[-1])
wnioskuj(teza)
for tuple in rezolucje:
    print(f'{tuple[0]} and {tuple[1]} => {tuple[2]}')

# TODO: mamy tutaj grupki z jakich klauzul ktora klauzula powstala, no i teraz mozemy to wykorzystac do narysowania drzewa jakos...
