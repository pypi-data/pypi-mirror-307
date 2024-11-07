from typing import Any, ClassVar, Self, override, Type
from abc import ABC, abstractmethod
from pathlib import Path
import re
from functools import reduce
import json

import pandas as pd
import matplotlib
matplotlib.use("Agg") # Use a non-GUI backend
import matplotlib.pyplot as plt
import numpy as np

from psychoanalyst.common_data import CommonData
from psychoanalyst.specifications import Specification, ExamSpecification, ComparativeSpecification, StructureError
from psychoanalyst.loaders import DummyLoader, CsvLoader, SqliteLoader, LoadError
from psychoanalyst.savers import DummySaver, CsvSaver, SqliteSaver, SaveError

class AnalysisPipeline[T:Specification](ABC):
    analysis_options: ClassVar[dict[str,str]] = {}
    """"
        A dictionary of:
        key:    configuration option name
        value:  description of what the configuration does/means
    """
    analysis_configurations: ClassVar[dict[str,Any]] = {}
    """The configurations used for the analysis options"""
    specification: ClassVar[T] # type: ignore
    _instances: ClassVar[dict[Type[Self],Self]] = dict()
    def __new__(cls) -> Self:
        if not cls._instances.get(cls, None):
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]
    def __init__(self) -> None:
        self.table: pd.DataFrame = None # type: ignore
        self.analyzed: dict[str, Any] = dict()
    @abstractmethod
    def _cleaning(self) -> None: ...
    @abstractmethod
    def _transformation(self) -> None: ...
    @abstractmethod
    def _analysis(self) -> None: ...
    @abstractmethod
    def _graph(self) -> None: ...
    @abstractmethod
    def main(self) -> dict[str, Any]: ...
    def save_json(self):
        if not CommonData.json_path.parent.exists():
            try:
                CommonData.json_path.parent.mkdir(parents=True)
            except PermissionError:
                CommonData.exception_reporter(
                    SaveError(f"Directory: {CommonData.json_path.parent} cannot be created")
                )
        with open(CommonData.json_path.with_stem(self.__class__.__name__), "w", encoding="utf-8") as f:
            json.dump(self.analyzed, f)
    @classmethod
    def set_configuration(cls, config: dict[str,Any]):
        cls.analysis_configurations = config


