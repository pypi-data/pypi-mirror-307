# import warnings
import pandas as pd
from Bio.PDB.Polypeptide import is_nucleic
from Bio.PDB.Polypeptide import is_aa
from Bio.PDB.Structure import Structure


def get_polymer_dataframe(structure: Structure) -> pd.DataFrame:
    """
    Return dataframe with polymer data from a Biopython structure object.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        Biopython structure object.

    Returns
    -------
    pandas.DataFrame
        Dataframe with polymer data in the structure.

    """
    data = []

    for chain in structure.get_chains():
        nucleotide_counter = 0
        aa_counter = 0
        water_counter = 0
        other_counter = 0

        for residue in chain:
            # it's a nucleotide
            # TODO distinguish between DNA and RNA
            if is_nucleic(residue):
                nucleotide_counter += 1
            # it's an aminoacid
            elif is_aa(residue):
                aa_counter += 1
            # it's water
            elif residue.resname == "HOH":
                water_counter += 1
            # it's something else
            else:
                other_counter += 1

        # stats = (nucleotide_counter, aa_counter,
        #          water_counter, other_counter)
        tot = nucleotide_counter + aa_counter + other_counter

        if nucleotide_counter / tot > 0.7:
            data.append((chain.id, "polymer_nucleic"))
        elif aa_counter / tot > 0.7:
            data.append((chain.id, "polymer_protein"))
        else:
            # warnings.warn(
            # f"Unknown polymer. id = {structure.id}, chain = \
            # {chain.id}, stats = {stats}"
            #             )
            data.append((chain.id, "unknown"))

    df = pd.DataFrame(data, columns=["chain_id", "polymer_type"])

    return df
    # TODO
    # "non_standard_linkage": non_standard_linkage,
    # "non_standard_residue": non_standard_residue,
