from abc import ABC, abstractmethod
from typing import override, ClassVar, Type, Self, Any
import sqlite3
from pathlib import Path

import pandas as pd

from psychoanalyst.common_data import CommonData
from psychoanalyst.specifications import Specification, ExamSpecification, ComparativeSpecification, StructureError

class LoadError(Exception):
    """Exception when Loading Data"""

class Loader[T:Specification](ABC):
    """Interface to load/store data"""
    source: ClassVar[Any]
    """From where to load data"""
    _instances: ClassVar[dict[Type[Self],Self]] = dict()
    def __new__(cls) -> Self:
        if not cls._instances.get(cls, None):
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
    @abstractmethod
    def _cleaning(self) -> None: ...
    @abstractmethod
    def _assert_structure(self) -> None: ...
    @abstractmethod
    def load(self, specification: T) -> pd.DataFrame:
        """Loads a table from the source specified by the class

        Args:
            specification (T): The specification of which table in the source to load

        Raises:
            StructureError: If the structure of the table (rows, columns) is not what expected
            LoadError: Problems while trying to load the table

        Returns:
            pd.DataFrame: the table loaded after the cleaning
        """

class DummyLoader(Loader):
    source: ClassVar[pd.DataFrame]
    @override
    def _cleaning(self) -> None: return None
    @override
    def _assert_structure(self) -> None: return None
    def load(self, specification: Any) -> pd.DataFrame:
        return self.source


class CsvLoader(Loader[ExamSpecification]):
    source: ClassVar[Path] = Path.home() / "Exams" / "default.csv"
    metadata_columns = {
        "Apellido(s)",
        "Nombre",
        "Dirección Email",
        "Estado",
        "Comenzado el",
        "Finalizado",
        "Tiempo empleado"
    }
    index_columns = {
        "Apellido(s)",
        "Nombre",
        "Dirección Email",
    }

    def _prepare_answers(self):
        # Enumerate response columns to facilitate answer classification
        renamed = {
            name:number
            for number, name in enumerate(self._table.columns[1:],1)
        }
        self._table.rename(columns=renamed,inplace=True)
        questions_columns = list(renamed.values())
        # Replace missing values with csv structure "-"
        self._table[questions_columns] = self._table[questions_columns].replace({"-":pd.NA})

    @override
    def _cleaning(self) -> None:
        # Drop unused metadata
        unused_cols = list(self.metadata_columns-self.index_columns)
        self._table.drop(columns=unused_cols, inplace=True)
        # Drop summary row
        self._table.drop(index=self._table.tail(1).index, inplace=True)
        self._table.set_index(list(self.index_columns), inplace=True)
        self._prepare_answers()

    @override
    def _assert_structure(self) -> None:
        expected_num_columns = self._specification.num_questions+len(self.metadata_columns)+1
        if self._table.columns.size > expected_num_columns:
            raise StructureError(f"Se encuentran mas columnas de las esperadas, se esperaban {expected_num_columns}")
        if self._table.columns.size < expected_num_columns:
            raise StructureError(f"Se encuentran menos columnas de las esperadas, se esperaban {expected_num_columns}")
        for col in self.metadata_columns:
            if col not in self._table.columns[:len(self.metadata_columns)]:
                raise StructureError(f"No se encuentra la columna con el nombre `{col}`, revise la estructura esperada en las tablas")
        grade_column = f"Calificación/{self._specification.total_grade}"
        if grade_column != self._table.columns[len(self.metadata_columns)]:
            raise StructureError(f"No se encuentra la columna con el nombre `{grade_column}`, revise la estructura esperada en las tablas")

    @override
    def load(self, specification: ExamSpecification) -> pd.DataFrame:
        self._specification = specification
        file = self.source.with_stem(self._specification.identifier)
        if not file.exists():
            raise LoadError(f"Not found {file}")
        self._table = pd.read_csv(file)
        self._assert_structure()
        self._cleaning()
        return self._table

class SqliteLoader(Loader[ComparativeSpecification]):
    source: ClassVar[Path] = Path.home() / "psicoanalisis" / "default.db"
    query = "SELECT * FROM `_{semester}_{identifier}`;"
    @override
    def _cleaning(self) -> None: return None

    @override
    def _assert_structure(self) -> None:
        search = set(map(lambda col: f"_{CommonData.semester}_{col}", self._specification.compared_columns))
        present = set(self._table.columns)
        for col in list(search-present):
            raise StructureError(f"No se encuentra la columna con el nombre {col}")

    @override
    def load(self, specification: ComparativeSpecification) -> pd.DataFrame:
        self._specification = specification
        source = self.source.with_stem(f"{CommonData.year}{CommonData.cycle}")
        if not source.exists():
            raise LoadError(f"Not found {source}")
        with sqlite3.connect(source) as con:
            self._table = pd.read_sql(self.query.format(semester=CommonData.semester, identifier=self._specification.identifier), con, index_col="hash")
        self._assert_structure()
        return self._table