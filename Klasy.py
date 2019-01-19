class Argument:
    def __init__(self, nazwa):
        self.Nazwa = nazwa

    def __str__(self):
        return self.Nazwa

    __repr__ = __str__  # dont do that often, repr should return Argument(nazwa) rather than nazwa itself..


class Predykat:
    def __init__(self, nazwa, argumenty):
        self.Nazwa = nazwa
        self.Argumenty = argumenty

    def __str__(self):
        return self.Nazwa + '(' + ','.join(str(x) for x in self.Argumenty) + ')'


class Literal:
    def __init__(self, booly, predykat):
        self.Bool = booly
        self.Predykat = predykat

    def __str__(self):
        nazwa = ('' if self.Bool else '-') + str(self.Predykat)
        return nazwa

    def __bool__(self):
        return self.Bool

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
