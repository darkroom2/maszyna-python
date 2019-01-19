import copy

from Klasy import Argument, Predykat, Literal, Klauzula

tekst = open('fakty.txt', 'r').read()
zdania = tekst.split('\n')

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


# TODO: dla ostatniego elementu przed parsowaniem na klauzule zaznaczyc ze powstale klauzule to TEZY

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
        # TODO: if exisct add klauzula 3 and 4 and...
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
#TODO: doadc do listy klauzul LISTE KLAUZUL Z TEZY
print(lista_klauzul)

# instnieje_rezolucja = True
#
# while instnieje_rezolucja:
#     istnieje_rezolucja = False

# def sprawdz_rezolucje:
#     pass
tezy = lista_klauzul[-1]
roboczy = []


def rezolucja_roboczego(lista_klauzul, roboczy_akt, roboczy):
    if roboczy_akt is None:
        return False
    else:
        for klauzula in lista_klauzul:
            roboczy += rezolucja(klauzula, roboczy_akt)
            roboczy_akt = roboczy[-1]
            lista_klauzul += roboczy_akt
            if rezolucja_roboczego(lista_klauzul, roboczy_akt, roboczy):
                break


# output = da_sie_rezolucje(lista_klauzul[0].Literaly[0], lista_klauzul[1].Literaly[0])
# print(output)
# quit()
# lista_rezolucji = []

# def zaszlaRezolucja(gornaKlauzula, dolnaKlauzula):
#     pass


def rezolucja(klauzula, teza):
    gornaKlauzula = teza
    dolnaKlauzula = klauzula
    nowa_gorna_klauzula = copy.deepcopy(gornaKlauzula)
    nowa_dolna_klauzula = copy.deepcopy(dolnaKlauzula)
    lista_unifikacji = []
    unifikacja_gorna = []
    unifikacja_dolna = []
    rezolucjowalny = False
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

                for lit in nowa_gorna_klauzula.Literaly:
                    for arg in lit.Predykat.Argumenty:
                        for i in range(0, len(unifikacja_gorna), 2):
                            if arg.Nazwa == unifikacja_gorna[i]:
                                arg.Nazwa = unifikacja_gorna[i + 1]
                                break

                for lit in nowa_dolna_klauzula.Literaly:
                    for arg in lit.Predykat.Argumenty:
                        for i in range(0, len(unifikacja_dolna), 2):
                            if arg.Nazwa == unifikacja_dolna[i]:
                                arg.Nazwa = unifikacja_dolna[i + 1]
                                break


tezy = [lista_klauzul[-1]]


def wnioskuj(lista_klauzul, roboczy):
    for klauzula in lista_klauzul:
        for teza in tezy:
            try:
                roboczy += rezolucja(klauzula, teza)
            except TypeError:
                continue
            lista_klauzul += roboczy
            roboczy_akt = roboczy[-1]
            if rezolucja_roboczego(lista_klauzul, roboczy_akt, roboczy):
                break


wnioskuj(lista_klauzul, roboczy)

# TODO: odzielna lista tez
# TODO: Clauses (for now only 2 argument clauses) are parsed properly, now we have to implement algorithm.
