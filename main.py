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