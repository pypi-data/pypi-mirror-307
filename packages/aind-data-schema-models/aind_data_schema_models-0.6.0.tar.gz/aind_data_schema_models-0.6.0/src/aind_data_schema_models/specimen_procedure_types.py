"""Specimen procedure types"""

from enum import Enum


class SpecimenProcedureType(str, Enum):
    """Specimen procedures"""

    CLEARING = "Clearing"
    DELIPIDATION = "Delipidation"
    EMBEDDING = "Embedding"
    EXPANSION = "Expansion"
    FIXATION = "Fixation"
    FIXATION_AND_PERMEABILIZATION = "Fixation and permeabilization"
    GELATION = "Gelation"
    HYBRIDICATION_AND_AMPLIFICATION = "Hybridication and amplification"
    HYBRIDIZATION_CHAIN_REACTION = "Hybridization Chain Reaction"
    IMMUNOLABELING = "Immunolabeling"
    MOUNTING = "Mounting"
    OTHER = "Other"
    REFRACTIVE_INDEX_MATCHING = "Refractive index matching"
    SECTIONING = "Sectioning"
    SOAK = "Soak"
    STORAGE = "Storage"
    STRIPPING = "Stripping"
    TAMOXIFEN_INDUCTION = "Tamoxifen induction"
