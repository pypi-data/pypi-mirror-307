from typing import Any, Callable

import pandas as pd

class InterpretationTools:
    @staticmethod
    def interpreter_selector_first(options: pd.Series) -> Any:
        return options[options.first_valid_index()]

    @staticmethod
    def interpreter_selector_max(options: pd.Series) -> Any:
        return options.max()

    @staticmethod
    def interpreter_selector_min(options: pd.Series) -> Any:
        return options.min()

    @staticmethod
    def interpreter_selector_join(options: pd.Series) -> str:
        return ",".join(map(lambda val: str(val), options))

    @staticmethod
    def interpreter_fabric(
        filter: Callable[[Any, pd.Series | pd.DataFrame], pd.Series],
        compared_value: pd.Series | pd.DataFrame,
        interpreted_value_out: pd.Series,
        result_selector: Callable[[pd.Series], Any],
        default_value: Any = None
    ) -> Callable[[Any], Any]:
        def inner(interpreted_value: Any):
            posible_results = filter(interpreted_value, compared_value)
            results = interpreted_value_out[posible_results]
            if len(results) == 0 and default_value != None: return default_value
            return result_selector(results)
        return inner