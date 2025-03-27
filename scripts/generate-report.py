from pathlib import Path

import duckdb

# Define file paths for both genotype and allele data
file_configs = [
    {
        "nodes_file": "output/alliance_genotype_nodes.tsv",
        "edges_file": "output/alliance_genotype_edges.tsv",
        "nodes_report": "output/alliance_genotype_nodes_report.tsv",
        "edges_report": "output/alliance_genotype_edges_report.tsv",
    },
    {
        "nodes_file": "output/alliance_allele_nodes.tsv",
        "edges_file": "output/alliance_allele_edges.tsv",
        "nodes_report": "output/alliance_allele_nodes_report.tsv",
        "edges_report": "output/alliance_allele_edges_report.tsv",
    },
]

# Process each set of files
for config in file_configs:
    # Generate nodes report
    if Path(config["nodes_file"]).exists():
        query = f"""
        SELECT category, split_part(id, ':', 1) as prefix, count(*)
        FROM '{config["nodes_file"]}'
        GROUP BY all
        ORDER BY all
        """
        duckdb.sql(f"""copy ({query}) to '{config["nodes_report"]}' (header, delimiter '\t')""")
        print(f"Generated report: {config['nodes_report']}")
    else:
        print(f"Input file not found: {config['nodes_file']}")

    # Generate edges report
    if Path(config["edges_file"]).exists():
        query = f"""
        SELECT category, split_part(subject, ':', 1) as subject_prefix, predicate,
        split_part(object, ':', 1) as object_prefix, count(*)
        FROM '{config["edges_file"]}'
        GROUP BY all
        ORDER BY all
        """
        duckdb.sql(f"""copy ({query}) to '{config["edges_report"]}' (header, delimiter '\t')""")
        print(f"Generated report: {config['edges_report']}")
    else:
        print(f"Input file not found: {config['edges_file']}")
