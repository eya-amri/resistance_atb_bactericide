import pandas as pd

# ──────────────────────────────────────────────
#  Données réelles issues de la présentation
# ──────────────────────────────────────────────

BACTERICIDAL_CLASSES = [
    "Carbapenem",
    "Cephalosporin",
    "Penicillin beta-lactam",
    "Glycopeptide antibiotic",
    "Nitroimidazole antibiotic",
    "Rifamycin antibiotic",
    "Monobactam",
    "Phosphonic acid antibiotic",
]

BACTERIOSTATIC_CLASSES = [
    "Macrolide antibiotic",
    "Oxazolidinone antibiotic",
    "Sulfonamide antibiotic",
    "Lincosamide antibiotic",
    "Tetracycline antibiotic",
    "Phenicol antibiotic",
    "Nitrofuran antibiotic",
    "Fusidane antibiotic",
    "Diaminopyrimidine antibiotic",
]

DUAL_CLASSES = [
    "Fluoroquinolone antibiotic",
    "Aminoglycoside antibiotic",
    "Oxazolidinone antibiotic",
    "Tetracycline antibiotic",
    "Glycylcycline",
    "Phenicol antibiotic",
]

CARD_ARO_GENES = {
    "Cephalosporin": 3404,
    "Penicillin beta-lactam": 3115,
    "Carbapenem": 2572,
    "Monobactam": 1310,
    "Fluoroquinolone antibiotic": 307,
    "Aminoglycoside antibiotic": 303,
    "Macrolide antibiotic": 212,
    "Peptide antibiotic": 187,
    "Tetracycline antibiotic": 186,
    "Phenicol antibiotic": 140,
    "Lincosamide antibiotic": 108,
    "Glycopeptide antibiotic": 103,
    "Streptogramin antibiotic": 99,
    "Rifamycin antibiotic": 63,
    "Phosphonic acid antibiotic": 48,
    "Glycylcycline": 37,
    "Oxazolidinone antibiotic": 18,
    "Nitroimidazole antibiotic": 18,
    "Sulfonamide antibiotic": 10,
}

CARD_TOTAL_CLASSES = 46
CARD_BACTERICIDE_COUNT = 10
CARD_BACTERICIDE_STRICT = 8
CARD_BACTERIOSTATIC_COUNT = 9
CARD_UNDETERMINED = 26

