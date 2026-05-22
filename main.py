from abc import ABC, abstractmethod
from datetime import date, timedelta


class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: float):
        self.__rendszam = rendszam
        self.__tipus = tipus
        self.__berleti_dij = berleti_dij

    @property
    def rendszam(self) -> str:
        return self.__rendszam

    @property
    def tipus(self) -> str:
        return self.__tipus

    @tipus.setter
    def tipus(self, ertek: str):
        if not ertek:
            raise ValueError("A tipus nem lehet ures!")
        self.__tipus = ertek

    @property
    def berleti_dij(self) -> float:
        return self.__berleti_dij

    @berleti_dij.setter
    def berleti_dij(self, ertek: float):
        if ertek < 0:
            raise ValueError("A berleti dij nem lehet negativ!")
        self.__berleti_dij = ertek

    @abstractmethod
    def leiras(self) -> str:
        pass

    def __str__(self) -> str:
        return (
            f"{self.leiras()} | Rendszam: {self.__rendszam} "
            f"| Dij: {self.__berleti_dij} Ft/nap"
        )


class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: float, ferohely: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__ferohely = ferohely

    @property
    def ferohely(self) -> int:
        return self.__ferohely

    def leiras(self) -> str:
        return f"Szemelyauto  {self.tipus}  ({self.__ferohely} ferohely)"


class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: float, teherbiras_kg: float):
        super().__init__(rendszam, tipus, berleti_dij)
        self.__teherbiras_kg = teherbiras_kg

    @property
    def teherbiras_kg(self) -> float:
        return self.__teherbiras_kg

    def leiras(self) -> str:
        return f"Teherauto  {self.tipus}  ({self.__teherbiras_kg} kg)"


class Berles:
    def __init__(self, auto: Auto, berlo_neve: str, datum: date):
        self.__auto = auto
        self.__berlo_neve = berlo_neve
        self.__datum = datum

    @property
    def auto(self) -> Auto:
        return self.__auto

    @property
    def berlo_neve(self) -> str:
        return self.__berlo_neve

    @property
    def datum(self) -> date:
        return self.__datum

    def ar(self) -> float:
        return self.__auto.berleti_dij

    def __str__(self) -> str:
        return (
            f"Berlo: {self.__berlo_neve} | "
            f"Datum: {self.__datum} | "
            f"{self.__auto} | "
            f"Fizetendo: {self.ar()} Ft"
        )


class Autokolcsonzo:
    def __init__(self, nev: str):
        self.__nev = nev
        self.__autok: list[Auto] = []
        self.__berlesek: list[Berles] = []

    @property
    def nev(self) -> str:
        return self.__nev

    def auto_hozzaadasa(self, auto: Auto):
        self.__autok.append(auto)

    def auto_berlese(self, rendszam: str, berlo_neve: str, datum: date) -> float:
        if not berlo_neve.strip():
            raise ValueError("A berlo neve nem lehet ures!")
        if datum < date.today():
            raise ValueError("A berlesi datum nem lehet multbeli!")

        auto = self.__auto_keresese(rendszam)
        if auto is None:
            raise ValueError(f"Nem talalhato auto '{rendszam}' rendszammal!")

        if self.__auto_foglalt_e(rendszam, datum):
            raise ValueError(
                f"Az auto ({rendszam}) mar foglalt erre a napra ({datum})!"
            )

        berles = Berles(auto, berlo_neve, datum)
        self.__berlesek.append(berles)
        return berles.ar()

    def berles_lemondasa(self, rendszam: str, datum: date) -> bool:
        for berles in self.__berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                self.__berlesek.remove(berles)
                return True
        raise ValueError(
            f"Nincs ilyen berles: rendszam={rendszam}, datum={datum}"
        )

    def berlesek_listazasa(self) -> list[Berles]:
        return list(self.__berlesek)

    def autok_listazasa(self) -> list[Auto]:
        return list(self.__autok)

    def __auto_keresese(self, rendszam: str):
        for auto in self.__autok:
            if auto.rendszam == rendszam:
                return auto
        return None

    def __auto_foglalt_e(self, rendszam: str, datum: date) -> bool:
        for berles in self.__berlesek:
            if berles.auto.rendszam == rendszam and berles.datum == datum:
                return True
        return False

