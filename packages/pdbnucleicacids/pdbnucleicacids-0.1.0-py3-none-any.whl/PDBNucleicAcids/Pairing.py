"""Single base pairing."""

from Bio.PDB.Structure import Structure
from Bio.PDB.Residue import Residue
from Bio.PDB.Atom import Atom
from Bio.PDB.NeighborSearch import NeighborSearch

# absolute imports
from PDBNucleicAcids._polymer_dataframe import get_polymer_dataframe
from PDBNucleicAcids.BasePairRules import dsDNAWatsonCrickBasePairRules


def search_paired_base(
    residue: Residue,
    nucleic_chain_ids: list[str] | None = None,
    nucleic_atoms: list[Atom] | None = None,
    pairing_rules=dsDNAWatsonCrickBasePairRules,
) -> Residue | None:
    """
    Search in the vicinity of a given base for its paired base.

    Parameters
    ----------
    residue : Bio.PDB.Residue.Residue
        A Biopython nucleic acid residue (nucleotide) taken from a Biopython
        structure.
    nucleic_chain_ids : list[str], optional
        List of ids for nucleic acid chains. If None they will be
        inferred using polymer_dataframe_from_structure(). Default is None.
    nucleic_atoms : list[Atom], optional
        List of atoms from the nucleic acid chains. If None they will be
        inferred using nucleic_chain_ids(). Default is None.
    pairing_rules : optional
        Class instance with rules for proper pairing.
        PDBNucleicAcids.BasePairsRules.WatsonCrickBasePairsRules
        is the default. Currently it might work only with those rules

    Returns
    -------
    Bio.PDB.Residue.Residue | None
        Nucleotide that binds to the input nucleotide residue.
        None in the case there is no nucleotide paired to the input nucleotide.

    """
    # from residue get to the structure
    structure: Structure = residue.parent.parent.parent

    # in case no nucleic atoms and no nucleic chain ids were given
    # get nucleic chains using get_polymer_dataframe
    if not nucleic_atoms and not nucleic_chain_ids:
        polymer_df = get_polymer_dataframe(structure)
        nucleic_chain_ids = polymer_df[
            polymer_df["polymer_type"] == "polymer_nucleic"
        ]["chain_id"].tolist()

    # in case no nucleic atoms were given but
    # nucleic chain ids were given or got from get_polymer_dataframe
    # list of all nucleic atoms, compute only once
    if not nucleic_atoms and nucleic_chain_ids:
        nucleic_atoms: list[Atom] = [
            atom
            for atom in structure.get_atoms()
            if atom.parent.parent.id in nucleic_chain_ids
            and atom.parent != residue  # not from the same residue
        ]

    # if there are no nucleic atoms except from the one input residue
    # then NeighborSearch will return an error
    if len(nucleic_atoms) == 0 or nucleic_atoms is None:
        return None

    # initialize NeighborSearch class
    ns = NeighborSearch(nucleic_atoms)

    # initialize Rules class
    pairing_rules = pairing_rules()

    central_atom: Atom = pairing_rules.atom_from_central_hbond(residue)
    # if the input residue is not a DNA base then the central atom
    # will be None
    if central_atom is None:
        return None

    # search around the central atom of the residue
    atom_neighborhood = ns.search(center=central_atom.coord, radius=4.0)

    residue_neighborhood: list[Residue] = list(
        {atom.parent for atom in atom_neighborhood}
    )

    candidate_residues: list[Residue] = []

    for residue_neighbour in residue_neighborhood:
        if pairing_rules.is_candidate(base1=residue, base2=residue_neighbour):
            dist = pairing_rules.distance(
                base1=residue, base2=residue_neighbour
            )
            candidate_residues.append((residue_neighbour, dist))

    if len(candidate_residues) > 1:
        # If there is more than one paired residue
        min_tuple: tuple = min(candidate_residues, key=lambda x: x[1])
        return min_tuple[0]
    elif candidate_residues:
        # only one paired nucleotide found
        return candidate_residues[0][0]
    else:
        # no paired nucleotides found
        return None
