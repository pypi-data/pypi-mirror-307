"""Functions that address atom geometry."""

import numpy as np

# from Bio.PDB.Atom import Atom


def calculate_normal_vector(v1, v2, v3) -> np.float64:
    """Compute normal vector from three 3D points."""
    u1 = v2 - v1
    u2 = v3 - v1

    # Calcolo del vettore normale
    normal = np.cross(u1, u2)

    # Normalizzazione manuale del vettore normale
    norm = np.linalg.norm(normal)
    if norm == 0:
        raise ValueError("Vettore normale nullo")
    normal_normalized = normal / norm

    return normal_normalized


def angle_between_vectors(v1, v2) -> np.float64:
    """Compute angle between two vectors."""
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    return np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))


def angle_between_planes(plane1, plane2) -> np.float64:
    """Compute angle between two planes, composed of three 3D points each."""
    v1, v2, v3 = plane1
    v4, v5, v6 = plane2

    normal1 = calculate_normal_vector(v1, v2, v3)
    normal2 = calculate_normal_vector(v4, v5, v6)

    angle = angle_between_vectors(normal1, normal2)

    return angle


def plane_separation(plane1, plane2) -> np.float64:
    """Calcola la distanza verticale tra due piani."""
    v1, v2, v3 = plane1
    v4, v5, v6 = plane2

    # Ottieni i vettori normali
    normal1 = calculate_normal_vector(v1, v2, v3)
    # normal2 = calculate_normal_vector(v4, v5, v6)

    # Ottieni i centri dei piani
    center1 = np.mean(plane1, axis=0)
    center2 = np.mean(plane2, axis=0)

    # Calcola il vettore tra i centri dei due piani
    center_vector = center2 - center1

    # Proietta il vettore tra i centri lungo la direzione del normale del
    # primo piano
    separation: np.float64 = abs(np.dot(center_vector, normal1))

    return separation


# def angle_between_3_atoms(atom1: Atom, atom2: Atom, atom3: Atom) -> float:
#     """
#     Get angle in degrees between three atoms. OBSOLETE.

#     Atom 1 has the angle that is returned

#     Parameters
#     ----------
#     atom1 : Bio.PDB.Atom.Atom
#         First atom, on which the returned angle rests.
#     atom2 : Bio.PDB.Atom.Atom
#         Second atom.
#     atom3 : Bio.PDB.Atom.Atom
#         Third atom.

#     Returns
#     -------
#     float
#         Angle between the three atoms, measured in degrees.

#     """
#     # get coordinate vectors
#     p1: np.array = atom1.coord
#     p2: np.array = atom2.coord
#     p3: np.array = atom3.coord

#     # Calculate the vectors
#     v1 = p2 - p1  # from p1 to p2
#     v2 = p3 - p1  # from p1 to p3

#     # Calculate the angle in radians
#     # rule of the cosine
#     angle_radians = np.arccos(
#         np.clip(
#             np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)),
#             -1.0,
#             1.0,
#         )
#     )

#     # Convert to degrees, cast into float
#     angle_degrees = np.degrees(angle_radians)
#     angle_degrees = float(angle_degrees)

#     return angle_degrees


# def dihedral_angle_between_4_atoms(
#     atom1: Atom, atom2: Atom, atom3: Atom, atom4: Atom
# ) -> float:
#     """
#     Get dihedral angle in degrees between four atoms. OBSOLETE.

#     The first plane rests of the dihedral angle rests on the first three
#     atoms while the second rests on the last three. `atom1` and `atom2`
#     are in common between the two planes.

#     Parameters
#     ----------
#     atom1 : Bio.PDB.Atom.Atom
#         First atom.
#     atom2 : Bio.PDB.Atom.Atom
#         Second atom.
#     atom3 : Bio.PDB.Atom.Atom
#         Third atom.
#     atom4 : Bio.PDB.Atom.Atom
#         Forth atom.

#     Returns
#     -------
#     float
#         Dihedral angle between the four atoms, measured in degrees.

#     """
#     # Punti tridimensionali, 4 atomi
#     p1 = atom1.coord
#     p2 = atom2.coord
#     p3 = atom3.coord
#     p4 = atom4.coord

#     # Vettori tra i punti
#     v1 = p2 - p1
#     v2 = p3 - p2
#     v3 = p4 - p3

#     # Vettori normali ai piani
#     n1 = np.cross(v1, v2)
#     n2 = np.cross(v2, v3)

#     # Vettore di riferimento per la direzione
#     m = np.cross(n1, v2)

#     # Normalizzazione dei vettori
#     n1 /= np.linalg.norm(n1)
#     n2 /= np.linalg.norm(n2)
#     m /= np.linalg.norm(m)

#     # Calcola coseno e seno dell'angolo
#     cos_theta = np.dot(n1, n2)
#     sin_theta = np.dot(m, n2)

#     # Calcola l'angolo diedro
#     theta = np.arctan2(sin_theta, cos_theta)

#     # Converti l'angolo da radianti a gradi e castalo in float
#     theta_deg = np.degrees(theta)
#     theta_deg = float(theta_deg)

#     return theta_deg
