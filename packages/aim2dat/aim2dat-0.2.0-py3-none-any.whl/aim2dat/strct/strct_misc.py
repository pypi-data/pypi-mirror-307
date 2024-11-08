"""
Miscellaneous functions for the StructureCollection class.
"""

# Standard library imports:
import itertools
from typing import List

# Third party library imports:
import numpy as np

# Internal library imports:
from aim2dat.utils.maths import calc_angle
from aim2dat.strct.strct_super_cell import _create_supercell_positions


def calculate_distance(
    structure,
    site_index1,
    site_index2,
    backfold_positions,
    use_supercell=False,
    r_max=0.0,
    return_pos=False,
):
    """Calculate distance."""
    if use_supercell:
        distance, pos = _calc_atomic_distance_sc(structure, site_index1, site_index2, r_max)
    else:
        distance, pos = _calc_atomic_distance(
            structure, site_index1, site_index2, backfold_positions
        )

    output = (None, (distance, pos)) if return_pos else (None, distance)
    return output


def calculate_angle(structure, site_index1, site_index2, site_index3, backfold_positions):
    """Calculate angle between three atomic positions."""
    _check_site_indices(structure, (site_index1, site_index2, site_index3))

    *_, pos2 = _calc_atomic_distance(structure, site_index1, site_index2, backfold_positions)
    *_, pos3 = _calc_atomic_distance(structure, site_index1, site_index3, backfold_positions)
    pos1 = np.array(structure["positions"][site_index1])
    return None, calc_angle(pos2 - pos1, pos3 - pos1) * 180.0 / np.pi


def calculate_dihedral_angle(
    structure, site_index1, site_index2, site_index3, site_index4, backfold_positions
):
    """Calculate dihedral angle between four atomic positions."""
    _check_site_indices(structure, (site_index1, site_index2, site_index3, site_index4))

    _, pos2 = _calc_atomic_distance(structure, site_index1, site_index2, backfold_positions)
    _, pos3 = _calc_atomic_distance(structure, site_index1, site_index3, backfold_positions)
    _, pos4 = _calc_atomic_distance(structure, site_index1, site_index4, backfold_positions)
    pos1 = np.array(structure["positions"][site_index1])
    n_vector1 = np.cross(pos2 - pos1, pos3 - pos2)
    n_vector2 = np.cross(pos3 - pos2, pos4 - pos3)
    return None, calc_angle(n_vector1, n_vector2) * 180.0 / np.pi


def _check_site_indices(structure, site_indices):
    is_int = (
        True if isinstance(site_indices[0], int) and isinstance(site_indices[1], int) else False
    )

    if site_indices[1] is None:
        site_indices = np.array(site_indices[0])
    else:
        if isinstance(site_indices[0], (tuple, list)) and isinstance(
            site_indices[1], (tuple, list)
        ):
            if len(site_indices[0]) != len(site_indices[1]):
                raise ValueError("The number of site indices must be equal.")
        elif isinstance(site_indices[0], (tuple, list)):
            if len(site_indices[0]) != 1:
                raise ValueError("The number of site indices must be equal.")
        elif isinstance(site_indices[1], (tuple, list)):
            if len(site_indices[1]) != 1:
                raise ValueError("The number of site indices must be equal.")
        site_indices = np.concatenate(site_indices, axis=None).flatten()

    if site_indices.dtype not in ["int32", "int64"]:
        raise TypeError("`site_index` needs to be of type int.")
    if len(structure["elements"]) <= site_indices.max():
        raise ValueError("`site_index` needs to be smaller than the number of sites.")

    return is_int


def _get_cell_from_lattice_p(
    a: float, b: float, c: float, alpha: float, beta: float, gamma: float
) -> List[List[float]]:
    """
    Get cell matrix from lattice parameters.

    Parameters
    ----------
    a : float
        Length of the first vector.
    b : float
        Length of the second vector.
    c : float
        Length of the third vector.
    alpha : float
        Angle between b and c.
    beta : float
        Angle between a and c.
    gamma : float
        Angle between a and b.

    Returns
    -------
    list
        Nested list of the three cell vectors.
    """
    eps = 1.0e-10
    sin = []
    cos = []
    for angle in [alpha, beta, gamma]:
        if abs(angle - 90.0) < eps:
            cos.append(0.0)
            sin.append(1.0)
        elif abs(angle + 90.0) < eps:
            cos.append(0.0)
            sin.append(-1.0)
        else:
            cos.append(np.cos(angle * np.pi / 180.0))
            sin.append(np.sin(angle * np.pi / 180.0))

    c1 = float(c) * cos[1]
    c2 = float(c) * (cos[0] - cos[1] * cos[2]) / sin[2]
    c3 = float(np.sqrt(float(c) ** 2.0 - c1**2.0 - c2**2.0))

    v1 = float(a) * np.array([1.0, 0.0, 0.0])
    v2 = float(b) * np.array([cos[2], sin[2], 0.0])
    return [v1.tolist(), v2.tolist(), [c1, c2, c3]]


