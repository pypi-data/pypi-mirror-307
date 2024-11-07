from typing import Any, override
import operator

import pandas as pd

import psychoanalyst as ps

class RyffAnalysis(ps.CommonAnalysisPipeline):
    analysis_options = {
        "Puntuación BP":        "Cualquier valor inferior se considerara alarmante",
        "Autoaceptación":       "Cualquier valor inferior se considerara alarmante",
        "Dominio del entorno":  "Cualquier valor inferior se considerara alarmante",
        "Relaciones positivas": "Cualquier valor inferior se considerara alarmante",
        "Crecimiento personal": "Cualquier valor inferior se considerara alarmante",
        "Autonomía":            "Cualquier valor inferior se considerara alarmante",
        "Propósito de vida":    "Cualquier valor inferior se considerara alarmante"
    }
    specification = ps.ExamSpecification("Ryff", 39, 234)
    classifier = {
        "Autoaceptación": [1,7,13,19,25,31],
        "Dominio del entorno": [5,11,16,22,28,39],
        "Relaciones positivas": [2,8,14,20,26,32],
        "Crecimiento personal": [24,30,34,35,36,37,38],
        "Autonomía": [3,4,9,10,15,21,27,33],
        "Propósito de vida": [6,12,17,18,23,29]
    }
    def __init__(self) -> None:
        super().__init__()

    @override
    def _transformation(self) -> None:
        self.table.rename(columns={"Calificación/234": "Puntuación BP"}, inplace=True)
        self.classify_answers(self.classifier)
        return super()._transformation()

    @override
    def _analysis(self) -> None:
        super()._analysis()
        interpreter = ps.InterpretationTools.interpreter_fabric(
            operator.ge,
            self.interpreter_table["Nivel BP"],
            self.interpreter_table["Interpretación"],
            ps.InterpretationTools.interpreter_selector_first,
        )
        self.table["Interpretación bienestar psicológico"] = self.table["Puntuación BP"].apply(interpreter)
        counts = self.table["Interpretación bienestar psicológico"].value_counts()
        normalized = dict(map(
            lambda n: (str(n),int(counts.get(n,0))),
            self.interpreter_table["Interpretación"] # Possible interpretations
        ))
        self.analyzed["Interpretación bienestar psicológico"] = normalized
        
        for col in self.classifier.keys():
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table2[col],
                self.interpreter_table2["Interpretación"],
                ps.InterpretationTools.interpreter_selector_first,
                default_value=pd.NA
            )
            self.table[f"Interpretación {col}"] = self.table[col].apply(interpreter)
        
        options = set(self.analysis_options.keys())
        for column in options.intersection(set(self.analysis_configurations.keys())):
            filter = self.table[column] <= self.analysis_configurations[column]
            self.saver.save(self.table[filter][column], ps.Specification[str]("Alert Ryff-"+column))

    @override
    def main(self) -> dict[str,Any]:
        self.interpreter_table = pd.read_csv(self._conversion_table.with_stem("Grado de bienestar psicológico"))
        self.interpreter_table2 = pd.read_csv(self._conversion_table.with_stem("Dominancia"))
        return super().main()