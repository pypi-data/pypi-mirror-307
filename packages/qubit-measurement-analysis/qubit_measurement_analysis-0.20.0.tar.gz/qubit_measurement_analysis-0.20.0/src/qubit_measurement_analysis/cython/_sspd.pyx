"""
Cython implementation of SSPD (Symmetric Segment-Path Distance).

This module provides an efficient Cython implementation of functions to calculate
the Symmetric Segment-Path Distance between trajectories.

Reference:
    P. Besse, B. Guillouet, J.-M. Loubes, and R. Francois,
    "Review and perspective for distance based trajectory clustering,"
    arXiv preprint arXiv:1508.04904, 2015.
"""

cimport cython
import numpy as np
cimport numpy as np

ctypedef np.complex64_t complex64_t
ctypedef np.float32_t float32_t

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float32_t point_to_point(complex64_t p1, complex64_t p2):
    cdef:
        float32_t dx = p1.real - p2.real
        float32_t dy = p1.imag - p2.imag
    return (dx * dx + dy * dy) ** 0.5

@cython.boundscheck(False)
@cython.wraparound(False)
cdef float32_t point_to_segment(complex64_t p, complex64_t seg_a, complex64_t seg_b):
    cdef:
        complex64_t ab = seg_b - seg_a
        complex64_t ap = p - seg_a
        float32_t ab_norm_sq = ab.real * ab.real + ab.imag * ab.imag
        float32_t proj_coef = (ap.real * ab.real + ap.imag * ab.imag) / ab_norm_sq
        complex64_t closest_point
    
    if proj_coef <= 0:
        return point_to_point(p, seg_a)
    elif proj_coef >= 1:
        return point_to_point(p, seg_b)
    else:
        closest_point = seg_a + proj_coef * ab
        return point_to_point(p, closest_point)

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef float32_t point_to_trajectory(complex64_t p, np.ndarray[complex64_t, ndim=1] trajectory):
    cdef:
        int i
        float32_t min_dist = np.inf
        float32_t dist
        int n = trajectory.shape[0]

    for i in range(n - 1):
        dist = point_to_segment(p, trajectory[i], trajectory[i+1])
        if dist < min_dist:
            min_dist = dist
    
    return min_dist

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef float32_t segment_path_distance(np.ndarray[complex64_t, ndim=1] trajectory, np.ndarray[complex64_t, ndim=1] target_trajectory):
    cdef:
        int i
        float32_t total_dist = 0
        int n = trajectory.shape[0]

    for i in range(n):
        total_dist += point_to_trajectory(trajectory[i], target_trajectory)
    
    return total_dist / n

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef float32_t symmetrized_segment_path_distance(np.ndarray[complex64_t, ndim=1] trajectory, np.ndarray[complex64_t, ndim=1] other_trajectory):
    cdef:
        float32_t spd_12 = segment_path_distance(trajectory, other_trajectory)
        float32_t spd_21 = segment_path_distance(other_trajectory, trajectory)
    return (spd_12 + spd_21) / 2

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[float32_t, ndim=2] cross_product(np.ndarray trajectories, np.ndarray target_trajectories):
    cdef:
        int M, N, i, j
        np.ndarray[float32_t, ndim=2] result

    if trajectories.ndim == 1:
        M = 1
        trajectories = trajectories.reshape(1, -1)
    else:
        M = trajectories.shape[0]

    if target_trajectories.ndim == 1:
        N = 1
        target_trajectories = target_trajectories.reshape(1, -1)
    else:
        N = target_trajectories.shape[0]

    result = np.zeros((M, N), dtype=np.float32)

    for i in range(M):
        for j in range(N):
            result[i, j] = symmetrized_segment_path_distance(trajectories[i], target_trajectories[j])

    return result

@cython.boundscheck(False)
@cython.wraparound(False)
cpdef np.ndarray[float32_t, ndim=1] pairwise(np.ndarray trajectories, np.ndarray target_trajectories):
    cdef:
        int N, i
        np.ndarray[float32_t, ndim=1] result

    if trajectories.ndim == 1:
        N = 1
        trajectories = trajectories.reshape(1, -1)
    else:
        N = trajectories.shape[0]
    
    if target_trajectories.ndim == 1:
        target_trajectories = target_trajectories.reshape(1, -1)

    # if trajectories.shape != target_trajectories.shape:
    #     raise ValueError("Trajectory sets must have the same shape")

    result = np.zeros(N, dtype=np.float32)

    for i in range(N):
        result[i] = symmetrized_segment_path_distance(trajectories[i], target_trajectories[i])

    return result