def _calc_reciprocal_cell(cell):
    """
    Calculate the reciprocal cell from the cell in 'real' space.

    Parameters
    ----------
    cell : list or np.array
        Nested 3x3 list of the cell vectors.

    Returns
    -------
    reciprocal_cell : list
        Nested 3x3 list of the cell vectors.
    """
    if isinstance(cell, (list, np.ndarray)):
        cell = np.array(cell).reshape((3, 3))
    else:
        raise TypeError("'cell' must be a list or numpy array.")
    cell_volume = abs(np.dot(np.cross(cell[0], cell[1]), cell[2]))
    reciprocal_cell = np.zeros((3, 3))
    for dir_idx in range(3):
        # We use negative indices here
        reciprocal_cell[dir_idx] = (
            2.0 * np.pi / cell_volume * np.cross(cell[dir_idx - 2], cell[dir_idx - 1])
        )
    return reciprocal_cell.tolist()


def _prepare_combined_indices(site_indices1, site_indices2):
    """Prepare combined indices for `calc_atomic_distance` methods.

    Can be applied to other methods requiring two sets of site indices, with the second
    set being optional. If the second set is not provided, the first one is used to create
    all unique combinations of pairs.
    """
    if isinstance(site_indices1, int):
        site_indices1 = [site_indices1]
    if site_indices2 is None:
        site_indices1, site_indices2 = zip(*itertools.combinations(site_indices1, 2))
        site_indices1 = list(site_indices1)
        site_indices2 = list(site_indices2)
    elif isinstance(site_indices2, int):
        site_indices2 = [site_indices2]

    return site_indices1, site_indices2


def _parse_calc_atomic_distance_output(is_int, distance, pos, site_indices1, site_indices2):
    if is_int:
        return distance[0], pos[0]
    else:
        distance_dict = {
            tuple(idx): dist for *idx, dist in zip(site_indices1, site_indices2, distance)
        }
        pos_dict = {tuple(idx): pos_ for *idx, pos_ in zip(site_indices1, site_indices2, pos)}
        return distance_dict, pos_dict


def _calc_atomic_distance(structure, site_indices1, site_indices2, backfold_positions):
    """Calculate distance between two atoms."""
    is_int = _check_site_indices(structure, (site_indices1, site_indices2))

    site_indices1, site_indices2 = _prepare_combined_indices(site_indices1, site_indices2)

    pos1 = np.array(structure["positions"])[site_indices1]
    pos2 = np.array(structure["positions"])[site_indices2]
    dist = np.linalg.norm(pos1 - pos2, axis=1)

    if structure["cell"] is not None and backfold_positions:
        fold_combs = np.array(list(itertools.product([0, -1, 1], repeat=3)))
        pos2_scaled = (
            fold_combs
            + np.array(structure.get_positions(cartesian=False, wrap=True))[site_indices2, None, :]
        )
        pos2_cart = (
            (np.array(structure["cell"]).T)
            .dot(pos2_scaled.reshape(-1, 3).T)
            .T.reshape(pos2_scaled.shape)
        )
        dist = np.linalg.norm(pos1[:, None, :] - pos2_cart, axis=2)
        pos2 = pos2_cart[np.arange(dist.shape[0]), dist.argmin(axis=1), :]
        dist = dist.min(axis=1)

    return _parse_calc_atomic_distance_output(is_int, dist, pos2, site_indices1, site_indices2)


def _calc_atomic_distance_sc(structure, site_indices1, site_indices2, r_max):
    """
    Calculate distance between two atoms, considering the
    replicates in a supercell.
    """
    is_int = _check_site_indices(structure, (site_indices1, site_indices2))

    site_indices1, site_indices2 = _prepare_combined_indices(site_indices1, site_indices2)

    dist_out = []
    pos_out = []

    for site_index1, site_index2 in zip(site_indices1, site_indices2):
        _, _, positions_sc, _, mapping, _ = _create_supercell_positions(structure, r_max)
        pos1 = np.array(structure["positions"][site_index1])
        mask = np.where(np.array(mapping) == site_index2, True, False)
        pos2 = np.array(positions_sc)[mask]
        dist = []
        for pos in pos2:
            dist0 = np.linalg.norm(np.array(pos1) - pos)
            if dist0 <= r_max:
                dist.append(dist0)
        if len(dist) > 0:
            zipped = list(zip(dist, pos2.tolist()))
            zipped.sort(key=lambda point: point[0])
            dist, pos = zip(*zipped)
        else:
            dist = None
            pos = None
        dist_out.append(dist)
        pos_out.append(pos)
    return _parse_calc_atomic_distance_output(
        is_int, dist_out, pos_out, site_indices1, site_indices2
    )
