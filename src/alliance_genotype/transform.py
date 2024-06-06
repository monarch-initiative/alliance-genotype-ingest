import uuid # For generating UUIDs for associations

from biolink_model.datamodel.pydanticmodel_v2 import (Genotype,
                                                      GenotypeToVariantAssociation,
                                                      KnowledgeLevelEnum,
                                                      AgentTypeEnum)
from koza.cli_utils import get_koza_app

koza_app = get_koza_app("alliance_genotype")

source_map = {
    "FB": "infores:flybase",
    "MGI": "infores:mgi",
    "RGD": "infores:rgd",
    "HGNC": "infores:rgd",  # Alliance contains RGD curation of human genes
    "SGD": "infores:sgd",
    "WB": "infores:wormbase",
    "Xenbase": "infores:xenbase",
    "ZFIN": "infores:zfin",
}

while (row := koza_app.get_row()) is not None:
    # Code to transform each row of data
    # For more information, see https://koza.monarchinitiative.org/Ingests/transform
#    print(row)
#    print(row["crossReference"])
#    print([xref.id for xref in row["crossReference"]])
    genotype = Genotype(
        id=row["primaryID"],
        type=[row["subtype"]] if "subtype" in row else None,
        name=row["name"],
        in_taxon=[row["taxonId"]],
    )
    entities = [genotype]

    for allele in row["affectedGenomicModelComponents"] if "affectedGenomicModelComponents" in row else []:
        genotype_to_variant_association = GenotypeToVariantAssociation(
            id=str(uuid.uuid4()),
            subject=genotype.id,
            predicate="biolink:has_variant_participant",
            object=allele["alleleID"],
            qualifier=allele["zygosity"] if "zygosity" in allele else None,
            primary_knowledge_source=source_map[row["objectId"].split(':')[0]],
            aggregator_knowledge_source=["infores:monarchinitiative", "infores:agrkb"],
            knowledge_level=KnowledgeLevelEnum.knowledge_assertion,
            agent_type=AgentTypeEnum.manual_agent,
        )
        entities.append(genotype_to_variant_association)

    koza_app.write(*entities)
