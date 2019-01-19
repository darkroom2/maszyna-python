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

    __repr__ = __str__


class Klauzula:
    def __init__(self, literaly):
        self.Literaly = literaly

    def dodaj(self, klauzula):
        self.Literaly.extend(klauzula.Literaly)
        return self

    def __str__(self):
        return '|'.join(str(x) for x in self.Literaly)

    __repr__ = __str__
