from typing import Any, Callable

from pathlib import Path

import dearpygui.dearpygui as dpg

from psychoanalyst.common_data import CommonData
import psychoanalyst as ps
import psychoanalyst.Exams as pse
import psychoanalyst.Comparisons as psc

class Application:
    application_dir = Path(__file__).parent
    def __init__(self) -> None:
        self.configuration: dict[str, dict[str,Any]] = dict()
        self.analysis_pipes: dict[str, ps.CommonAnalysisPipeline] = {
            "Estrés": pse.EstresAnalysis(),
            "Ryff": pse.RyffAnalysis(),
            "Categoría interpretativa": pse.CategoriaInterpretativaAnalysis(),
            "DISC": pse.DiscAnalysis(),
            "Intereses y aptitudes": pse.InteresesAptitudesAnalysis(),
        }
        self.comparison_pipes: dict[str, ps.ComparisonAnalysisPipeline] = {
            "Estrés": psc.EstresComparison(),
            "Ryff": psc.RyffComparison(),
            "Categoría interpretativa": psc.CategoriaInterpretativaComparison(),
        }
        # configuration, analysis_pipes and comparison_pipes should share keys for every shared exam implementation
        self.setup_view()
    
    def setup_view(self) -> None:
        # Configurar la ventana
        dpg.create_context()
        dpg.create_viewport(title="Psicoanalisis", small_icon=str(self.application_dir / "assets/cuy-128.ico"), large_icon=str(self.application_dir / "assets/cuy-128.ico"))
        dpg.setup_dearpygui()

        dpg.add_file_dialog(label="Input directory", directory_selector=True, callback=self.set_input_dir, show=False, width=960, height=540, tag="input_dir_selector")
        dpg.add_file_dialog(label="Output directory", directory_selector=True, callback=self.set_output_dir, show=False, width=960, height=540, tag="output_dir_selector")
        dpg.add_file_dialog(label="Graphs directory", directory_selector=True, callback=self.set_graphs_dir, show=False, width=960, height=540, tag="graphs_dir_selector")
        dpg.add_file_dialog(label="Storage directory", directory_selector=True, callback=self.set_storage_dir, show=False, width=960, height=540, tag="storage_dir_selector")
        with dpg.file_dialog(label="Identity table", show=False, callback=self.set_identity_table, width=960, height=540, tag="identity_table_selector"):
                dpg.add_file_extension("CSV (*.csv){.csv}", color=(0, 255, 0, 255), custom_text="[Table]")

        with dpg.window(label="Confirm", tag="confirmation_store", show=False, no_resize=True) as tag:
            dpg.add_text("Si existen datos que coincidan en año, ciclo, semestre \nde los estudiante y examen, estos datos se perderán", color=(200, 10, 10, 255))
            updater = self.setup_year_configuration(tag)
            def confirmation() -> None:
                dpg.hide_item("confirmation_store")
                updater()
                self.permanent_store()
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit):
                dpg.add_table_column()
                dpg.add_table_column(width_stretch=True)
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_button(label="Cancelar", callback=lambda: dpg.hide_item("confirmation_store"))
                    dpg.add_table_cell()
                    dpg.add_button(label="Confirmar", callback=confirmation)

        with dpg.window(label="Select", tag="comparison_select", show=False, width=400, no_resize=True) as tag:
            updater = self.setup_year_configuration(tag)
            def compare() -> None:
                dpg.hide_item("comparison_select")
                updater()
                self.compare_data()
            dpg.add_button(label="Select Identity Table", callback=lambda:dpg.show_item("identity_table_selector"))
            dpg.add_input_text(default_value="NONE", enabled=False, width=-1, tag="identity_table")
            with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit):
                dpg.add_table_column(width_stretch=True)
                dpg.add_table_column()
                dpg.add_table_column(width_stretch=True)
                with dpg.table_row():
                    dpg.add_table_cell()
                    dpg.add_button(label="Analizar", callback=compare)
                    dpg.add_table_cell()

        # Crear la ventana principal
        with dpg.window(tag="main") as tag:
            self.setup_configuration_exams(tag)
            self.setup_configuration_environment(tag)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Analizar", callback=self.analyse)
                t = dpg.add_button(label="Almacenar permanentemente", callback=lambda: dpg.show_item("confirmation_store"))
                with dpg.tooltip(t):
                    dpg.add_text("Almacena valores relevantes de las pruebas:\n\t- Estrés\n\t- Categoría interpretativa\n\t- Ryff")
                t = dpg.add_button(label="Comparar", callback=lambda: dpg.show_item("comparison_select"))
                with dpg.tooltip(t):
                    dpg.add_text("1. Selecciona un semestre para analizar, que se encuentre en el almacén permanente\n2. El programa busca todos los datos previos de esa misma generación de estudiantes\n3. El programa Compara todos los datos disponibles")
                dpg.add_button(label="Show Log", callback=lambda : dpg.show_item("logs"))

        with dpg.window(label="Log", tag="logs", show=False, width=600, height=600):
            def clear_logs():
                d: dict[int,list[int]] = dpg.get_item_children("pretty_log") # type: ignore
                for item in d[1]:
                    dpg.delete_item(item)
            dpg.add_button(label="Clear", callback=clear_logs)
            with dpg.child_window(tag="pretty_log", autosize_x=True, autosize_y=True, horizontal_scrollbar=True):
                def add_progress_log(info:str):
                    dpg.add_text(info, parent="pretty_log", color=(10, 150, 10, 255))
                def add_error_log(info: Exception):
                    dpg.add_text(str(info), parent="pretty_log", color=(150, 10, 10, 255))
                CommonData.progress_reporter = add_progress_log
                CommonData.exception_reporter = add_error_log

        with dpg.theme(tag="default"):
            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 245, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (240, 245, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (240, 245, 250, 255)) 
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
                
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (150, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button, (150, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (150, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (150, 200, 255, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (150, 200, 255, 255))

                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (50, 150, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (50, 150, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (50, 150, 200, 255))

                dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, (240, 245, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TableRowBgAlt, (200, 200, 200, 255))

                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (200, 145, 210, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (200, 145, 210, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (200, 145, 210, 255))

            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (50, 100, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (40, 80, 160, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (40, 160, 80, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

            dpg.bind_theme("default")

        # Ejecutar la aplicación
        dpg.show_viewport()
        dpg.set_primary_window("main", True)
        dpg.set_viewport_resizable(True)
        dpg.start_dearpygui()

    def setup_configuration_exams(self, main_tag: int|str) -> None:
        with dpg.collapsing_header(label="Configuración Estrés", show=False, tag="conf_estres", parent=main_tag) as tag:
            with dpg.table(policy=dpg.mvTable_SizingFixedFit, borders_outerH=True, borders_outerV=True, no_host_extendX=True, row_background=True):
                dpg.add_table_column(label="Configuración")
                dpg.add_table_column(label="Valor",init_width_or_weight=150)
                dpg.add_table_column(label="Activo")
                for text, tooltip in pse.EstresAnalysis.analysis_options.items():
                    with dpg.table_row():
                        tag_2 = dpg.add_text(text)
                        with dpg.tooltip(tag_2):
                            dpg.add_text(tooltip)
                        tag_2 = dpg.add_input_int(default_value=19, min_value=19, max_value=81, min_clamped=True, max_clamped=True, callback=self.change_configuration_value)
                        tag_3 = dpg.add_checkbox(user_data=("Estrés", text, tag_2), callback=self.toggle_configuration)
                        dpg.configure_item(tag_2, user_data=("Estrés", text, tag_3))
            def toggle_estres(_, value) -> None:
                if value:
                    self.configuration["Estrés"] = dict()
                    dpg.show_item("conf_estres")
                else:
                    self.configuration.pop("Estrés")
                    dpg.hide_item("conf_estres")
            dpg.add_checkbox(label="Estrés", before=tag, callback=toggle_estres)
        with dpg.collapsing_header(label="Configuración Ryff", show=False, tag="conf_ryff", parent=main_tag) as tag:
            with dpg.table(policy=dpg.mvTable_SizingFixedFit, borders_outerH=True, borders_outerV=True, no_host_extendX=True, row_background=True):
                dpg.add_table_column(label="Configuración")
                dpg.add_table_column(label="Valor",init_width_or_weight=150)
                dpg.add_table_column(label="Activo")
                for text, tooltip in pse.RyffAnalysis.analysis_options.items():
                    with dpg.table_row():
                        tag_2 = dpg.add_text(text)
                        with dpg.tooltip(tag_2):
                            dpg.add_text(tooltip)
                        tag_2 = dpg.add_input_int(default_value=6, min_value=6, max_value=36, min_clamped=True, max_clamped=True, callback=self.change_configuration_value)
                        tag_3 = dpg.add_checkbox(user_data=("Ryff", text, tag_2), callback=self.toggle_configuration)
                        dpg.configure_item(tag_2, user_data=("Ryff", text, tag_3))
            def toggle_ryff(_, value) -> None:
                if value:
                    self.configuration["Ryff"] = dict()
                    dpg.show_item("conf_ryff")
                else:
                    self.configuration.pop("Ryff")
                    dpg.hide_item("conf_ryff")
            dpg.add_checkbox(label="Ryff", before=tag, callback=toggle_ryff)
        with dpg.collapsing_header(label="Configuración categoría interpretativa", show=False, tag="conf_ci", parent=main_tag) as tag:
            with dpg.table(policy=dpg.mvTable_SizingFixedFit, borders_outerH=True, borders_outerV=True, no_host_extendX=True, row_background=True):
                dpg.add_table_column(label="Configuración")
                dpg.add_table_column(label="Valor",init_width_or_weight=150)
                dpg.add_table_column(label="Activo")
                for text, tooltip in pse.CategoriaInterpretativaAnalysis.analysis_options.items():
                    with dpg.table_row():
                        tag_2 = dpg.add_text(text)
                        with dpg.tooltip(tag_2):
                            dpg.add_text(tooltip)
                        tag_2 = dpg.add_input_int(default_value=30, min_value=30, max_value=146, min_clamped=True, max_clamped=True, callback=self.change_configuration_value)
                        tag_3 = dpg.add_checkbox(user_data=("Categoría interpretativa", text, tag_2), callback=self.toggle_configuration)
                        dpg.configure_item(tag_2, user_data=("Categoría interpretativa", text, tag_3))
            def toggle_ci(_, value) -> None:
                if value:
                    self.configuration["Categoría interpretativa"] = dict()
                    dpg.show_item("conf_ci")
                else:
                    self.configuration.pop("Categoría interpretativa")
                    dpg.hide_item("conf_ci")
            dpg.add_checkbox(label="Categoría interpretativa", before=tag, callback=toggle_ci)
        dpg.add_checkbox(label="DISC", parent=main_tag,
            callback=lambda s,v: self.configuration.__setitem__("DISC", dict()) if v else self.configuration.pop("DISC")
        )
        dpg.add_checkbox(label="Intereses y aptitudes", parent=main_tag,
            callback=lambda s,v: self.configuration.__setitem__("Intereses y aptitudes", dict()) if v else self.configuration.pop("Intereses y aptitudes")
        )

    def setup_configuration_environment(self, main_tag) -> None:
        with dpg.group(horizontal=True, parent=main_tag):
            tag = dpg.add_button(label="Input directory", callback=lambda:dpg.show_item("input_dir_selector"), width=150)
            with dpg.tooltip(tag):
                dpg.add_text("Directorio donde se encuentran los exámenes en formato .csv")
            dpg.add_input_text(default_value=str(Path.home() / "Exams"), enabled=False, width=-1, tag="input_dir")
        with dpg.group(horizontal=True, parent=main_tag):
            tag = dpg.add_button(label="Output directory", callback=lambda:dpg.show_item("output_dir_selector"), width=150)
            with dpg.tooltip(tag):
                dpg.add_text("Directorio donde se guardaran los exámenes analizados")
            dpg.add_input_text(default_value=str(Path.home() / "Results"), enabled=False, width=-1, tag="output_dir")
        with dpg.group(horizontal=True, parent=main_tag):
            tag = dpg.add_button(label="Graphs directory", callback=lambda:dpg.show_item("graphs_dir_selector"), width=150)
            with dpg.tooltip(tag):
                dpg.add_text("Directorio donde se guardaran las gráficas del análisis")
            dpg.add_input_text(default_value=str(Path.home() / "Results" / "Graphs"), enabled=False, width=-1, tag="graphs_dir")
        with dpg.group(horizontal=True, parent=main_tag):
            tag = dpg.add_button(label="Permanent storage", callback=lambda:dpg.show_item("storage_dir_selector"), width=150)
            with dpg.tooltip(tag):
                dpg.add_text("Directorio donde se guardan las bases de datos permanentes")
            dpg.add_input_text(default_value=str((Path.home() / "psicoanalisis")), enabled=False, width=-1, tag="storage_dir")

    def setup_year_configuration(self, main_tag) -> Callable[[], None]:
        with dpg.table(header_row=False, policy=dpg.mvTable_SizingFixedFit, parent=main_tag):
            dpg.add_table_column()
            dpg.add_table_column(width_stretch=True)
            with dpg.table_row():
                dpg.add_text("Año en que se recolectaron los datos")
                CommonData.year = 2024
                year = dpg.add_input_int(default_value=2024, min_value=2024, min_clamped=True, width=-1)
            with dpg.table_row():
                dpg.add_text("Ciclo en que se recolectaron los datos")
                CommonData.cycle = "A"
                cycle = dpg.add_combo(["A", "B"], default_value="A", width=-1)
            with dpg.table_row():
                dpg.add_text("Semestre de los estudiantes evaluados")
                CommonData.semester = 1
                semester = dpg.add_input_int(default_value=1, min_value=1, min_clamped=True, width=-1)
        def update() -> None:
            CommonData.year = dpg.get_value(year)
            CommonData.cycle = dpg.get_value(cycle)
            CommonData.semester = dpg.get_value(semester)
        return update

    def change_configuration_value(self, _, app_data, user_data) -> None:
        test, configuration, activated_tag = user_data
        if self.configuration[test].get(configuration) is None:
            dpg.set_value(activated_tag, True)
        self.configuration[test][configuration] = app_data

    def toggle_configuration(self, _, activate, user_data) -> None:
        test, configuration, value_tag = user_data
        if activate:
            self.configuration[test][configuration] = dpg.get_value(value_tag)
        else:
            self.configuration[test].pop(configuration)

    def set_input_dir(self, _, app_data) -> None:
        directory = Path(app_data["file_path_name"])
        dpg.set_value("input_dir", str(directory))
        ps.CsvLoader.source = directory / "default.csv"

    def set_output_dir(self, _, app_data) -> None:
        directory = Path(app_data["file_path_name"])
        dpg.set_value("output_dir", str(directory))
        ps.CsvSaver.destiny = directory / "default.csv"
        CommonData.json_path = directory / "json" / "default.json"

    def set_graphs_dir(self, _, app_data) -> None:
        directory = Path(app_data["file_path_name"])
        dpg.set_value("graphs_dir", str(directory))
        CommonData.figures_path = directory / "default.png"

    def set_storage_dir(self, _, app_data) -> None:
        directory = Path(app_data["file_path_name"])
        dpg.set_value("storage_dir", str(directory))
        ps.SqliteSaver.destiny = directory / "default.db"
        ps.SqliteLoader.source = directory / "default.db"

    def set_identity_table(self, _, app_data) -> None:
        file = Path(app_data["file_path_name"])
        dpg.set_value("identity_table", str(file))
        ps.ComparisonAnalysisPipeline.identity_data_path = file

    def analyse(self) -> None:
        dpg.show_item("logs")
        if len(self.configuration.keys()) == 0:
            CommonData.exception_reporter(
                Exception("No hay exámenes seleccionados")
            )
            return None
        for key, configuration in self.configuration.items():
            self.analysis_pipes[key].set_configuration(configuration)
            self.analysis_pipes[key].main()
        CommonData.progress_reporter("TERMINO EL ANÁLISIS")

    def permanent_store(self) -> None:
        dpg.show_item("logs")
        if len(self.configuration.keys()) == 0:
            CommonData.exception_reporter(
                Exception("No hay exámenes seleccionados")
            )
            return None
        # Marks if it"s possible to store the data
        flag = True
        to_Store = set(self.comparison_pipes.keys()).intersection(self.configuration.keys())
        # Follow a transaction strategy: all currently configured items should be analyzed.
        # If any item was not analyzed, no results will be stored for any of the items.
        # In other words, if one or more items fail to be analyzed, the storage of results will be skipped entirely.
        for key in to_Store:
            if self.analysis_pipes[key].table is None:
                flag = False
                CommonData.exception_reporter(
                    Exception(f"Faltan los datos del examen {key}, vuelve a analizar, o elimina este examen de tu selección")
                )
        if not flag:
            return
        for key in to_Store:
            self.comparison_pipes[key].save_to_sql(self.analysis_pipes[key].table)
            self.analysis_pipes[key].table = None # type: ignore
            CommonData.progress_reporter(f"Se almacenaron los datos de {key}")
        CommonData.progress_reporter("DATOS GUARDADOS PERMANENTEMENTE")

    def compare_data(self):
        dpg.show_item("logs")
        if len(self.configuration.keys()) == 0:
            CommonData.exception_reporter(
                Exception("No hay exámenes seleccionados")
            )
            return None
        for key, configuration in self.configuration.items():
            self.comparison_pipes[key].set_configuration(configuration)
            self.comparison_pipes[key].main()
        CommonData.progress_reporter("TERMINO LA COMPARACIÓN")

def main():
    Application()

if __name__ == "__main__":
    main()