

from abc import ABC, abstractmethod
from typing import override, ClassVar, Type, Self
import sqlite3
import hashlib
from pathlib import Path

import pandas as pd

from psychoanalyst.common_data import CommonData
from psychoanalyst.specifications import Specification, ExamSpecification, ComparativeSpecification, StructureError


class SaveError(Exception):
    """Exception when Saving Data"""


class Saver[T:Specification](ABC):
    destiny: ClassVar
    """Where to store data"""
    _instances: ClassVar[dict[Type[Self],Self]] = dict()
    def __new__(cls) -> Self:
        if not cls._instances.get(cls, None):
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
    @abstractmethod
    def _prepare_destiny(self) -> None:...
    @abstractmethod
    def _prepare_data(self) -> None: ...
    @abstractmethod
    def save(self, table: pd.DataFrame, specification: T) -> None: 
        """Saves the table on the destiny specified by the class using the given specification

        Args:
            table (pd.DataFrame): Table to save
            specification (T): Specification on how to save the table

        Raises:
            SaveError: A Problem while trying to save the table
        """


class DummySaver(Saver):
    @override
    def _prepare_destiny(self) -> None: return None
    @override
    def _prepare_data(self) -> None: return None
    @override
    def save(self, table: pd.DataFrame, specification) -> None: ...


class CsvSaver(Saver[Specification[str]]):
    destiny: ClassVar[Path] = Path.home() / "Results" / "default.csv"
    @override
    def _prepare_destiny(self) -> None:
        if self._destiny.parent.exists():
            return
        CommonData.exception_reporter(SaveError(f"Directory: {self._destiny.parent} not found"))
        try:
            self._destiny.parent.mkdir(parents=True)
            CommonData.progress_reporter(f"Directory: {self._destiny.parent} created")
        except PermissionError:
            raise SaveError(f"Directory: {self._destiny.parent} cannot be created")

    @override
    def _prepare_data(self) -> None: ...
    @override
    def save(self, table: pd.DataFrame, specification: Specification[str]) -> None:
        self._destiny = self.destiny.with_stem(specification.identifier)
        self._prepare_destiny()
        table.to_csv(self._destiny)


class SqliteSaver(Saver[ComparativeSpecification]):
    destiny: ClassVar[Path] = Path.home() / "psicoanalisis" / "default.db"
    hash_algorithm = hashlib.sha3_256

    @override
    def _prepare_destiny(self) -> None:
        if self.destiny.parent.exists():
            return
        CommonData.exception_reporter(SaveError(f"Directory: {self.destiny.parent} not found"))
        try:
            self.destiny.parent.mkdir(parents=True)
            CommonData.progress_reporter(f"Directory: {self.destiny.parent} created")
        except PermissionError:
            raise SaveError(f"Directory: {self.destiny.parent} cannot be created")

    @override
    def _prepare_data(self) -> None:
        not_present = list(set(self._specification.compared_columns) - set(self._table.columns))
        if len(not_present):
            raise SaveError(f"No se encuentran las columnas {not_present}")
        unused = list(set(self._table.columns) - set(self._specification.compared_columns))
        self._table.drop(columns=unused, inplace=True)
        self._table["hash"] = self._table.index.to_frame()[self._specification.index_columns]\
            .apply(lambda cols: "".join(map(str,cols)).encode(), axis=1)\
            .apply(lambda composed_key: bytes.fromhex(self.hash_algorithm(composed_key).hexdigest()))
        self._table.set_index("hash", inplace=True)
        self._table.rename(columns={
            col: f"_{CommonData.semester}_{col}"
            for col in self._table.columns
        }, inplace=True)

    @override
    def save(self, table: pd.DataFrame, specification: ComparativeSpecification) -> None:
        self._table = table
        self._specification = specification
        self._prepare_destiny()
        self._prepare_data()
        with sqlite3.connect(self.destiny.with_stem(f"{CommonData.year}{CommonData.cycle}")) as con:
            self._table.to_sql(f"_{CommonData.semester}_{specification.identifier}", con, if_exists="replace")