from dataclasses import dataclass

class StructureError(Exception):
    """Loaded data does not have the expected Structure"""

@dataclass(slots=True, frozen=True)
class Specification[T]:
    identifier: T

@dataclass(slots=True, frozen=True)
class ExamSpecification(Specification[str]):
    num_questions: int
    total_grade: int

@dataclass(slots=True, frozen=True)
class ComparativeSpecification(Specification[str]):
    index_columns: list[str]
    compared_columns: list[str]