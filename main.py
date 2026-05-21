from abc import ABC, abstractmethod
from datetime import date, timedelta

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.columns import Columns
from rich import box
console = Console()

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

    a1 = Szemelyauto("ABC-123", "Toyota Corolla",   12_000, 5)
    a2 = Szemelyauto("XYZ-456", "BMW 3-as",         25_000, 5)
    a3 = Teherauto ("TRK-789", "Mercedes Sprinter",  35_000, 1500)

    for auto in (a1, a2, a3):
        kolcsonzo.auto_hozzaadasa(auto)

    today = date.today()
    adatok = [
        ("ABC-123", "Kiss Peter",   today + timedelta(days=1)),
        ("XYZ-456", "Nagy Anna",    today + timedelta(days=2)),
        ("TRK-789", "Szabo Gabor",  today + timedelta(days=3)),
        ("ABC-123", "Toth Maria",   today + timedelta(days=5)),
    ]
    for rendszam, nev, datum in adatok:
        kolcsonzo.auto_berlese(rendszam, nev, datum)

    return kolcsonzo

ACCENT  = "bright_cyan"
DIM     = "grey50"
OK      = "green"
ERR     = "red"
WARN    = "yellow"

MENU_ITEMS = [
    ("1", "Auto berlese"),
    ("2", "Berles lemondasa"),
    ("3", "Berlesek listazasa"),
    ("4", "Flotta megtekintese"),
    ("0", "Kilepes"),
]

def clear():
    console.clear()


def header(kolcsonzo: Autokolcsonzo):
    content = Text.assemble(
        Text(kolcsonzo.nev, style="bold bright_white"),
        "\n",
        Text(f"Mai nap: {date.today().isoformat()}", style=DIM),
    )
    console.print(Panel(content, style=ACCENT, padding=(0, 2)))


def siker(uzenet: str):
    console.print(f"\n  [{OK}]Siker:[/{OK}] {uzenet}")
    enter_folytatas()


def hiba(uzenet: str):
    console.print(f"\n  [{ERR}]Hiba:[/{ERR}] {uzenet}")
    enter_folytatas()


def enter_folytatas():
    Prompt.ask(f"\n  [{DIM}]Nyomjon Entert a folytatáshoz[/{DIM}]", default="")


def beolvas(felirat: str) -> str:
    while True:
        ertek = Prompt.ask(f"  [{ACCENT}]{felirat}[/{ACCENT}]").strip()
        if ertek:
            return ertek
        console.print(f"  [{WARN}]Ez a mezo nem maradhat ures.[/{WARN}]")

NAPOK  = ["H", "K", "Sz", "Cs", "P", "Sz", "V"]
HONAPOK = ["", "jan", "feb", "mar", "apr", "maj", "jun",
           "jul", "aug", "sze", "okt", "nov", "dec"]


def _honap_napjai(ev: int, honap: int) -> int:
    if honap == 12:
        return (date(ev + 1, 1, 1) - date(ev, 12, 1)).days
    return (date(ev, honap + 1, 1) - date(ev, honap, 1)).days


def datum_valaszto(cim: str = "Valasszon datumot") -> date | None:
    """
    havi naptár.
    L/J: nap  |  N/P: hónap  |  Enter: választ  |  X: mégse
    """
    kivalasztott = date.today() + timedelta(days=1)

    while True:
        clear()
        console.print(Panel(f"[bold]{cim}[/bold]", style=ACCENT, padding=(0, 2)))
        _naptar_rajzol(kivalasztott)
        console.print(
            f"\n  [{DIM}]"
            f"L/J = nap    N/P = honap    Enter = valaszt    X = vissza"
            f"[/{DIM}]"
        )

        parancs = Prompt.ask(f"\n  [{ACCENT}]Navigacio[/{ACCENT}]", default="").strip().upper()

        ev, h, nap = kivalasztott.year, kivalasztott.month, kivalasztott.day
        max_nap = _honap_napjai(ev, h)

        if parancs in ("", "ENTER"):
            if kivalasztott < date.today():
                console.print(f"  [{WARN}]Multbeli datum nem valaszthato.[/{WARN}]")
                enter_folytatas()
                continue
            return kivalasztott

        elif parancs == "X":
            return None

        elif parancs == "L":
            kivalasztott -= timedelta(days=1)

        elif parancs == "J":
            kivalasztott += timedelta(days=1)

        elif parancs == "N":
            if h == 1:
                kivalasztott = date(ev - 1, 12, min(nap, _honap_napjai(ev - 1, 12)))
            else:
                kivalasztott = date(ev, h - 1, min(nap, _honap_napjai(ev, h - 1)))

        elif parancs == "P":
            if h == 12:
                kivalasztott = date(ev + 1, 1, min(nap, _honap_napjai(ev + 1, 1)))
            else:
                kivalasztott = date(ev, h + 1, min(nap, _honap_napjai(ev, h + 1)))

        else:
            try:
                szam = int(parancs)
                if 1 <= szam <= max_nap:
                    kivalasztott = date(ev, h, szam)
                else:
                    console.print(f"  [{WARN}]Ervenytelen nap: {szam}[/{WARN}]")
            except ValueError:
                console.print(f"  [{WARN}]Ismeretlen parancs.[/{WARN}]")


