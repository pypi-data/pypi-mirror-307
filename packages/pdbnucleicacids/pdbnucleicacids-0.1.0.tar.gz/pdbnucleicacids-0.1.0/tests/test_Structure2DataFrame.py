"""Testing the Structure2DataFrame module from PDBNucleicAcids."""

# import pytest
from Bio.PDB.MMCIFParser import MMCIFParser

# to be tested
from PDBNucleicAcids.Structure2DataFrame import get_basepair_dataframe


def get_test_structure():
    filepath = "tests/data/gattaca.cif"
    parser = MMCIFParser(QUIET=True)
    structure = parser.get_structure("gattaca", filepath)

    return structure


def test_invalid_residue():
    """Test per verificare il comportamento con residuo non nucleico."""
    structure = get_test_structure()

    df = get_basepair_dataframe(structure)
    print(df)

    assert True