# ──────────────────────────────────────────────
#  46 classes CARD — descriptions FR + occurrences
# ──────────────────────────────────────────────
CARD_CLASS_DETAILS = {
    "aminocoumarin antibiotic": {
        "desc": "Les aminocoumarines se lient à la sous-unité B de l'ADN gyrase et inhibent la superenroulement de l'ADN dépendant de l'ATP.",
        "genes": 12,
    },
    "aminoglycoside antibiotic": {
        "desc": "Les aminosides se lient à la sous-unité ribosomique 30S et inhibent la translocation du peptidyl-ARNt, entraînant une mauvaise lecture de l'ARNm et bloquant la synthèse protéique.",
        "genes": 303,
    },
    "antibacterial free fatty acids": {
        "desc": "Les acides gras libres perturbent la chaîne de transport des électrons et la phosphorylation oxydative. Ils peuvent aussi inhiber des enzymes, lyser les cellules bactériennes ou générer des produits de peroxydation toxiques.",
        "genes": 5,
    },
    "antibiotic without defined classification": {
        "desc": "Composés antibiotiques de structure ou d'origine unique, sans classification définie dans la nomenclature standard.",
        "genes": 8,
    },
    "bicyclomycin-like antibiotic": {
        "desc": "Groupe d'antibiotiques comprenant la bicyclomycine et ses analogues structuraux.",
        "genes": 3,
    },
    "carbapenem": {
        "desc": "Les carbapénèmes sont des antibiotiques bêta-lactamines à large spectre, très résistants aux bêta-lactamases. Ils sont bactéricides et agissent en inhibant la synthèse de la couche de peptidoglycane de la paroi bactérienne.",
        "genes": 2572,
    },
    "cephalosporin": {
        "desc": "Les céphalosporines sont des antibiotiques bêta-lactamines bactéricides. Elles inhibent la synthèse de la couche peptidoglycane de la paroi cellulaire bactérienne, essentielle à l'intégrité structurelle.",
        "genes": 3404,
    },
    "cycloserine-like antibiotic": {
        "desc": "Groupe d'antibiotiques comprenant la cyclosérine et ses dérivés, ciblant la synthèse de la paroi bactérienne.",
        "genes": 6,
    },
    "diaminopyrimidine antibiotic": {
        "desc": "Les diaminopyrimidines inhibent la dihydrofolate réductase, enzyme critique pour la synthèse de l'ADN et la voie de biosynthèse de l'acide tétrahydrofolique.",
        "genes": 15,
    },
    "diarylquinoline antibiotic": {
        "desc": "Antibiotiques antimycobactériens ciblant Mycobacterium tuberculosis. Ils inhibent la synthèse d'ATP en perturbant l'ATP synthase mycobactérienne.",
        "genes": 4,
    },
    "disinfecting agents and antiseptics": {
        "desc": "Désinfectants pouvant interagir avec les mécanismes de résistance aux antimicrobiens, notamment via l'efflux moléculaire.",
        "genes": 66,
    },
    "elfamycin antibiotic": {
        "desc": "Les elfamycines inhibent le facteur d'élongation bactérien EF-Tu, une protéine clé qui apporte l'aminoacyl-ARNt au ribosome. Elles perturbent ainsi la synthèse protéique.",
        "genes": 7,
    },
    "fluoroquinolone antibiotic": {
        "desc": "Les fluoroquinolones sont des antibiotiques synthétiques à large spectre qui interagissent avec la topoisomérase II (ADN gyrase) pour perturber la réplication de l'ADN bactérien et provoquer la mort cellulaire.",
        "genes": 307,
    },
    "fusidane antibiotic": {
        "desc": "Groupe d'antibiotiques possédant des structures stéroïdiennes ou pseudo-stéroïdiennes. Ils inhibent la synthèse protéique en bloquant le facteur d'élongation G.",
        "genes": 22,
    },
    "glycopeptide antibiotic": {
        "desc": "Les glycopeptides se lient au motif terminal D-Ala-D-Ala des précurseurs du peptidoglycane, inhibant la transglycolsylation et provoquant la mort cellulaire par stress osmotique. Actifs principalement contre les bactéries Gram-positives.",
        "genes": 103,
    },
    "glycylcycline": {
        "desc": "Les glycylcyclines sont des analogues de tétracyclines conçus pour contourner deux mécanismes de résistance. La tigécycline, seul représentant clinique, inhibe le ribosome 30S en empêchant la liaison de l'aminoacyl-ARNt.",
        "genes": 37,
    },
    "isoniazid-like antibiotic": {
        "desc": "Groupe d'antibiotiques contenant l'isoniazide et ses dérivés, principalement utilisés contre Mycobacterium tuberculosis. Ils inhibent la synthèse des acides mycoliques.",
        "genes": 9,
    },
    "lincosamide antibiotic": {
        "desc": "Les lincosamides se lient à la portion 23S du ribosome 50S bactérien et inhibent l'allongement peptidique précoce en bloquant la réaction de transpeptidation.",
        "genes": 108,
    },
    "macrolide antibiotic": {
        "desc": "Les macrolides possèdent un grand cycle lactonique macrocyclique. Ils se lient à la sous-unité 50S du ribosome bactérien et inhibent la synthèse des protéines essentielles.",
        "genes": 212,
    },
    "moenomycin antibiotic": {
        "desc": "Les moenomycines sont des phosphoglycolipides qui inhibent les glycosyltransférases du peptidoglycane pour bloquer la biosynthèse de la paroi bactérienne.",
        "genes": 2,
    },
    "monobactam": {
        "desc": "Les monobactames sont des bêta-lactamines monocycliques bactéricides à large spectre, très résistants aux bêta-lactamases. Ils inhibent la synthèse de la couche peptidoglycane de la paroi bactérienne.",
        "genes": 1310,
    },
    "mupirocin-like antibiotic": {
        "desc": "Groupe d'antibiotiques comprenant la mupirocine et les mélanges similaires. La mupirocine inhibe l'isoleucyl-ARNt synthétase, bloquant la synthèse protéique.",
        "genes": 11,
    },
    "nitrofuran antibiotic": {
        "desc": "Les nitrofuranes sont des agents chimiothérapeutiques à activité antibactérienne et antiprotozoaire. Ils agissent en endomageant l'ADN bactérien via des métabolites réactifs.",
        "genes": 18,
    },
    "nitroimidazole antibiotic": {
        "desc": "Les nitroimidazoles ont une activité antiprotozoaire et antibactérienne. Ils génèrent des radicaux nitro réactifs par réduction anaérobie qui endommagent l'ADN bactérien.",
        "genes": 18,
    },
    "nucleoside antibiotic": {
        "desc": "Les antibiotiques nucléosidiques sont composés de nucléosides et nucléotides modifiés avec diverses activités et mécanismes d'action antibactériens.",
        "genes": 14,
    },
    "orthosomycin antibiotic": {
        "desc": "Les orthosomycines ciblent la sous-unité ribosomique 70S. Utilisées principalement en médecine vétérinaire et pour la recherche expérimentale.",
        "genes": 6,
    },
    "oxazolidinone antibiotic": {
        "desc": "Les oxazolidinones inhibent la synthèse protéique en se liant au domaine V de l'ARNr 23S de la sous-unité ribosomique 50S. Le linézolide est le seul représentant en usage clinique.",
        "genes": 18,
    },
    "pactamycin-like antibiotic": {
        "desc": "Groupe d'antibiotiques comprenant la pactamycine et ses dérivés, inhibant la traduction ribosomique.",
        "genes": 2,
    },
    "penicillin beta-lactam": {
        "desc": "Les pénicillines sont des antibiotiques bêta-lactamines historiques dérivés de champignons Penicillium. Elles inhibent la synthèse du peptidoglycane de la paroi bactérienne en se liant aux PBPs (Penicillin-Binding Proteins).",
        "genes": 3115,
    },
    "peptide antibiotic": {
        "desc": "Les antibiotiques peptidiques ont des mécanismes variés selon leur composition, mais la plupart perturbent la membrane cellulaire. Les lipopeptides incluent des chaînes lipidiques supplémentaires.",
        "genes": 187,
    },
    "phenicol antibiotic": {
        "desc": "Les phénicols sont des antibiotiques bactériostatiques à large spectre. Ils bloquent l'allongement peptidique en se liant au centre peptidyltransférase du ribosome 70S.",
        "genes": 140,
    },
    "phosphonic acid antibiotic": {
        "desc": "Groupe d'antibiotiques dérivés d'acides phosphoniques. La fosfomycine inhibe MurA, la première enzyme de la biosynthèse du peptidoglycane.",
        "genes": 48,
    },
    "pleuromutilin antibiotic": {
        "desc": "Les pleuromutilins sont des produits naturels fongiques qui ciblent la traduction bactérienne en se liant à l'ARNr 23S et bloquant le site P du ribosome. Principalement utilisés en agriculture et médecine vétérinaire.",
        "genes": 8,
    },
    "polyamine antibiotic": {
        "desc": "Les antibiotiques polyamines sont des composés organiques possédant deux ou plusieurs groupes amino primaires avec une activité antimicrobienne.",
        "genes": 4,
    },
    "pyrazine antibiotic": {
        "desc": "Groupe d'antibiotiques dérivés du pyrazine, incluant le pyrazinamide utilisé contre la tuberculose.",
        "genes": 5,
    },
    "rifamycin antibiotic": {
        "desc": "Les rifamycines sont des antibiotiques ansamycines à large spectre qui inhibent l'ARN polymérase bactérienne en se liant à une région hautement conservée, bloquant le tunnel de sortie des oligonucléotides.",
        "genes": 63,
    },
    "salicylic acid antibiotic": {
        "desc": "Groupe d'antibiotiques dérivés de l'acide salicylique avec des propriétés antimicrobiennes.",
        "genes": 3,
    },
    "streptogramin A antibiotic": {
        "desc": "Les streptogramines A sont des hybrides cyclopeptidiques polyketides qui se lient au centre de transfert peptidique du ribosome. Seules, elles sont bactériostatiques, mais bactéricides en association avec les streptogramines B.",
        "genes": 53,
    },
    "streptogramin B antibiotic": {
        "desc": "Les streptogramines B bloquent le tunnel de sortie des peptides du ribosome 50S. Seules, elles sont bactériostatiques, mais bactéricides en association avec les streptogramines A.",
        "genes": 37,
    },
    "streptogramin antibiotic": {
        "desc": "Les streptogramines sont des produits naturels de Streptomyces. Elles se lient au site P de la sous-unité 50S pour inhiber la synthèse protéique. La famille comprend deux sous-groupes A et B produits simultanément dans un ratio 70:30.",
        "genes": 99,
    },
    "sulfonamide antibiotic": {
        "desc": "Les sulfonamides sont des antibiotiques synthétiques à large spectre qui inhibent la dihydroptéroate synthase, perturbant la biosynthèse de l'acide tétrahydrofolique essentiel à la synthèse des nucléotides.",
        "genes": 10,
    },
    "sulfone antibiotic": {
        "desc": "Les sulfones sont actives contre un large spectre bactérien, principalement utilisées contre Mycobacterium leprae. Leur mécanisme implique l'inhibition de la synthèse de l'acide folique.",
        "genes": 7,
    },
    "tetracycline antibiotic": {
        "desc": "Les tétracyclines sont des antibiotiques polyketides qui inhibent la sous-unité ribosomique 30S en empêchant la liaison de l'aminoacyl-ARNt au site accepteur du ribosome.",
        "genes": 186,
    },
    "thioamide antibiotic": {
        "desc": "Groupe d'antibiotiques possédant le groupe fonctionnel thioamide. Ils inhibent la synthèse des acides mycoliques dans les mycobactéries.",
        "genes": 5,
    },
    "thiosemicarbazone antibiotic": {
        "desc": "Groupe d'antibiotiques dérivés du thiosemicarbazide, possédant le groupe fonctionnel thiosemicarbazone avec activité antimycobactérienne.",
        "genes": 3,
    },
    "zoliflodacin-like antibiotic": {
        "desc": "Groupe d'antibiotiques incluant le composé expérimental zoliflodacin et ses dérivés. Ils inhibent la topoisomérase II bactérienne par un mécanisme distinct des fluoroquinolones.",
        "genes": 2,
    },
}


