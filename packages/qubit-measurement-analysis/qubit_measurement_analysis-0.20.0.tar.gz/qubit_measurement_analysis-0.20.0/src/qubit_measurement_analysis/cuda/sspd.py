"Module for calculating SSPD between trajectories using CUDA"

from qubit_measurement_analysis.cuda.spd import (
    pairwise as pairwise_spd,
    cross_product as cross_product_spd,
)


def pairwise(trajectories, other_trajectories):
    """
    Computes SSPD from trajectories to their corresponding other trajectories
    """
    spd_12 = pairwise_spd(trajectories, other_trajectories)
    spd_21 = pairwise_spd(other_trajectories, trajectories)
    return (spd_12 + spd_21) / 2


def cross_product(trajectories, other_trajectories):
    """
    Computes SSPD from M trajectories to N other trajectories.
    Returns (M, N) distance matrix
    """
    spd_12 = cross_product_spd(trajectories, other_trajectories)
    spd_21 = cross_product_spd(other_trajectories, trajectories)
    return (spd_12 + spd_21.T) / 2