def rendszer_inicializalasa() -> Autokolcsonzo:
    kolcsonzo = Autokolcsonzo("Budapest AutoBerlo Kft.")

    a1 = Szemelyauto("ABC-123", "Toyota Corolla",  12_000, 5)
    a2 = Szemelyauto("XYZ-456", "BMW 3-as",        25_000, 5)
    a3 = Teherauto("TRK-789",  "Mercedes Sprinter", 35_000, 1500)

    for auto in (a1, a2, a3):
        kolcsonzo.auto_hozzaadasa(auto)

    today = date.today()
    adatok = [
        ("ABC-123", "Kiss Peter",  today + timedelta(days=1)),
        ("XYZ-456", "Nagy Anna",   today + timedelta(days=2)),
        ("TRK-789", "Szabo Gabor", today + timedelta(days=3)),
        ("ABC-123", "Toth Maria",  today + timedelta(days=5)),
    ]
    for rendszam, nev, datum in adatok:
        kolcsonzo.auto_berlese(rendszam, nev, datum)

    return kolcsonzo

SEP = "-" * 60

def vonal():
    print(SEP)

def fejlec(cim: str):
    vonal()
    print(f"  {cim}")
    vonal()

def siker(uzenet: str):
    print(f"\n  [SIKER] {uzenet}")
    enter_folytatas()

def hiba(uzenet: str):
    print(f"\n  [HIBA] {uzenet}")
    enter_folytatas()

def enter_folytatas():
    input("\n  Nyomjon Entert a folytatáshoz...")

def beolvas(felirat: str) -> str:
    while True:
        ertek = input(f"  {felirat}: ").strip()
        if ertek:
            return ertek
        print("  Ez a mezo nem maradhat ures.")

def flotta_tabla(kolcsonzo: Autokolcsonzo):
    autok = kolcsonzo.autok_listazasa()
    if not autok:
        print("  Nincs auto a rendszerben.")
        return
    print(f"  {'#':<4} {'Rendszam':<12} {'Leiras':<40} {'Dij (Ft/nap)':>12}")
    vonal()
    for i, a in enumerate(autok, 1):
        print(f"  {i:<4} {a.rendszam:<12} {a.leiras():<40} {a.berleti_dij:>12,.0f}")
    vonal()


def berles_tabla(kolcsonzo: Autokolcsonzo) -> list[tuple[int, Berles]]:
    berlesek = kolcsonzo.berlesek_listazasa()
    if not berlesek:
        print("\n  Jelenleg nincs aktiv berles.\n")
        return []

    today = date.today()
    print(f"  {'#':<4} {'Berlo':<20} {'Rendszam':<12} {'Datum':<14} {'Dij (Ft)':>10}")
    vonal()
    sorok = []
    for i, b in enumerate(berlesek, 1):
        days = (b.datum - today).days
        if days == 1:
            datum_str = f"{b.datum} (holnap)"
        elif days <= 3:
            datum_str = f"{b.datum} ({days} nap mulva)"
        else:
            datum_str = str(b.datum)
        print(f"  {i:<4} {b.berlo_neve:<20} {b.auto.rendszam:<12} {datum_str:<14} {b.ar():>10,.0f}")
        sorok.append((i, b))
    vonal()
    return sorok

def datum_valaszto(cim: str = "Valasszon datumot") -> date | None:
    """
    Dátum bekérése YYYY-MM-DD formátumban, vagy üres = mégse.
    """
    print(f"\n  {cim}")
    print(f"  (Formatum: YYYY-MM-DD, pl. {date.today() + timedelta(days=1)}  |  ures = vissza)")
    while True:
        ertek = input("  Datum: ").strip()
        if not ertek:
            return None
        try:
            d = date.fromisoformat(ertek)
        except ValueError:
            print("  Ervenytelen formatum. Kerem YYYY-MM-DD alakban adja meg.")
            continue
        if d < date.today():
            print("  Multbeli datum nem valaszthato.")
            continue
        return d

