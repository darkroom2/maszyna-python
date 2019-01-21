import copy


class Argument:
    def __init__(self, nazwa):
        self.Nazwa = nazwa

    def __str__(self):
        return self.Nazwa

    def stala(self):
        if not self.Nazwa[0].isupper():
            return False
        return True

    __repr__ = __str__  # dont do that often, repr should return Argument(nazwa) rather than nazwa itself..


class Predykat:
    def __init__(self, nazwa, argumenty):
        self.Nazwa = nazwa
        self.Argumenty = argumenty

    def rezolucjowalny(self, inny_predykat):
        if not (self.Nazwa == inny_predykat.Nazwa):
            return False
        if len(self.Argumenty) != len(inny_predykat.Argumenty):
            return False
        if self.Argumenty[0].Nazwa == '':
            return True

        for index, argument in enumerate(self.Argumenty):
            if argument.stala() and inny_predykat.Argumenty[index].stala():
                if argument.Nazwa != inny_predykat.Argumenty[index].Nazwa:
                    return False
        return True

    def dajacy_prawde(self, inny_predykat):
        if not (self.Nazwa == inny_predykat.Nazwa):
            return False
        if len(self.Argumenty) != len(inny_predykat.Argumenty):
            return False
        if self.Argumenty[0].Nazwa == '':
            return True

        for index, argument in enumerate(self.Argumenty):
            if argument.stala() and inny_predykat.Argumenty[index].stala():
                if argument.Nazwa != inny_predykat.Argumenty[index].Nazwa:
                    return False

            if (not argument.stala() and inny_predykat.Argumenty[index].stala()) or (
                    argument.stala() and not inny_predykat.Argumenty[index].stala()):
                return False
        return True

    def __str__(self):
        return self.Nazwa + '(' + ','.join(str(x) for x in self.Argumenty) + ')'


class Literal:
    def __init__(self, booly, predykat):
        self.Bool = booly
        self.Predykat = predykat

    def __str__(self):
        nazwa = ('' if self.Bool else '-') + str(self.Predykat)
        return nazwa

    def rezolucjowalny(self, inny_literal):
        if self.Bool == inny_literal.Bool:
            return False
        return self.Predykat.rezolucjowalny(inny_literal.Predykat)

    def dajacy_prawde(self, inny_literal):
        if self.Bool == inny_literal.Bool:
            return False
        return self.Predykat.dajacy_prawde(inny_literal.Predykat)


    __repr__ = __str__


# def stworz_liste_unifikacji(Predykat, Predykat1):
#     lista = []
#     for index, arg in enumerate(Predykat.Argumenty):
#         if arg.Nazwa != Predykat1.Argumenty[index].Nazwa:
#             lista.append((arg, Predykat1.Argumenty[index]))
#     return list


class Klauzula:
    def __init__(self, literaly):
        self.Literaly = literaly

    def dodaj(self, klauzula):
        self.Literaly.extend(klauzula.Literaly)
        return self

    def __str__(self):
        return '|'.join(str(x) for x in self.Literaly)  # + f'{id(self)}'

    def usun_prawde(self, inna_klauzula):
        inna_klauzula = copy.deepcopy(inna_klauzula)
        for lit_gorna in self.Literaly:
            for lit_dolna in inna_klauzula.Literaly:
                if lit_gorna.dajacy_prawde(lit_dolna):
                    self.Literaly.remove(lit_gorna)
                    inna_klauzula.Literaly.remove(lit_dolna)
                    # self.Literaly.extend(inna_klauzula.Literaly)
                    seta = []
                    setb = []
                    for lit in self.Literaly:
                        if lit.Predykat.Nazwa not in setb:
                            seta.append(lit)
                            setb.append(lit.Predykat.Nazwa)
                    for lit in inna_klauzula.Literaly:
                        if lit.Predykat.Nazwa not in setb:
                            seta.append(lit)
                            setb.append(lit.Predykat.Nazwa)
                    if seta:
                        return Klauzula(seta)
                    else:
                        return 'F'
        return None

    # def przeprowadz_rezolucje(self, inna_klauzula):
    #     gorna_klauzula = Klauzula(inna_klauzula.Literaly)
    #     dolna_klauzula = Klauzula(self.Literaly)
    #
    #     for literal_z_gornej_klauzuli in gorna_klauzula.Literaly:
    #         for literal_z_dolnej_klauzuli in dolna_klauzula.Literaly:
    #             if literal_z_gornej_klauzuli.rezolucjowalny(literal_z_dolnej_klauzuli):
    #                 lista_unifikacji = stworz_liste_unifikacji(literal_z_gornej_klauzuli.Predykat, literal_z_dolnej_klauzuli.Predykat)
    #                 print(lista_unifikacji)
                    
    __repr__ = __str__
