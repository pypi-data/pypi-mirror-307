import psychoanalyst as ps

class EstresComparison(ps.ComparisonAnalysisPipeline):
    means_graph = [
        "Estrés-T",
        "Hábitos de salud-T",
        "ARC-T",
        "Red de apoyo social-T",
        "Conducta Tipo A-T",
        "Fuerza cognitiva-T",
        "Valoración positiva-T",
        "Valoración negativa-T",
        "Minimización de la amenaza-T",
        "Concentración en el problema-T",
        "Bienestar psicológico-T",
    ]

    specification = ps.ComparativeSpecification(
        "Estrés Comparison",
        ["Dirección Email"],
        [
            # "Estrés",
            "Estrés-T",
            # "Hábitos de salud",
            # "Ejercicio",
            # "Descanso sueño",
            # "Prevención",
            # "Alimentación nutrición",
            # "ARC",
            # "Ejercicio-T",
            # "Descanso sueño-T",
            # "Prevención-T",
            # "Alimentación nutrición-T",
            "Hábitos de salud-T",
            "ARC-T",
            # "Red de apoyo social",
            "Red de apoyo social-T",
            # "Conducta Tipo A",
            "Conducta Tipo A-T",
            # "Fuerza cognitiva",
            "Fuerza cognitiva-T",
            # "Valoración positiva",
            # "Valoración negativa",
            # "Minimización de la amenaza",
            # "Concentración en el problema",
            "Valoración positiva-T",
            "Valoración negativa-T",
            "Minimización de la amenaza-T",
            "Concentración en el problema-T",
            # "Bienestar psicológico",
            "Bienestar psicológico-T",
            "Indice de sesgo",
            "Inconsistencias",
            "Incompletitud Estrés"
        ]
    )