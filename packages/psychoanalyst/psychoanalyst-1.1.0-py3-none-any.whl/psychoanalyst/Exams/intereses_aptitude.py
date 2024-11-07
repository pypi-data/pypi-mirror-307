from typing import Any, override

import psychoanalyst as ps

class InteresesAptitudesAnalysis(ps.CommonAnalysisPipeline):
    perfiles = ["S.S", "E.P", "V.", "A.P", "Ms", "Og", "Ct", "Cl", "M.C", "AL"]
    specification = ps.ExamSpecification("Intereses-Aptitudes", 0, 0)
    class Intereses(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Intereses", 60, 240)
        def __init__(self) -> None:
            super().__init__()
            self.classifier = {
                perfil: [i for i in range(index, self.specification.num_questions+1, 10)]
                for index, perfil in enumerate(InteresesAptitudesAnalysis.perfiles,1)
            }

        @override
        def _transformation(self) -> None:
            self.classify_answers(self.classifier)
            self.table.drop("Calificación/240", axis=1, inplace=True)
            # Get higher profile values
            self.table["max"] = self.table[InteresesAptitudesAnalysis.perfiles].max(axis=1)
            self.table["Perfil dominante intereses"] = []
            for column in InteresesAptitudesAnalysis.perfiles:
                filter = (self.table[column] == self.table["max"])
                # Add profile as dominant if it has the same value has the highest value
                self.table.loc[filter,"Perfil dominante intereses"].apply(lambda x: x.append(column))
                self.table[column] = self.table[column].astype("float")
                self.table[column] = (
                    self.table[column]
                    /24 # Max possible value for each profile
                    *100
                ).round(decimals=2)
            self.table.drop(columns=["max"], inplace=True)
            self.table["Perfil dominante intereses"] = self.table["Perfil dominante intereses"].apply(lambda x: "-".join(x))
            return super()._transformation()

    class Aptitudes(ps.CommonAnalysisPipeline):
        specification = ps.ExamSpecification("Aptitudes", 60, 240)
        def __init__(self) -> None:
            super().__init__()
            self.classifier = {
                perfil: [i for i in range(index, self.specification.num_questions+1, 10)]
                for index, perfil in enumerate(InteresesAptitudesAnalysis.perfiles,1)
            }

        @override
        def _transformation(self) -> None:
            self.classify_answers(self.classifier)
            self.table.drop("Calificación/240", axis=1, inplace=True)
            # Get higher profile values
            self.table["max"] = self.table[InteresesAptitudesAnalysis.perfiles].max(axis=1)
            self.table["Perfil dominante aptitudes"] = []
            for column in InteresesAptitudesAnalysis.perfiles:
                filter = (self.table[column] == self.table["max"])
                # Add profile as dominant if it has the same value has the highest value
                self.table.loc[filter,"Perfil dominante aptitudes"].apply(lambda x: x.append(column))
                self.table[column] = self.table[column].astype("float")
                self.table[column] = (
                    self.table[column]
                    /24 # Max possible value for each profile
                    *100
                ).round(decimals=2)
            self.table.drop(columns=["max"], inplace=True)
            self.table["Perfil dominante aptitudes"] = self.table["Perfil dominante aptitudes"].apply(lambda x: "-".join(x))
            return super()._transformation()

    @override
    def main(self) -> dict[str, Any]:
        intereses = self.Intereses()
        self.analyzed.update(intereses.main())
        self.intereses = intereses.table

        aptitudes = self.Aptitudes()
        self.analyzed.update(aptitudes.main())
        self.aptitudes = aptitudes.table

        return self.analyzed