def kepernyo_berlese(kolcsonzo: Autokolcsonzo):
    fejlec("Auto berlese")
    flotta_tabla(kolcsonzo)

    autok = kolcsonzo.autok_listazasa()
    auto_map = {a.rendszam: a for a in autok}

    rendszam = None
    while True:
        valasz = beolvas("Auto sorszama vagy rendszama").upper()
        if valasz.isdigit():
            idx = int(valasz) - 1
            if 0 <= idx < len(autok):
                rendszam = autok[idx].rendszam
                break
            else:
                print(f"  Hiba: Ervenytelen sorszam. Valasszon 1 es {len(autok)} kozott.")
        elif valasz in auto_map:
            rendszam = valasz
            break
        else:
            print(f"  Hiba: Nem talalhato auto '{valasz}' rendszammal.")

    berlo = beolvas("Berlo neve")

    datum = datum_valaszto(f"Mikor szeretne berelni? ({rendszam})")
    if datum is None:
        return

    try:
        ar = kolcsonzo.auto_berlese(rendszam, berlo, datum)
        siker(f"{rendszam} sikeresen berelve | {datum} | Fizetendo: {ar:,.0f} Ft")
    except ValueError as e:
        hiba(str(e))


def kepernyo_lemondas(kolcsonzo: Autokolcsonzo):
    fejlec("Berles lemondasa")
    sorok = berles_tabla(kolcsonzo)
    if not sorok:
        enter_folytatas()
        return

    print("  Irja be a lemondani kivant berles sorszamat, vagy 0 = vissza.")
    while True:
        try:
            valasz = int(input("  Sorszam: ").strip())
        except ValueError:
            print("  Kerem szamot adjon meg.")
            continue
        if valasz == 0:
            return
        if 1 <= valasz <= len(sorok):
            _, kivalasztott = sorok[valasz - 1]
            break
        print(f"  Ervenytelen sorszam. Kerem 1 es {len(sorok)} kozott.")

    print(
        f"\n  Biztosan lemondja?  {kivalasztott.berlo_neve}  |  "
        f"{kivalasztott.auto.rendszam}  |  {kivalasztott.datum}"
    )
    megerosit = input("  Megerosites (i = igen, barmi mas = vissza): ").strip().lower()

    if megerosit != "i":
        print("  Lemondas megszakitva.")
        enter_folytatas()
        return

    try:
        kolcsonzo.berles_lemondasa(kivalasztott.auto.rendszam, kivalasztott.datum)
        siker("A berles sikeresen lemondva.")
    except ValueError as e:
        hiba(str(e))


def kepernyo_berlesek(kolcsonzo: Autokolcsonzo):
    fejlec("Aktualis berlesek")
    berles_tabla(kolcsonzo)
    enter_folytatas()


def kepernyo_flotta(kolcsonzo: Autokolcsonzo):
    fejlec("Flotta")
    flotta_tabla(kolcsonzo)
    enter_folytatas()

MENU_ITEMS = [
    ("1", "Auto berlese"),
    ("2", "Berles lemondasa"),
    ("3", "Berlesek listazasa"),
    ("4", "Flotta megtekintese"),
    ("0", "Kilepes"),
]

def menu_kiir(kolcsonzo: Autokolcsonzo):
    vonal()
    print(f"  {kolcsonzo.nev}  |  Mai nap: {date.today()}")
    vonal()
    for key, label in MENU_ITEMS:
        print(f"  [{key}]  {label}")
    vonal()

def valaszt() -> str:
    ervenyes = {k for k, _ in MENU_ITEMS}
    while True:
        valasz = input("  Valasszon: ").strip()
        if valasz in ervenyes:
            return valasz
        print(f"  Ervenytelen valasz. Lehetosegek: {', '.join(sorted(ervenyes))}")


def main():
    kolcsonzo = rendszer_inicializalasa()

    while True:
        menu_kiir(kolcsonzo)
        valasz = valaszt()

        if valasz == "1":
            kepernyo_berlese(kolcsonzo)
        elif valasz == "2":
            kepernyo_lemondas(kolcsonzo)
        elif valasz == "3":
            kepernyo_berlesek(kolcsonzo)
        elif valasz == "4":
            kepernyo_flotta(kolcsonzo)
        elif valasz == "0":
            print("\n  Viszlat!\n")
            break


if __name__ == "__main__":
    main()