def _naptar_rajzol(kivalasztott: date):
    ev, h = kivalasztott.year, kivalasztott.month
    max_nap = _honap_napjai(ev, h)
    today = date.today()

    console.print()
    console.print(f"    [bold bright_white]{HONAPOK[h].upper()} {ev}[/bold bright_white]")
    console.print()

    fejlec = Text("   ")
    for nev in NAPOK:
        fejlec.append(f" {nev}  ", style=DIM)
    console.print(fejlec)
    console.print()

    elso = date(ev, h, 1).weekday()   # 0=H … 6=V
    aktualis_nap = 1

    while aktualis_nap <= max_nap:
        sor = Text("   ")

        if aktualis_nap == 1:
            sor.append("    " * elso)

        while aktualis_nap <= max_nap:
            nap_datum = date(ev, h, aktualis_nap)
            het_napja = nap_datum.weekday()
            szam = f"{aktualis_nap:2d} "

            if nap_datum == kivalasztott:
                sor.append(f" {szam}", style="bold black on bright_cyan")
            elif nap_datum == today:
                sor.append(f" {szam}", style=f"bold {WARN}")
            elif nap_datum < today:
                sor.append(f" {szam}", style=DIM)
            else:
                sor.append(f" {szam}", style="white")

            aktualis_nap += 1
            if het_napja == 6:
                break

        console.print(sor)

    console.print()
    console.print(
        f"  Kivalasztva: [bold {ACCENT}]{kivalasztott.isoformat()}[/bold {ACCENT}]"
    )
def _flotta_tabla(kolcsonzo: Autokolcsonzo):
    autok = kolcsonzo.autok_listazasa()
    if not autok:
        console.print(f"  [{DIM}]Nincs auto a rendszerben.[/{DIM}]")
        return

    t = Table(box=box.SIMPLE_HEAVY, show_header=True,
              header_style=f"bold {ACCENT}", show_edge=True, padding=(0, 1))
    t.add_column("#",             style=DIM,         justify="right", width=3)
    t.add_column("Rendszam",      style="bold white")
    t.add_column("Leiras",        style="white")
    t.add_column("Dij (Ft/nap)", style=ACCENT,       justify="right")

    for i, a in enumerate(autok, 1):
        t.add_row(str(i), a.rendszam, a.leiras(), f"{a.berleti_dij:,.0f}")

    console.print(t)
def _berles_tabla(kolcsonzo: Autokolcsonzo) -> list[tuple[int, "Berles"]]:
    """Kirajzolja a bérlés táblát, visszaadja a sorszám->Berles párosokat."""
    berlesek = kolcsonzo.berlesek_listazasa()
    if not berlesek:
        console.print(f"\n  [{DIM}]Jelenleg nincs aktiv berles.[/{DIM}]\n")
        return []

    t = Table(box=box.SIMPLE_HEAVY, show_header=True,
              header_style=f"bold {ACCENT}", show_edge=True, padding=(0, 1))
    t.add_column("#",        style=DIM,        justify="right", width=3)
    t.add_column("Berlo",    style="bold white")
    t.add_column("Rendszam", style="white")
    t.add_column("Datum",    style="white")
    t.add_column("Dij (Ft)", style=ACCENT,     justify="right")

    today = date.today()
    sorok = []
    for i, b in enumerate(berlesek, 1):
        days = (b.datum - today).days
        if days == 1:
            datum_str = f"[{OK}]{b.datum}  (holnap)[/{OK}]"
        elif days <= 3:
            datum_str = f"[{WARN}]{b.datum}  ({days} nap mulva)[/{WARN}]"
        else:
            datum_str = str(b.datum)

        t.add_row(str(i), b.berlo_neve, b.auto.rendszam, datum_str, f"{b.ar():,.0f}")
        sorok.append((i, b))

    console.print(t)
    return sorok

