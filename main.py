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
