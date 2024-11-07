from typing import Any, override

import pandas as pd

import psychoanalyst as ps

class DiscAnalysis(ps.CommonAnalysisPipeline):
    __positive_answers = [i for i in range(1,57,2)]
    __negative_answers = [i for i in range(2,57,2)]
    __DOMINIO = 1
    __INFLUENCIA = 2
    __SEGURIDAD = 3
    __COMPLACENCIA = 4
    specification = ps.ExamSpecification("DISC", 56, 224)
    columns = ["Dominio","Influencia","Seguridad","Complacencia"]

    @staticmethod
    def relativize_patter(frame:pd.DataFrame) -> pd.DataFrame:
        # Center pattern around 0
        means = frame.mean(axis=1)
        frame = frame.apply(lambda column: column - means)
        # Move patterns towards the positives to avoid negative values and divisions between 0s
        pivots = abs(frame).sum(axis=1)
        frame = frame.apply(lambda column: column + pivots)
        # Convert patterns to a relative form
        means = frame.mean(axis=1)
        # Avoid 0`s means
        means = means.replace(0,1)
        frame = frame.apply(lambda column: column/means)
        return frame

    @override
    def _transformation(self) -> None:
        self.table.drop("Calificación/224", axis=1, inplace=True)
        self.table["Dominio"] =         (self.table[DiscAnalysis.__positive_answers] == DiscAnalysis.__DOMINIO).sum(axis=1) - \
                                        (self.table[DiscAnalysis.__negative_answers] == DiscAnalysis.__DOMINIO).sum(axis=1)
        self.table["Influencia"] =      (self.table[DiscAnalysis.__positive_answers] == DiscAnalysis.__INFLUENCIA).sum(axis=1) - \
                                        (self.table[DiscAnalysis.__negative_answers] == DiscAnalysis.__INFLUENCIA).sum(axis=1)
        self.table["Seguridad"] =       (self.table[DiscAnalysis.__positive_answers] == DiscAnalysis.__SEGURIDAD).sum(axis=1) - \
                                        (self.table[DiscAnalysis.__negative_answers] == DiscAnalysis.__SEGURIDAD).sum(axis=1)
        self.table["Complacencia"] =    (self.table[DiscAnalysis.__positive_answers] == DiscAnalysis.__COMPLACENCIA).sum(axis=1) - \
                                        (self.table[DiscAnalysis.__negative_answers] == DiscAnalysis.__COMPLACENCIA).sum(axis=1)
        def inputFilter(interpretedValue: pd.Series, entryPoint: pd.DataFrame) -> pd.Series:
            # Calculate patter difference between user pattern and profile patterns
            pattern_difference = abs(entryPoint - interpretedValue).sum(axis=1)
            # Select the profile with the pattern that most closely resembles the user`s pattern
            return (pattern_difference == pattern_difference.min())
        interpreter = ps.InterpretationTools.interpreter_fabric(
            filter=inputFilter,  # type: ignore
            compared_value=self.relativize_patter(self.interpreter_table[self.columns]),
            interpreted_value_out=self.interpreter_table["Perfil representativo"],
            result_selector=ps.InterpretationTools.interpreter_selector_join
        )
        self.table["Perfil"] = self.relativize_patter(self.table[self.columns]).apply(interpreter, axis=1)
        return super()._transformation()

    @override
    def main(self) -> dict[str, Any]:
        self.interpreter_table = pd.read_csv(self._conversion_table.with_stem("DISC"))
        return super().main()