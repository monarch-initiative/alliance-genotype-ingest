#! /bin/bash

echo "# alliance-genotype Report" >docs/index.md
echo "" >> docs/index.md
echo "## Nodes" >>docs/index.md
echo "" >> docs/index.md
duckdb -markdown -s "select category, split_part(id, ':', 1) as prefix, count(*) from 'output/alliance_genotype_nodes.tsv' group by all order by all" >>docs/index.md
echo "" >> docs/index.md
echo "## Edges" >>docs/index.md
echo "" >> docs/index.md
duckdb -markdown -s "select category, split_part(subject, ':', 1) as subject_prefix, predicate, split_part(object, ':', 1) as object_prefix, count(*) from 'output/alliance_genotype_edges.tsv' group by all order by all" >>docs/index.md
