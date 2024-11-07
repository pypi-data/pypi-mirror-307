from typing import ClassVar, Literal, Callable
from pathlib import Path

def exception_reporter(e:Exception):
    raise e

class CommonData:
    """Data that needs to be accesible to all files
    """
    year: ClassVar[int]
    """Year of analysis"""
    cycle: ClassVar[Literal["A", "B"]]
    """year cycle of analysis"""
    semester: ClassVar[int]
    """Analyzed group of students (1 = freshmen)"""
    figures_path: ClassVar[Path] = Path.home() / "Results" / "Graphs" / "default.png"
    """Where figures/graphs should be saved"""
    json_path: ClassVar[Path] = Path.home() / "Results" / "json" / "default.json"
    """The results of analysis in an standard format"""
    exception_reporter: ClassVar[Callable[[Exception], None]] = exception_reporter
    """Common function to report exceptions"""
    progress_reporter: ClassVar[Callable[[str], None]] = lambda s: None
    """Common function to report Progress"""
    @classmethod
    def previous_semester(cls):
        """
        Goes back in time using (year, cycle, semester)
        """
        if cls.semester <=1:
            raise UserWarning("Can`t go back")
        if cls.cycle == "B":
            cls.cycle = "A"
        else:
            cls.year -= 1
            cls.cycle = "B"
        cls.semester -= 1
    @classmethod
    def next_semester(cls):
        """
        Goes forward in time using (year, cycle, semester)
        """
        if cls.cycle == "A":
            cls.cycle = "B"
        else:
            cls.year += 1
            cls.cycle = "A"
        cls.semester += 1