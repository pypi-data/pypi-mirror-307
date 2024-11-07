import operator
from typing import Any, override

import pandas as pd

import psychoanalyst as ps

class CategoriaInterpretativaAnalysis(ps.CommonAnalysisPipeline):
    analysis_options = {
        "Puntuación estándar": "Cualquier valor inferior se considerara alarmante",
    }
    specification = ps.ExamSpecification("Categoría interpretativa", 0, 0)

    class Abstraccion(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Abstracción", 25, 25)

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/25": "Abstracción"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            ages = [(17,19),(20,29),(30,39),(40,49),(50,59),(60,69),(70,79)]
            self.table["Puntuación estándar abstracción"] = pd.NA
            if "edad" not in self.table.index.names:
                raise ps.StructureError("No se puede obtener la Puntuación Estándar sin la edad")
            age = self.table.index.get_level_values("edad")
            for min_age, max_age in ages:
                interpreter = ps.InterpretationTools.interpreter_fabric(
                    operator.ge,
                    self.interpreter_table[f"{min_age}-{max_age}"],
                    self.interpreter_table["Puntuación estándar"],
                    ps.InterpretationTools.interpreter_selector_max,
                    pd.NA
                )
                filter = (min_age <= age) & (age <= max_age)
                self.table.loc[filter,"Puntuación estándar abstracción"] = self.table[filter]["Abstracción"].apply(interpreter)
            return super()._analysis()

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = pd.read_csv(self._conversion_table.with_stem("Abstracción"))
            return super().main()

    class Vocabulario(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Vocabulario", 40, 40)

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/40":"Vocabulario"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            ages = [(17,19),(20,29),(30,39),(40,49),(50,59),(60,69),(70,79)]
            self.table["Puntuación estándar vocabulario"] = pd.NA
            if "edad" not in self.table.index.names:
                raise ps.StructureError("No se puede obtener la Puntuación Estándar sin la edad")
            age = self.table.index.get_level_values("edad")
            for min_age, max_age in ages:
                interpreter = ps.InterpretationTools.interpreter_fabric(
                    operator.ge,
                    self.interpreter_table[f"{min_age}-{max_age}"],
                    self.interpreter_table["Puntuación estándar"],
                    ps.InterpretationTools.interpreter_selector_max,
                    pd.NA
                )
                filter = (min_age <= age) & (age <= max_age)
                self.table.loc[filter,"Puntuación estándar vocabulario"] = self.table[filter]["Vocabulario"].apply(interpreter)
            return super()._analysis()

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = pd.read_csv(self._conversion_table.with_stem("Vocabulario"))
            return super().main()

    @override
    def _load_additional_data(self) -> None:
        return None

    def _cleaning(self):
        self.table = self.table.join(self.vocabulario, how="outer")

    def _transformation(self) -> None:
        self.table["Combinación A"] = self.table["Puntuación estándar abstracción"] + self.table["Puntuación estándar vocabulario"]

    def _analysis(self) -> None:
        ages = [(17,19),(20,29),(30,39),(40,49),(50,59),(60,69),(70,79)]
        self.table["Puntuación estándar"] = pd.NA
        age = self.table.index.get_level_values("edad")
        for min_age, max_age in ages:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table[f"{min_age}-{max_age}"],
                self.interpreter_table["Puntuación estándar"],
                ps.InterpretationTools.interpreter_selector_max,
                pd.NA
            )
            filter = (min_age <= age) & (age <= max_age)
            self.table.loc[filter,"Puntuación estándar"] = self.table[filter]["Combinación A"].apply(interpreter)

        interpreter = ps.InterpretationTools.interpreter_fabric(
            operator.ge,
            self.interpreter_table2["Puntuación estándar"],
            self.interpreter_table2["Interpretación"],
            ps.InterpretationTools.interpreter_selector_first,
            pd.NA
        )
        self.table["Categoría interpretativa"] = self.table["Puntuación estándar"].apply(interpreter)

    def main(self) -> dict[str, Any]:
        analyzed = dict()

        abstraccion = self.Abstraccion()
        analyzed.update(abstraccion.main())
        self.abstraccion = abstraccion.table

        vocabulario = self.Vocabulario()
        analyzed.update(vocabulario.main())
        self.vocabulario = vocabulario.table

        if any(map(lambda x: "message" in x, analyzed.keys())):
            self.analyzed[f"message_{self.__class__.__name__}"] = "Uno de los exámenes previos fallo"
            return self.analyzed
        
        self.interpreter_table = pd.read_csv(self._conversion_table.with_stem("Combinación A"))
        self.interpreter_table2 = pd.read_csv(self._conversion_table.with_stem("Categoría interpretativa"))
        
        ps.DummyLoader.source = abstraccion.table
        return super().main()