# alliance-genotype Report

{{ get_nodes_report() }}

{{ get_edges_report() }}

{ % include 'docs/nodes_report.md' %}
{ % include 'docs/edges_report.md' %}

# Alliance Genotype Ingest Pipeline

This pipeline converts Alliance AGM files from MGI, ZFIN & RGD to KGX TSV following the Biolink Model.

The source files (AGM_{MGI,ZFIN,RGD}.json) provide associations to Alleles as well, but those edges are not currently captured. 

Example transform:
```
 {
     'primaryID': 'ZFIN:ZDB-FISH-150901-9455', 
      'name': 'acvr1l<sup>sk42/sk42</sup>; f2Tg',
      'affectedGenomicModelComponents': [
            {'alleleID': 'ZFIN:ZDB-ALT-060821-6', 'zygosity': 'GENO:0000137'},
            {'alleleID': 'ZFIN:ZDB-ALT-100701-1', 'zygosity': 'GENO:0000136'}],
       'crossReference': { 'id': 'ZFIN:ZDB-FISH-150901-9455', 'pages': ['Fish']}, 
       'taxonId': 'NCBITaxon:7955'
}
```

Is transformed into
```
    category: biolink:Genotype
    id: ZFIN:ZDB-FISH-150901-9455
    name: acvr1l<sup>sk42/sk42</sup>; f2Tg
    in_taxon: NCBITaxon:7955
    in_taxon_label: Danio rerio
```