class CommonAnalysisPipeline(AnalysisPipeline[ExamSpecification]):
    """An implementation of Analysis Pipeline, any subclass will be loaded with some common methods/data for analysis"""
    _loaded_additional_data_flag: ClassVar[bool] = False
    """The first time _load_additional_data is called this flag should be set, implying that it tried to load the additional data"""
    _additional_data_table: ClassVar[pd.DataFrame|None] = None
    """Data that should be stored in every analyzed table"""
    _additional_data_columns: ClassVar[list[str]] = []
    """The columns of the data that should be stored in every analyzed table, used for joins/merges"""
    _conversion_table: ClassVar[Path] = Path(__file__).parent / "conversion_tables" / "default.csv"
    specification: ClassVar[ExamSpecification]
    loader = CsvLoader()
    saver = CsvSaver()

    @staticmethod
    def _load_personal_data() -> None:
        data = DatosPersonales()
        data.main()
        if data.table is not None:
            CommonAnalysisPipeline._additional_data_table = data.table
            CommonAnalysisPipeline._additional_data_columns = data._additional_data_columns
            CommonData.progress_reporter(f"Se cargaron los datos personales")

    def _load_additional_data(self) -> None:
        if not CommonAnalysisPipeline._loaded_additional_data_flag:
            CommonAnalysisPipeline._loaded_additional_data_flag = True
            self._load_personal_data()
        if CommonAnalysisPipeline._additional_data_table is None:
            return
        self.table = self.table.join(CommonAnalysisPipeline._additional_data_table, how="outer")
        self.table.set_index(CommonAnalysisPipeline._additional_data_columns, append=True, inplace=True)

    @override
    def _cleaning(self) -> None:
        questions_columns = list(range(1, self.specification.num_questions+1))
        # Calculate Incompleteness
        self.table[f"Incompletitud {self.specification.identifier}"] = (
            (self.table[questions_columns].isna()).sum(axis=1) # Number of not completed questions
            /self.specification.num_questions
            *100
        ).round(2)
        # Replace not completed questions for 0 so they don"t affect the result
        self.table.fillna(0, inplace=True)
        try:
            self.table = self.table.astype("float")
        except ValueError:
            # Something different from "-" or a number was in the table
            raise StructureError("Las respuestas contienen datos extraños, recuerda usar `-` para marcar las preguntas no contestadas todo lo demás debe ser un numero")

    @override
    def _transformation(self) -> None:
        # Once the transformations are completed delete answers
        self.table.drop(columns=range(1,self.specification.num_questions+1), inplace=True)

    @override
    def _analysis(self) -> None:
        normalized: dict[
            float, # percentage of incompleteness
            int # number of persons with that percentage of incompleteness
        ] = self.table[f"Incompletitud {self.specification.identifier}"].value_counts().to_dict()
        self.analyzed[f"Incompletitud {self.specification.identifier}"] = normalized

    def _graph_incompleteness(self) -> None:
        pat = "^Incompletitud"
        incompleteness_keys = [ s for s in self.analyzed.keys() if re.match(pat, s) ]
        if not len(incompleteness_keys):
            return
        TOTAL: int = sum(self.analyzed[incompleteness_keys[0]].values())

        fig, ax = plt.subplots(layout="constrained", figsize=(10, 5))
        labels = [
            "<21%",
            "<41%",
            "<61%",
            "<81%",
            "<=100%"
        ]
        # Quintiles labels
        quintiles = {
            test: [
                sum(
                    quantity for 
                        percentage, # Percentage of incompletitud
                        quantity  # Persons with that percentage
                    in self.analyzed[test].items()
                    if (Q - 21) <= percentage < Q
                )/TOTAL*100
                for Q in (21,41,61,81,101)
            ]
            for test in incompleteness_keys
        }
        y_labels = list(quintiles.keys())
        data = np.array(list(quintiles.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = [
            [0.25, 0.60, 0.25, 1.],
            [0.70, 0.85, 0.50, 1.],
            [1.00, 1.00, 0.75, 1.],
            [1.00, 0.70, 0.40, 1.],
            [0.90, 0.30, 0.20, 1.],
        ]

        ax.invert_yaxis()
        ax.set_xlim(0, 100)

        for i, (colname, color) in enumerate(zip(labels, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(y_labels, widths, left=starts, height=0.5, label=colname, color=color)

        ax.set_title("Distribución del % de incompletitud en Quintiles")
        ax.grid(axis="x", color="0.8")
        fig.legend(ncols=len(labels), loc="outside lower center", fontsize="small")
        fig.savefig(CommonData.figures_path.with_stem(f"Incompletitud {self.specification.identifier}"))

    def _graph_alert(self) -> None:
        fig, ax = plt.subplots(layout="constrained", figsize=(10, 5))
        pat = "^%Alert"
        alerts = {
            key: [100-value, value]
            for key, value in self.analyzed.items() if re.match(pat, key)
        }
        if not len(alerts):
            return
        labels = ("OK", "Alert")
        y_labels = list(alerts.keys())
        data = np.array(list(alerts.values()))
        data_cum = data.cumsum(axis=1)
        category_colors = [
            [0.25, 0.60, 0.25, 1.],
            [0.90, 0.30, 0.20, 1.],
        ]

        ax.invert_yaxis()
        ax.set_xlim(0, 100)

        for i, (colname, color) in enumerate(zip(labels, category_colors)):
            widths = data[:, i]
            starts = data_cum[:, i] - widths
            ax.barh(y_labels, widths, left=starts, height=0.5, label=colname, color=color)
        
        ax.set_title("% personas en nivel de aleta")
        ax.grid(axis="x", color="0.8")
        fig.legend(ncols=len(labels), loc="outside lower center", fontsize="small")
        fig.savefig(CommonData.figures_path.with_stem(f"Alerta {self.specification.identifier}"))

    @override
    def _graph(self) -> None:
        if not CommonData.figures_path.parent.exists():
            CommonData.exception_reporter(SaveError(f"Directory: {CommonData.figures_path.parent} not found"))
            try:
                CommonData.figures_path.parent.mkdir(parents=True)
                CommonData.progress_reporter(f"Directory: {CommonData.figures_path.parent} created")
            except PermissionError:
                CommonData.exception_reporter(
                    SaveError(f"Directory: {CommonData.figures_path.parent} cannot be created")
                )
                # Skip graphs
                return
        self._graph_incompleteness()
        self._graph_alert()

    @override
    def main(self) -> dict[str, Any]:
        try:
            self.table = self.loader.load(self.specification)
            self._load_additional_data()
            self._cleaning()
            self._transformation()
            self._analysis()
            self._graph()
            self.saver.save(self.table, self.specification)
            CommonData.progress_reporter(f"Analyzed: {self.specification.identifier}")
        except (LoadError, SaveError, StructureError) as e:
            CommonData.exception_reporter(e)
            self.analyzed[f"message_{self.__class__.__name__}"] = str(e)
            self.table = None # type: ignore
            # In case an error happened clear currently loaded table
        self.save_json()
        return self.analyzed

    def classify_answers(self, clasificador:dict[str, list[int]]):
        """An utility method to classify answers

        Args:
            clasificador (dict[str, list[int]]): A dictionary where keys are columns names and values are lists of integers representing question numbers
        """        
        for name, columns in clasificador.items():
            self.table[name] = self.table[columns].sum(axis=1)


class DatosPersonales(CommonAnalysisPipeline):
    _additional_data_columns: ClassVar[list[str]] = [
        "Código de estudiante",
        "Carrera",
        "Edad"
    ]
    specification = ExamSpecification("datos_personales", 3, 0)
    saver = DummySaver()
    renamer = {
        1: "Código de estudiante",
        2: "Carrera",
        3: "Edad"
    }

    @override
    def _cleaning(self) -> None: return None

    @override
    def _transformation(self) -> None:
        for col, new_name in self.renamer.items():
            self.table[new_name] = self.table[col]
        self.table["Código de estudiante"] = self.table["Código de estudiante"].astype("int")
        self.table.drop(columns=range(1,self.specification.num_questions+1), inplace=True)
        self.table.drop(columns=["Calificación/0"], inplace=True)

    @override
    def _analysis(self) -> None: return None


class ComparisonAnalysisPipeline(AnalysisPipeline[ComparativeSpecification]):
    _loaded_identity_data_flag: ClassVar[bool] = False
    """The first time _load_additional_data is called this flag should be set, implying that it tried to load the additional data"""
    _identity_data_table: ClassVar[pd.DataFrame|None] = None
    """Data that identifies students, should content at least email, since this is used for the join"""
    identity_data_path: ClassVar[Path|None] = None
    specification: ClassVar[ComparativeSpecification]
    index_columns = [
        "Dirección Email"
    ]
    """Index columns used for hashing, if change this should also change on all child
    classes"s specification"""
    means_graph: ClassVar[list[str]]
    """Which columns should be on graph_means"""
    loader = SqliteLoader()
    saver = CsvSaver()
    sql_saver = SqliteSaver()
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def _load_identity_data() -> None:
        if ComparisonAnalysisPipeline.identity_data_path is None:
            CommonData.exception_reporter(LoadError(Exception(
                f"No se encuentra una Identity Table"
            )))
            return
        table = pd.read_csv(ComparisonAnalysisPipeline.identity_data_path)
        valid_table_flag = True
        for col in ComparisonAnalysisPipeline.index_columns:
            if col not in table.columns:
                valid_table_flag = False
                CommonData.exception_reporter(LoadError(Exception(
                    f"Identity Table no tiene la columna {col}"
                )))
                break
        if not valid_table_flag:
            return
        table["hash"] = table[ComparisonAnalysisPipeline.index_columns]\
            .apply(lambda cols: "".join(map(str,cols)).encode(), axis=1)\
            .apply(lambda composed_key: bytes.fromhex(SqliteSaver.hash_algorithm(composed_key).hexdigest()))
        table.set_index("hash", inplace=True)
        ComparisonAnalysisPipeline._identity_data_table = table
        CommonData.progress_reporter("Se cargo Identity Table")

    def _load_additional_data(self) -> None:
        if not ComparisonAnalysisPipeline._loaded_identity_data_flag:
            ComparisonAnalysisPipeline._loaded_identity_data_flag = True
            self._load_identity_data()
        if ComparisonAnalysisPipeline._identity_data_table is None:
            return
        self.table = self.table.join(ComparisonAnalysisPipeline._identity_data_table, how="outer")

    @override
    def _cleaning(self) -> None:
        return None

    @override
    def _transformation(self) -> None:
        analyzed_year = CommonData.year
        analyzed_cycle = CommonData.cycle
        analyzed_semester = CommonData.semester

        # Stablish data for first semester
        while CommonData.semester > 1:
            CommonData.previous_semester()

        self.init_year = CommonData.year
        self.init_cycle = CommonData.cycle

        self.analyzed["means"] = {
            col: list()
            for col in self.specification.compared_columns
        }
        self.analyzed["means_semesters"] = []

        for semester in range(1,analyzed_semester):
            try:
                table = self.loader.load(self.specification)
                self.table = self.table.join(table, how="outer")
                for col, means  in self.analyzed["means"].items():
                    means.append(float(round(table[f"_{semester}_{col}"].mean(), 2)))
                self.analyzed["means_semesters"].append(semester)
            except LoadError:
                CommonData.progress_reporter(f"Not data for semester {semester}")
            CommonData.next_semester()

        for col, means  in self.analyzed["means"].items():
            means.append(float(round(self.table[f"_{analyzed_semester}_{col}"].mean(), 2)))
        self.analyzed["means_semesters"].append(analyzed_semester)

        CommonData.year = analyzed_year
        CommonData.cycle = analyzed_cycle
        CommonData.semester = analyzed_semester

    @override
    def _analysis(self) -> None:
        return None

    def _graph_means(self) -> None:
        x = np.arange(len(self.analyzed["means_semesters"]))*2
        width = 0.10  # the width of the bars
        multiplier = 0
        # 2 / 0.10 = 20, 20 columns max to graph

        fig, ax = plt.subplots(layout="constrained", figsize=(10, 5))
        for attribute in self.means_graph:
            measurement = self.analyzed["means"][attribute]
            offset = width * multiplier
            ax.bar(x + offset, measurement, width, label=attribute)
            multiplier += 1

        ax.set_xticks(x + (width*len(self.means_graph)/2) - width/2, self.analyzed["means_semesters"])
        ax.grid(axis="y", color="0.8")
        ax.set_title(f"Medias generación {self.init_year}{self.init_cycle}-{CommonData.year}{CommonData.cycle} por semestre")
        fig.legend(ncols=len(self.means_graph)//2, loc="outside lower center", fontsize="small")
        fig.savefig(CommonData.figures_path.with_stem(f"Medias {self.specification.identifier}"))

    @override
    def _graph(self) -> None:
        if not CommonData.figures_path.parent.exists():
            CommonData.exception_reporter(SaveError(f"Directory: {CommonData.figures_path.parent} not found"))
            try:
                CommonData.figures_path.parent.mkdir(parents=True)
                CommonData.progress_reporter(f"Directory: {CommonData.figures_path.parent} created")
            except PermissionError:
                CommonData.exception_reporter(
                    SaveError(f"Directory: {CommonData.figures_path.parent} cannot be created")
                )
                # Skip graphs
                return
        self._graph_means()

    def _format(self) -> None:
        self.table["hash"] = self.table.index
        self.table["hash"] = self.table["hash"].apply(bytes.hex)
        self.table.set_index("hash", inplace=True)

    def save_to_sql(self, table: pd.DataFrame) -> None:
        try:
            self.sql_saver.save(table, self.specification)
        except SaveError as e:
            CommonData.exception_reporter(e)

    @override
    def main(self) -> dict[str, Any]:
        try:
            self.table = self.loader.load(self.specification)
            self._load_additional_data()
            self._cleaning()
            self._transformation()
            self._analysis()
            self._graph()
            self._format()
            self.saver.save(self.table, self.specification)
            CommonData.progress_reporter(f"Analyzed: {self.specification.identifier}")
        except (LoadError, SaveError, StructureError) as e:
            CommonData.exception_reporter(e)
            self.analyzed[f"message_{self.__class__.__name__}"] = str(e)
            self.table = None # type: ignore
        self.save_json()
        return self.analyzed