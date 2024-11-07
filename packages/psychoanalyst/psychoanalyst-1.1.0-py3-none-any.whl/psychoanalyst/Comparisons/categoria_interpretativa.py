import psychoanalyst as ps

class CategoriaInterpretativaComparison(ps.ComparisonAnalysisPipeline):
    means_graph = [
        "Puntuación estándar",
        "Puntuación estándar abstracción",
        "Puntuación estándar vocabulario",
    ]
    specification = ps.ComparativeSpecification(
        "Categoría interpretativa Comparison",
        ["Dirección Email"],
        [
            "Puntuación estándar",
            "Puntuación estándar abstracción",
            "Puntuación estándar vocabulario",
            "Incompletitud Categoría interpretativa",
        ]
    )