def kepernyo_berlese(kolcsonzo: Autokolcsonzo):
    clear()
    console.print(Panel("[bold]Auto berlese[/bold]", style=ACCENT, padding=(0, 2)))
    _flotta_tabla(kolcsonzo)
    console.print(f"  [grey50]Valasszon sorszam (pl. 1) vagy rendszam (pl. ABC-123) alapjan.[/grey50]")
    console.print()

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
                console.print(f"  [red]Hiba:[/red] Ervenytelen sorszam. Valasszon 1 es {len(autok)} kozott.")
        elif valasz in auto_map:
            rendszam = valasz
            break
        else:
            console.print(f"  [red]Hiba:[/red] Nem talalhato auto [bold]{valasz!r}[/bold] rendszammal.")

    berlo = beolvas("Berlo neve")

    datum = datum_valaszto(f"Mikor szeretne berelni? ({rendszam})")
    if datum is None:
        return   # visszalepett

    try:
        ar = kolcsonzo.auto_berlese(rendszam, berlo, datum)
        siker(f"{rendszam} sikeresen berelve  |  {datum}  |  Fizetendo: [bold]{ar:,.0f} Ft[/bold]")
    except ValueError as e:
        hiba(str(e))
def kepernyo_lemondas(kolcsonzo: Autokolcsonzo):
    clear()
    console.print(Panel("[bold]Berles lemondasa[/bold]", style=ACCENT, padding=(0, 2)))

    sorok = _berles_tabla(kolcsonzo)
    if not sorok:
        enter_folytatas()
        return

    console.print(f"\n  [{DIM}]Irja be a lemondani kivant berles sorszamat, vagy 0 = vissza.[/{DIM}]")

    while True:
        valasz = IntPrompt.ask(f"  [{ACCENT}]Sorszam[/{ACCENT}]")
        if valasz == 0:
            return
        if 1 <= valasz <= len(sorok):
            _, kivalasztott = sorok[valasz - 1]
            break
        console.print(f"  [{WARN}]Ervenytelen sorszam. Kerem 1 es {len(sorok)} kozott.[/{WARN}]")

    console.print(
        f"\n  Biztosan lemondja?  "
        f"[bold]{kivalasztott.berlo_neve}[/bold]  |  "
        f"[bold]{kivalasztott.auto.rendszam}[/bold]  |  "
        f"[bold]{kivalasztott.datum}[/bold]"
    )
    megerosit = Prompt.ask(
        f"  [{WARN}]Megerosites (i = igen, barmi mas = vissza)[/{WARN}]",
        default="n"
    ).strip().lower()

    if megerosit != "i":
        console.print(f"  [{DIM}]Lemondas megszakitva.[/{DIM}]")
        enter_folytatas()
        return

    try:
        kolcsonzo.berles_lemondasa(kivalasztott.auto.rendszam, kivalasztott.datum)
        siker("A berles sikeresen lemondva.")
    except ValueError as e:
        hiba(str(e))


def kepernyo_berlesek(kolcsonzo: Autokolcsonzo):
    clear()
    console.print(Panel("[bold]Aktualis berlesek[/bold]", style=ACCENT, padding=(0, 2)))
    _berles_tabla(kolcsonzo)
    enter_folytatas()


def kepernyo_flotta(kolcsonzo: Autokolcsonzo):
    clear()
    console.print(Panel("[bold]Flotta[/bold]", style=ACCENT, padding=(0, 2)))
    _flotta_tabla(kolcsonzo)
    enter_folytatas()

def menu_panel():
    t = Table.grid(padding=(0, 3))
    t.add_column(style=f"bold {ACCENT}", justify="right")
    t.add_column(style="white")
    for key, label in MENU_ITEMS:
        t.add_row(f"[{key}]", label)
    console.print(Panel(t, title="[bold]Menu[/bold]", style=DIM, padding=(1, 3)))


def valaszt() -> str:
    return Prompt.ask(
        f"\n  [{ACCENT}]Valasszon[/{ACCENT}]",
        choices=[k for k, _ in MENU_ITEMS],
        show_choices=False,
    )


def main():
    kolcsonzo = rendszer_inicializalasa()

    while True:
        clear()
        header(kolcsonzo)
        console.print()
        menu_panel()

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
            clear()
            console.print(Panel(
                Text("Viszlat!", style="bold bright_white", justify="center"),
                style=ACCENT, padding=(1, 4)
            ))
            break


if __name__ == "__main__":
    main()
