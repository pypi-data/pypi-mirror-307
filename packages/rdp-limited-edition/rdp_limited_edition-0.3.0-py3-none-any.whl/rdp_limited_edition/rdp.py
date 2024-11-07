from typing import Union

import numpy as np


def rdp_limed(x: np.ndarray, y: np.ndarray, max_points: int, tolerance: Union[float, int]) -> list[int]:
    """Apply RDP algorithm to points on line

    :param x: x values
    :param y: y values
    :param max_points: maximum number of points to retain
    :param tolerance: tolerance band around auxiliary line
    :return: indexes of points to retain
    """
    x_norm = (x - x.min()) / (x.max() - x.min())
    y_norm = (y - y.min()) / (y.max() - y.min())
    points = np.column_stack((x_norm, y_norm))

    # initially keep first and last point
    reduced_idxs = [0, (x.shape[0] - 1)]

    to_terminate = False
    while not to_terminate:

        slices_max_distance = np.empty((len(reduced_idxs)-1), dtype=float)
        slices_argmax_distance = np.empty((len(reduced_idxs)-1), dtype=np.int64)

        # TODO to reduce computation, only recalc slices which are new
        for i in range(0, (len(reduced_idxs) - 1)):
            slice_start = reduced_idxs[i]
            slice_end = reduced_idxs[i + 1] + 1
            if (slice_end - 1 - slice_start ) == 1:
                # skip slices between directly neighboring points
                continue
            slice_normal_distances = _calc_normal_distances_to_aux_line(points[slice_start:slice_end,])
            slices_max_distance[i] = np.max(slice_normal_distances)
            slices_argmax_distance[i] = np.argmax(slice_normal_distances) + slice_start + 1

        overall_max_distance = np.max(slices_max_distance)
        # if the max dist of every slice is already below tolerance, abort
        if (overall_max_distance < tolerance):
            to_terminate = True
        else:
            argmax_over_max_distance_of_all_slices = np.argmax(slices_max_distance)
            idx_to_be_added = slices_argmax_distance[argmax_over_max_distance_of_all_slices]
            reduced_idxs.append(int(idx_to_be_added))
            reduced_idxs = sorted(reduced_idxs)
        
        if (len(reduced_idxs) >= max_points):
            to_terminate = True
    
    return reduced_idxs


def _calc_normal_distances_to_aux_line(points: np.array) -> np.array:
    """Calculate normal distances

    Calculates normal distances of all points to the line between the first and the last point.
    Normal distance means distance of point to line where distance vector has rectangular angle to the auxiliary line
    
    Line between first_point and last_point, normal distance from that line to avery point pn in between
    Formular: abs(cross(last_point-first_point, first_point-pn)) / norm(last_point-first_point)
    
    Expects input shape: (num_points, 2)
    Returns output shape: (num_points-2, 1)

    :param points: points on line in R2
    :return: normal distances of points
    """
    # vector from 1st point to last point
    aux_line = points[(points.shape[0] - 1),] - points[0,]
    # (first_point - pn) for all pn between first_point and last_point
    vector_diffs = (points[1:(points.shape[0] - 1),] - points[0,]) * -1

    # calc cross product for all pn
    cross_products = np.abs(_calc_cross_products_in_r2(reference_vector=aux_line, target_vectors=vector_diffs))
    line_frobenius_norm = _calc_frobenius_norm_in_r2(aux_line)
    # abs_cross/norm(last_point-first_point)
    return cross_products / line_frobenius_norm


def _calc_frobenius_norm_in_r2(vec: np.array) -> np.array:
    """Calculate frobenius norm of vector in R2

    Specialized and faster implementation of `np.linalg.norm(vec)`

    :param vec: vector in R2
    :return: frobenius norm of vector
    """
    return np.sqrt(np.power(vec[0], 2) + np.power(vec[1], 2))


def _calc_cross_products_in_r2(reference_vector: np.array, target_vectors: np.array) -> np.array:
    """Calculate cross product of several vectors to reference vector

    Specialized and faster implementation of `np.cross(reference_vector, target_vectors)`

    :param reference_vector: reference vector in R2 shape (2)
    :param target_vectors: vectors, shape (n, 2)
    :return: cross products
    """
    return target_vectors[:,1] * reference_vector[0] - target_vectors[:,0] * reference_vector[1]
