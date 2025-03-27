"""
This is an example test file for the transform script. 
It uses pytest fixtures to define the input data and the mock koza transform. 
The test_example function then tests the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""
import pytest
from biolink_model.datamodel.pydanticmodel_v2 import Genotype, GenotypeToVariantAssociation

# Define the ingest name and transform script path
INGEST_NAME = "alliance_genotype"
TRANSFORM_SCRIPT = "./src/alliance_genotype/genotype.py"


# Or a list of rows
@pytest.fixture
def zfin_entities(mock_koza):
    row = {
        'primaryID': 'ZFIN:ZDB-FISH-150901-9455',
        'name': 'acvr1l<sup>sk42/sk42</sup>; f2Tg',
        'affectedGenomicModelComponents': [
            {'alleleID': 'ZFIN:ZDB-ALT-060821-6', 'zygosity': 'GENO:0000137'},
            {'alleleID': 'ZFIN:ZDB-ALT-100701-1', 'zygosity': 'GENO:0000136'},
        ],
        'crossReference': {'id': 'ZFIN:ZDB-FISH-150901-9455', 'pages': ['Fish']},
        'taxonId': 'NCBITaxon:7955',
    }

    return mock_koza(
        INGEST_NAME,
        row,
        TRANSFORM_SCRIPT,
    )


# Define the mock koza transform
@pytest.fixture
def mgi_entities(mock_koza):
    mgi_row = {
        'primaryID': 'MGI:3626201',
        'subtype': 'genotype',
        'name': 'Ep300<sup>tm3Pkb</sup>/Ep300<sup>+</sup> Tg(IghMyc)22Bri/0  [background:] involves: 129S6/SvEvTac * C57BL * SJL',
        'taxonId': 'NCBITaxon:10090',
        'crossReference': {'id': 'MGI:3626201', 'pages': ['genotype']},
        'affectedGenomicModelComponents': [
            {'alleleID': 'MGI:3612049', 'zygosity': 'GENO:0000135'},
            {'alleleID': 'MGI:2447604', 'zygosity': 'GENO:0000606'},
        ],
    }

    return mock_koza(
        INGEST_NAME,
        mgi_row,
        TRANSFORM_SCRIPT,
    )


def test_mgi_transform_genotype(mgi_entities):
    entities = mgi_entities
    genotypes = [entity for entity in entities if isinstance(entity, Genotype)]
    genotype = genotypes[0]
    assert genotype.id == 'MGI:3626201'
    assert (
        genotype.name
        == 'Ep300<sup>tm3Pkb</sup>/Ep300<sup>+</sup> Tg(IghMyc)22Bri/0  [background:] involves: 129S6/SvEvTac * C57BL * SJL'
    )
    assert genotype.in_taxon == ['NCBITaxon:10090']
    assert genotype.in_taxon_label == 'Mus musculus'


def test_zfin_transform_genotype(zfin_entities):
    entities = zfin_entities
    genotypes = [entity for entity in entities if isinstance(entity, Genotype)]
    assert len(genotypes) == 1
    genotype = genotypes[0]
    assert genotype.id == 'ZFIN:ZDB-FISH-150901-9455'
    assert genotype.name == 'acvr1l<sup>sk42/sk42</sup>; f2Tg'
    assert genotype.in_taxon == ['NCBITaxon:7955']
    assert genotype.in_taxon_label == 'Danio rerio'


def test_zfin_transform_associations(zfin_entities):
    entities = zfin_entities
    associations = [entity for entity in entities if isinstance(entity, GenotypeToVariantAssociation)]
    assert len(associations) == 2

    # Check first association
    assert associations[0].subject == 'ZFIN:ZDB-FISH-150901-9455'
    assert associations[0].predicate == 'biolink:has_variant_participant'
    assert associations[0].object == 'ZFIN:ZDB-ALT-060821-6'
    assert associations[0].qualifier == 'GENO:0000137'
    assert associations[0].primary_knowledge_source == 'infores:zfin'
    assert set(associations[0].aggregator_knowledge_source) == {'infores:monarchinitiative', 'infores:agrkb'}

    # Check second association
    assert associations[1].subject == 'ZFIN:ZDB-FISH-150901-9455'
    assert associations[1].predicate == 'biolink:has_variant_participant'
    assert associations[1].object == 'ZFIN:ZDB-ALT-100701-1'
    assert associations[1].qualifier == 'GENO:0000136'
    assert associations[1].primary_knowledge_source == 'infores:zfin'
    assert set(associations[1].aggregator_knowledge_source) == {'infores:monarchinitiative', 'infores:agrkb'}


def test_mgi_transform_associations(mgi_entities):
    entities = mgi_entities
    associations = [entity for entity in entities if isinstance(entity, GenotypeToVariantAssociation)]
    assert len(associations) == 2

    # Check first association
    assert associations[0].subject == 'MGI:3626201'
    assert associations[0].predicate == 'biolink:has_variant_participant'
    assert associations[0].object == 'MGI:3612049'
    assert associations[0].qualifier == 'GENO:0000135'
    assert associations[0].primary_knowledge_source == 'infores:mgi'
    assert set(associations[0].aggregator_knowledge_source) == {'infores:monarchinitiative', 'infores:agrkb'}

    # Check second association
    assert associations[1].subject == 'MGI:3626201'
    assert associations[1].predicate == 'biolink:has_variant_participant'
    assert associations[1].object == 'MGI:2447604'
    assert associations[1].qualifier == 'GENO:0000606'
    assert associations[1].primary_knowledge_source == 'infores:mgi'
    assert set(associations[1].aggregator_knowledge_source) == {'infores:monarchinitiative', 'infores:agrkb'}
