import pandas as pd
from Bio.PDB.Structure import Structure

# absolute import
from PDBNucleicAcids.utils import get_paired_segments
from PDBNucleicAcids.Pairing import search_paired_base
from PDBNucleicAcids._polymer_dataframe import get_polymer_dataframe


def get_basepair_dataframe(
    structure: Structure,
    nucleic_chain_ids: list[str] | None = None,
) -> pd.DataFrame:
    """
    Return dataframe with base pairs data from a Biopython structure object.

    Parameters
    ----------
    structure : Bio.PDB.Structure.Structure
        Biopython structure object.
    nucleic_chains : list[str] | None, optional
        List that contain chain ids of nucleic acid polymers. If `None` then
        they will be inferred using `polymer_dataframe_from_structure`.

    Returns
    -------
    pandas.DataFrame
        Dataframe with base pairs data in the structure.

    """
    # in case no nucleic chain ids were given
    # get nucleic chains using get_polymer_dataframe
    if nucleic_chain_ids is None:
        # polymer chain data
        polymer_df: pd.DataFrame = get_polymer_dataframe(structure)

        # select only nucleic chains
        nucleic_chain_ids: list[str] = polymer_df[
            polymer_df["polymer_type"] == "polymer_nucleic"
        ]["chain_id"].tolist()

    # list of all nucleic atoms, compute only once
    nucleic_atoms: list = [
        atom
        for atom in structure.get_atoms()
        if atom.parent.parent.id in nucleic_chain_ids
    ]

    # output data
    data: list[tuple[str, int]] = []

    for chain in structure.get_chains():
        if chain.id not in nucleic_chain_ids:
            continue
        for residue in chain:
            i_residue = residue
            j_residue = search_paired_base(
                i_residue, nucleic_atoms=nucleic_atoms
            )

            # in this case there is no base pair
            if j_residue is None:
                continue

            row: tuple[str, int] = (
                i_residue.parent.id,
                i_residue.id[1],
                i_residue.resname,
                j_residue.resname,
                j_residue.id[1],
                j_residue.parent.id,
            )

            # Look if it's on the data list
            if row not in data and row[::-1] not in data:
                data.append(row)

    base_pairs_df = pd.DataFrame(
        data,
        columns=[
            "i_chain_id",
            "i_residue_index",
            "i_residue_name",
            "j_residue_name",
            "j_residue_index",
            "j_chain_id",
        ],
    )

    # Add a column with an index that indicates a paired segment
    # i.e.
    # A  T  0
    # C  G  0
    # C  G  0
    # T  A  1
    base_pairs_df["paired_segment"] = get_paired_segments(base_pairs_df)

    return base_pairs_df
