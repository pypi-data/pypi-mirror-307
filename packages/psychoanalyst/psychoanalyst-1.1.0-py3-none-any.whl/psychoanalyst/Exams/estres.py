import operator
from typing import Any, override

import pandas as pd

import psychoanalyst as ps

class EstresAnalysis(ps.CommonAnalysisPipeline):
    analysis_options = {
        "Estrés-T":             "Cualquier valor superior se considerara alarmante",
        "ARC-T":                "Cualquier valor superior se considerara alarmante",
        "Conducta tipo A-T":    "Cualquier valor superior se considerara alarmante",
        "Valoración negativa-T":"Cualquier valor superior se considerara alarmante",
        
        "Hábitos de salud-T":       "Cualquier valor inferior se considerara alarmante",
        "Bienestar psicológico-T":  "Cualquier valor inferior se considerara alarmante",
    }
    interpreter_table: pd.DataFrame
    specification = ps.ExamSpecification("Estrés", 0, 0)
    loader = ps.DummyLoader()

    @staticmethod
    def detect_inconsistencies(table: pd.DataFrame, inconsistencies: list[tuple[int,int]], exam: str):
        table[f"Inconsistencias {exam}"] = 0
        for q1, q2 in inconsistencies:
            table[f"Inconsistencias {exam}"] += (abs(table[q1] - table[q2]) > 1)

    class Estres_1(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_1", 6, 30)

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/30": "Estrés"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["Estrés"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_max,
            )
            self.table["Estrés-T"] = self.table["Estrés"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_2(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_2", 25, 125)
        classifier = {
            "Ejercicio":[1,2,3],
            "Descanso sueño":[4,5,6,7,8],
            "Prevención":[9,10,11,12,13,14,21,22,23,24,25],
            "Alimentación nutrición":[16,17,18,19,20],
            "ARC":[23,24,25]
        }

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/125":"Hábitos de salud"}, inplace=True)
            self.classify_answers(self.classifier)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            convertir_T = ("Ejercicio","Descanso sueño","Prevención","Alimentación nutrición","Hábitos de salud")
            for column in convertir_T:
                interpreter = ps.InterpretationTools.interpreter_fabric(
                    operator.ge,
                    self.interpreter_table[column],
                    self.interpreter_table["T"],
                    ps.InterpretationTools.interpreter_selector_max,
                )
                self.table[f"{column}-T"] = self.table[column].apply(interpreter)
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["ARC"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_min,
            )
            self.table["ARC-T"] = self.table["ARC"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str,Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_3(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_3", 15, 75)
        inconsistencies = [
            (1, 11), # 32, 42
            (3, 13), # 34, 44
            (5, 10), # 36, 41
            (6, 7), # 37, 38
            (9, 14) # 37, 38
        ]

        @override
        def _transformation(self) -> None:
            EstresAnalysis.detect_inconsistencies(self.table, self.inconsistencies, self.specification.identifier)
            self.table.rename(columns={"Calificación/75":"Red de apoyo social"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["Red de apoyo social"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_max,
            )
            self.table["Red de apoyo social-T"] = self.table["Red de apoyo social"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_4(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_4", 10, 50)

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/50":"Conducta Tipo A"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["Conducta Tipo A"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_max,
            )
            self.table["Conducta tipo A-T"] = self.table["Conducta Tipo A"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_5(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_5", 30, 150)
        inconsistencies = [
            (25, 27)
        ]

        @override
        def _transformation(self) -> None:
            EstresAnalysis.detect_inconsistencies(self.table, self.inconsistencies, self.specification.identifier)
            self.table.rename(columns={"Calificación/150":"Fuerza cognitiva"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["Fuerza cognitiva"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_max,
            )
            self.table["Fuerza cognitiva-T"] = self.table["Fuerza cognitiva"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_6(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_6", 20, 100)
        classifier = {
            "Valoración positiva":[1,2,3,4,5],
            "Valoración negativa":[6,7,8,9,10],
            "Minimización de la amenaza":[11,12,13,14,15],
            "Concentración en el problema":[16,17,18,19,20],
        }

        @override
        def _transformation(self) -> None:
            self.classify_answers(self.classifier)
            self.table.drop("Calificación/100", axis=1, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            for name in self.classifier.keys():
                interpreter = ps.InterpretationTools.interpreter_fabric(
                    operator.ge,
                    self.interpreter_table[name],
                    self.interpreter_table["T"],
                    ps.InterpretationTools.interpreter_selector_max,
                )
                self.table[f"{name}-T"] = self.table[name].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_7(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_7", 12, 60)
        inconsistencies: list[tuple[int, int]] = [
            (2, 3), # 109, 110
            (4, 6), # 111, 113
            (7, 8), # 114, 115
            (9, 11), # 116, 118
        ]

        @override
        def _transformation(self) -> None:
            EstresAnalysis.detect_inconsistencies(self.table, self.inconsistencies, self.specification.identifier)
            self.table.rename(columns={"Calificación/60":"Bienestar psicológico"}, inplace=True)
            return super()._transformation()

        @override
        def _analysis(self) -> None:
            interpreter = ps.InterpretationTools.interpreter_fabric(
                operator.ge,
                self.interpreter_table["Bienestar psicológico"],
                self.interpreter_table["T"],
                ps.InterpretationTools.interpreter_selector_max,
            )
            self.table["Bienestar psicológico-T"] = self.table["Bienestar psicológico"].apply(interpreter)
            return super()._analysis()

        @override
        def _graph(self) -> None:
            return None

        @override
        def main(self) -> dict[str, Any]:
            self.interpreter_table = EstresAnalysis.interpreter_table
            return super().main()

    class Estres_8(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Estrés_8", 5, 5)

        @override
        def _transformation(self) -> None:
            self.table.rename(columns={"Calificación/5":"Indice de sesgo"}, inplace=True)
            return super()._transformation()

        @override
        def _graph(self) -> None:
            return None

    @override
    def _load_additional_data(self) -> None:
        return None

    @override
    def _cleaning(self):
        self.table = self.estrés_1
        self.table = self.table.join(self.estrés_2, how="outer")
        self.table = self.table.join(self.estrés_3, how="outer")
        self.table = self.table.join(self.estrés_4, how="outer")
        self.table = self.table.join(self.estrés_5, how="outer")
        self.table = self.table.join(self.estrés_6, how="outer")
        self.table = self.table.join(self.estrés_7, how="outer")
        self.table = self.table.join(self.estrés_8, how="outer")

    @override
    def _transformation(self) -> None:
        inconsistencies = [
            "Inconsistencias Estrés_3",
            "Inconsistencias Estrés_5",
            "Inconsistencias Estrés_7"
        ]
        self.table["Inconsistencias"] = self.table[inconsistencies].sum(axis=1)
        self.table.drop(columns=inconsistencies, inplace=True)
        incompletitudes = {
            "Incompletitud Estrés_1":4.88,
            "Incompletitud Estrés_2":20.33,
            "Incompletitud Estrés_3":12.20,
            "Incompletitud Estrés_4":8.13,
            "Incompletitud Estrés_5":24.39,
            "Incompletitud Estrés_6":16.26,
            "Incompletitud Estrés_7":9.76,
            "Incompletitud Estrés_8":4.05,
        }
        l_i = list(incompletitudes.keys())
        self.table.loc[:,l_i] = self.table[l_i].fillna(100)
        self.table["Incompletitud Estrés"] = 0
        for col, val in incompletitudes.items():
            self.table["Incompletitud Estrés"] += self.table[col] * val / 100
        self.table.drop(columns=l_i, inplace=True)
        rows = self.table.shape[0]
        for l in  incompletitudes.keys():
            difference = rows - sum(self.analyzed[l].values())
            if difference > 0:
                incomplete_100 = self.analyzed[l].get(100)
                if not incomplete_100:
                    incomplete_100 = 0
                self.analyzed[l][100] = incomplete_100 + difference

    @override
    def _analysis(self) -> None:
        super()._analysis()

        upper = {"Estrés-T", "ARC-T", "Conducta tipo A-T", "Valoración negativa-T"}
        lower = {"Hábitos de salud-T", "Bienestar psicológico-T"}
        options = set(self.analysis_configurations.keys()).intersection(self.analysis_options.keys())
        for column in options.intersection(upper):
            filter = self.table[column] >= self.analysis_configurations[column]
            filtered = self.table[filter][column]
            self.analyzed["%Alert Estrés-"+column] = round(filtered.size * 100 / len(self.table.index), 2)
            self.saver.save(filtered, ps.Specification[str]("Alert Estrés-"+column))
        for column in options.intersection(lower):
            filter = self.table[column] <= self.analysis_configurations[column]
            filtered = self.table[filter][column]
            self.analyzed["%Alert Estrés-"+column] = round(filtered.size * 100 / len(self.table.index), 2)
            self.saver.save(filtered,ps.Specification[str]("Alerta Estrés-"+column))

    @override
    def main(self):
        EstresAnalysis.interpreter_table = pd.read_csv(self._conversion_table.with_stem("Conversión T"))
        estres_1 = self.Estres_1()
        self.analyzed.update(estres_1.main())
        self.estrés_1 = estres_1.table

        estres_2 = self.Estres_2()
        self.analyzed.update(estres_2.main())
        self.estrés_2 = estres_2.table

        estres_3 = self.Estres_3()
        self.analyzed.update(estres_3.main())
        self.estrés_3 = estres_3.table

        estres_4 = self.Estres_4()
        self.analyzed.update(estres_4.main())
        self.estrés_4 = estres_4.table

        estres_5 = self.Estres_5()
        self.analyzed.update(estres_5.main())
        self.estrés_5 = estres_5.table

        estres_6 = self.Estres_6()
        self.analyzed.update(estres_6.main())
        self.estrés_6 = estres_6.table

        estres_7 = self.Estres_7()
        self.analyzed.update(estres_7.main())
        self.estrés_7 = estres_7.table

        estres_8 = self.Estres_8()
        self.analyzed.update(estres_8.main())
        self.estrés_8 = estres_8.table

        if any(map(lambda x: "message" in x, self.analyzed.keys())):
            self.analyzed[f"message_{self.__class__.__name__}"] = "Uno de los exámenes previos fallo"
            return self.analyzed
        ps.DummyLoader.source = estres_1.table
        return super().main()