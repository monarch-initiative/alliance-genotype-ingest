"""
This is an example test file for the transform script. 
It uses pytest fixtures to define the input data and the mock koza transform. 
The test_example function then tests the output of the transform script.

See the Koza documentation for more information on testing transforms:
https://koza.monarchinitiative.org/Usage/testing/
"""
import pytest 

from koza.utils.testing_utils import mock_koza

# Define the ingest name and transform script path
INGEST_NAME = "alliance_genotype"
TRANSFORM_SCRIPT = "./src/alliance_genotype/transform.py"


# Or a list of rows
@pytest.fixture
def zfin_row():
    return {'primaryID': 'ZFIN:ZDB-FISH-150901-9455', 'name': 'acvr1l<sup>sk42/sk42</sup>; f2Tg',
            'affectedGenomicModelComponents': [{'alleleID': 'ZFIN:ZDB-ALT-060821-6', 'zygosity': 'GENO:0000137'},
                                               {'alleleID': 'ZFIN:ZDB-ALT-100701-1', 'zygosity': 'GENO:0000136'}],
            'crossReference': {'id': 'ZFIN:ZDB-FISH-150901-9455', 'pages': ['Fish']}, 'taxonId': 'NCBITaxon:7955'}



# Define the mock koza transform
@pytest.fixture
def mgi_transform(mock_koza):
    mgi_row = {'primaryID': 'MGI:3626201', 'subtype': 'genotype',
         'name': 'Ep300<sup>tm3Pkb</sup>/Ep300<sup>+</sup> Tg(IghMyc)22Bri/0  [background:] involves: 129S6/SvEvTac * C57BL * SJL',
         'taxonId': 'NCBITaxon:10090', 'crossReference': {'id': 'MGI:3626201', 'pages': ['genotype']},
         'affectedGenomicModelComponents': [{'alleleID': 'MGI:3612049', 'zygosity': 'GENO:0000135'},
                                            {'alleleID': 'MGI:2447604', 'zygosity': 'GENO:0000606'}]}

    return mock_koza(
        INGEST_NAME,
        mgi_row,
        TRANSFORM_SCRIPT,
    )

def test_mgi_transform_genotype(mgi_transform):
    entities = mgi_transform
    genotypes = [entity for entity in entities if 'biolink:Genotype' in entity.category]
    genotype = genotypes[0]
    assert genotype.id == 'MGI:3626201'
    assert genotype.name == 'Ep300<sup>tm3Pkb</sup>/Ep300<sup>+</sup> Tg(IghMyc)22Bri/0  [background:] involves: 129S6/SvEvTac * C57BL * SJL'
    assert genotype.in_taxon == ['NCBITaxon:10090']


def test_mgi_transform_associations(mgi_transform):
    entities = mgi_transform
    associations = [entity for entity in entities if 'biolink:GenotypeToVariantAssociation' in entity.category]
    assert len(associations) == 2

    association_1 = associations[0]
    assert association_1.subject == 'MGI:3626201'
    assert association_1.object == 'MGI:3612049'
    assert association_1.qualifier == 'GENO:0000135'

    association_2 = associations[1]
    assert association_2.subject == 'MGI:3626201'
    assert association_2.object == 'MGI:2447604'
    assert association_2.qualifier == 'GENO:0000606'
