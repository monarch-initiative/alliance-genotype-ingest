import duckdb 


db = duckdb.connect(database=':memory:', read_only=False)
db.execute("""
copy (
  select distinct AlleleId, AlleleAssociatedGeneId
  from read_csv_auto('data/VARIANT-ALLELE_*.tsv.gz', comment='#', ignore_errors=true)
  where AlleleAssociatedGeneId is not null
) to 'data/allele_to_gene.tsv' (header true, delimiter '\t');
""")