def get_distribution_data():
    data = {
        "Classe": list(CARD_ARO_GENES.keys()),
        "Gènes ARO": list(CARD_ARO_GENES.values()),
        "Activité": [
            "Bactéricide",
            "Bactéricide",
            "Bactéricide",
            "Bactéricide",
            "Double activité",
            "Double activité",
            "Bactériostatique",
            "Non déterminé",
            "Bactériostatique",
            "Bactériostatique",
            "Bactériostatique",
            "Bactéricide",
            "Bactériostatique",
            "Bactéricide",
            "Bactéricide",
            "Double activité",
            "Double activité",
            "Bactéricide",
            "Bactériostatique",
        ],
    }
    return pd.DataFrame(data)


def get_card_stats():
    return {
        "total": CARD_TOTAL_CLASSES,
        "bactericide_strict": CARD_BACTERICIDE_STRICT,
        "bactericide": CARD_BACTERICIDE_COUNT,
        "bacteriostatic": CARD_BACTERIOSTATIC_COUNT,
        "undetermined": CARD_UNDETERMINED,
        "pct_bactericide": 22,
        "pct_bactericide_strict": 17,
        "pct_bacteriostatic": 20,
        "pct_undetermined": 57,
    }


def get_llm_comparison_data():
    data = {
        "Classe ATB (CARD)": [
            "Aminoglycoside antibiotic",
            "Carbapenem",
            "Cephalosporin",
            "Fluoroquinolone antibiotic",
            "Glycopeptide antibiotic",
            "Rifamycin antibiotic",
            "Macrolide antibiotic",
            "Oxazolidinone antibiotic",
            "Lincosamide antibiotic",
            "Phenicol antibiotic",
            "Streptogramin A antibiotic",
            "Streptogramin B antibiotic",
        ],
        "Molécule représentative": [
            "Gentamicin",
            "Meropenem",
            "Ceftriaxone",
            "Ciprofloxacin",
            "Vancomycin",
            "Rifampicin",
            "Azithromycin",
            "Linezolid",
            "Clindamycin",
            "Chloramphenicol",
            "Virginiamycin M",
            "Quinupristin",
        ],
        "Ratio CMB/CMI": [
            2.40,
            2.58,
            0.25,
            3.00,
            4.00,
            3.00,
            2.60,
            4.00,
            4.00,
            4.00,
            2.00,
            2.50,
        ],
        "BioGPT": ["⚠️ Bactéricide (biais)"] * 12,
        "BioMedLM": (["✅ Bactéricide"] * 6 + ["❌ Incohérent"] * 6),
        "Littérature (réf.)": [
            "⚡ Double activité",
            "✅ Bactéricide strict",
            "✅ Bactéricide strict",
            "⚡ Double activité",
            "✅ Bactéricide strict",
            "✅ Bactéricide strict",
            "❌ Bactériostatique",
            "❌ Bactériostatique",
            "❌ Bactériostatique",
            "❌ Bactériostatique",
            "❌ Bactériostatique",
            "❌ Bactériostatique",
        ],
        "Validation finale": [
            "⚡",
            "✅",
            "✅",
            "⚡",
            "✅",
            "✅",
            "❌",
            "❌",
            "❌",
            "❌",
            "❌",
            "❌",
        ],
    }
    return pd.DataFrame(data)


