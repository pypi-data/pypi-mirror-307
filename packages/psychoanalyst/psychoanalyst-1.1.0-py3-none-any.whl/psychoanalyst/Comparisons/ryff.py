import psychoanalyst as ps

class RyffComparison(ps.ComparisonAnalysisPipeline):
    means_graph = [
        "Puntuación BP",
    ]
    specification = ps.ComparativeSpecification(
        "Ryff Comparison",
        ["Dirección Email"],
        [
            "Puntuación BP",
            "Incompletitud Ryff"
        ]
    )