def get_validated_results():
    data = {
        "Classe ATB (CARD)": BACTERICIDAL_CLASSES,
        "Mécanisme principal": [
            "Inhibition synthèse paroi (PBP) – β-lactamine",
            "Inhibition synthèse paroi (PBP) – β-lactamine",
            "Inhibition synthèse paroi (PBP) – β-lactamine historique",
            "Liaison D-Ala-D-Ala → inhibition paroi (VanA/VanB)",
            "Lésions ADN par réduction anaérobie (radicaux nitroso)",
            "Inhibition ARN polymérase (rpoB) – transcription",
            "Inhibition synthèse paroi PBP3 – β-lactamine monocyclique",
            "Inhibition synthèse paroi (MurA/MurZ) – fosfomycine",
        ],
        "Molécule clé": [
            "Meropenem",
            "Ceftriaxone",
            "Amoxicillin",
            "Vancomycin",
            "Metronidazole",
            "Rifampicin",
            "Aztreonam",
            "Fosfomycin",
        ],
        "Ratio CMB/CMI": [2.58, 0.25, "≤ 4", 4.00, "≤ 4", 3.00, "≤ 4", "≤ 4"],
        "App.1 ARO": ["✓"] * 8,
        "App.2 Réf.": ["✓"] * 8,
        "App.2 ATC": ["✓", "✓", "✓", "✓", "—", "—", "✓", "—"],
        "App.3 MDR": ["✓", "✓", "✓", "✓", "—", "—", "—", "—"],
        "Littérature": ["✓"] * 8,
        "Priorité ★": ["★★★", "★★★", "★★★", "★★★", "★★", "★★", "★★", "★★"],
    }
    return pd.DataFrame(data)


def get_approche1_results():
    return [
        "Carbapenem",
        "Cephalosporin",
        "Penicillin Beta-Lactam",
        "Fluoroquinolone antibiotic",
        "Monobactam",
        "Tetracycline Antibiotic",
        "Rifamycin Antibiotic",
    ]


def get_mdr_data():
    data = {
        "Classe": [
            "Penicillin beta-lactam",
            "Cephalosporin",
            "Carbapenem",
            "Monobactam",
            "Macrolide antibiotic",
            "Fluoroquinolone antibiotic",
            "Tetracycline antibiotic",
            "Streptogramin antibiotic",
            "Lincosamide antibiotic",
            "Phenicol antibiotic",
            "Disinfecting agents",
            "Aminoglycoside antibiotic",
            "Streptogramin A",
            "Glycylcycline",
            "Streptogramin B",
            "Rifamycin antibiotic",
        ],
        "Gènes MDR (seuil≥2)": [
            2526,
            2463,
            2388,
            1310,
            142,
            133,
            102,
            99,
            93,
            85,
            66,
            59,
            53,
            37,
            37,
            35,
        ],
        "Dans TOP genes (score=13)": [
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
        ],
    }
    return pd.DataFrame(data)
