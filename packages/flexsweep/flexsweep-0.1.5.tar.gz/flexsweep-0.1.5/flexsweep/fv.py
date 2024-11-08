import os

os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"
os.environ["NUMEXPR_MAX_THREADS"] = "1"
os.environ["NUMBA_NUM_THREADS"] = "1"

import threadpoolctl

threadpoolctl.threadpool_limits(1)

import subprocess

from . import pd, np, Parallel, delayed
from .data import Data

# import pandas as pd
# import numpy as np
# from joblib import Parallel, delayed

from math import comb
from functools import partial, reduce
from numba import njit
from typing import Tuple
from allel import (
    HaplotypeArray,
    ihs,
    nsl,
    garud_h,
    standardize_by_allele_count,
    sequence_diversity,
    mean_pairwise_difference,
    haplotype_diversity,
    moving_haplotype_diversity,
    tajima_d,
    sfs,
)
from allel.compat import memoryview_safe
from allel.opt.stats import ihh01_scan, ihh_scan
from allel.util import asarray_ndim, check_dim0_aligned, check_integer_dtype
from allel.stats.selection import compute_ihh_gaps

from copy import deepcopy
from collections import defaultdict, namedtuple
from itertools import product, chain

from warnings import filterwarnings
import pickle

import gzip
import re


################## Utils
def mispolarize(hap, proportion=0.1):
    """
    Allele mispolarization by randomly flipping the alleles of a haplotype matrix (i.e., switching between 0 and 1). The proportion of rows to be flipped is determined by the `proportion` parameter.

    Parameters
    ----------
    hap : numpy.ndarray
        A 2D numpy array representing the haplotype matrix of shape (S, n),
        where S is the number of variants (rows), and n is the number of samples (columns).
        Each element is expected to be binary (0 or 1), representing the alleles.

    proportion : float, optional (default=0.1)
        A float between 0 and 1 specifying the proportion of rows (loci) in the haplotype
        matrix to randomly flip. For example, if proportion=0.1, 10% of the rows in the
        haplotype matrix will have their allele values flipped.

    Returns
    -------
    hap_copy : numpy.ndarray
        A new 2D numpy array of the same shape as `hap`, with a proportion of rows
        randomly flipped (alleles inverted). The original matrix `hap` is not modified
        in-place.

    Notes
    -----
    The flipping operation is done using a bitwise XOR operation (`^= 1`), which
    efficiently flips 0 to 1 and 1 to 0 for the selected rows.

    """
    # Get shape of haplotype matrix
    S, n = hap.shape

    # Select the column indices to flip based on the given proportion
    to_flip = np.random.choice(np.arange(S), int(S * proportion), replace=False)

    # Create a copy of the original hap matrix to avoid in-place modification
    hap_copy = hap.copy()
    hap_copy[to_flip, :] ^= 1
    return hap_copy


def filter_gt(hap, rec_map, region=None):
    """
    Convert the 2d numpy haplotype matrix to HaplotypeArray from scikit-allel and change type np.int8. It filters and processes the haplotype matrix based on a recombination map and
    returns key information for further analysis such as allele frequencies and physical positions.

    Parameters
    ----------
    hap : array-like, HaplotypeArray
        The input haplotype data which can be in one of the following forms:
        - A `HaplotypeArray` object.
        - A genotype matrix (as a numpy array or similar).

    rec_map : numpy.ndarray
        A 2D numpy array representing the recombination map, where each row corresponds
        to a genomic variant and contains recombination information. The third column (index 2)
        of the recombination map provides the physical positions of the variants.

    Returns
    -------
    tuple
        A tuple containing the following elements:
        - hap_01 (numpy.ndarray): The filtered haplotype matrix, with only biallelic variants.
        - ac (AlleleCounts): An object that stores allele counts for the filtered variants.
        - biallelic_mask (numpy.ndarray): A boolean mask indicating which variants are biallelic.
        - hap_int (numpy.ndarray): The haplotype matrix converted to integer format (int8).
        - rec_map_01 (numpy.ndarray): The recombination map filtered to include only biallelic variants.
        - position_masked (numpy.ndarray): The physical positions of the biallelic variants.
        - sequence_length (int): An arbitrary sequence length set to 1.2 million bases (1.2e6).
        - freqs (numpy.ndarray): The frequencies of the alternate alleles for each biallelic variant.
    """
    try:
        hap = HaplotypeArray(hap.genotype_matrix())
    except:
        try:
            hap = HaplotypeArray(hap)
        except:
            hap = HaplotypeArray(load(hap).genotype_matrix())

    # positions = rec_map[:, -1]
    # physical_position = rec_map[:, -2]

    # HAP matrix centered to analyse whole chromosome
    hap_01, ac, biallelic_mask = filter_biallelics(hap)
    hap_int = hap_01.astype(np.int8)
    rec_map_01 = rec_map[biallelic_mask]
    sequence_length = int(1.2e6)
    freqs = ac.to_frequencies()[:, 1]

    if region is not None:
        tmp = list(map(int, region.split(":")[-1].split("-")))
        d_pos = dict(zip(np.arange(tmp[0], tmp[1]), np.arange(sequence_length) + 1))
        for r in rec_map_01:
            r[-1] = d_pos[r[-1]]

    position_masked = rec_map_01[:, -1]
    physical_position_masked = rec_map_01[:, -2]

    return (
        hap_01,
        ac,
        biallelic_mask,
        hap_int,
        rec_map_01,
        position_masked,
        physical_position_masked,
        sequence_length,
        freqs,
    )


def filter_gt2(hap, rec_map, region=None):
    """
    Convert the 2d numpy haplotype matrix to HaplotypeArray from scikit-allel and change type np.int8. It filters and processes the haplotype matrix based on a recombination map and
    returns key information for further analysis such as allele frequencies and physical positions.

    Parameters
    ----------
    hap : array-like, HaplotypeArray
        The input haplotype data which can be in one of the following forms:
        - A `HaplotypeArray` object.
        - A genotype matrix (as a numpy array or similar).

    rec_map : numpy.ndarray
        A 2D numpy array representing the recombination map, where each row corresponds
        to a genomic variant and contains recombination information. The third column (index 2)
        of the recombination map provides the physical positions of the variants.

    Returns
    -------
    tuple
        A tuple containing the following elements:
        - hap_01 (numpy.ndarray): The filtered haplotype matrix, with only biallelic variants.
        - ac (AlleleCounts): An object that stores allele counts for the filtered variants.
        - biallelic_mask (numpy.ndarray): A boolean mask indicating which variants are biallelic.
        - hap_int (numpy.ndarray): The haplotype matrix converted to integer format (int8).
        - rec_map_01 (numpy.ndarray): The recombination map filtered to include only biallelic variants.
        - position_masked (numpy.ndarray): The physical positions of the biallelic variants.
        - sequence_length (int): An arbitrary sequence length set to 1.2 million bases (1.2e6).
        - freqs (numpy.ndarray): The frequencies of the alternate alleles for each biallelic variant.
    """
    try:
        # Avoid unnecessary conversion if hap is already a HaplotypeArray
        if not isinstance(hap, HaplotypeArray):
            hap = HaplotypeArray(
                hap if isinstance(hap, np.ndarray) else hap.genotype_matrix()
            )
    except:
        hap = HaplotypeArray(load(hap).genotype_matrix())

    # positions = rec_map[:, -1]
    # physical_position = rec_map[:, -2]

    # HAP matrix centered to analyse whole chromosome
    hap_01, ac, biallelic_mask = filter_biallelics2(hap)
    sequence_length = int(1.2e6)

    if region is not None:
        tmp = list(map(int, region.split(":")[-1].split("-")))
        d_pos = dict(zip(np.arange(tmp[0], tmp[1]), np.arange(sequence_length) + 1))
        for r in rec_map_01:
            r[-1] = d_pos[r[-1]]

    rec_map_01 = rec_map[biallelic_mask]
    position_masked = rec_map_01[:, -1]
    physical_position_masked = rec_map_01[:, -2]

    return (
        hap_01,
        rec_map_01,
        ac,
        biallelic_mask,
        position_masked,
        physical_position_masked,
    )


def filter_biallelics(hap: HaplotypeArray) -> tuple:
    """
    Filter out non-biallelic loci from the haplotype data.

    Args: hap (allel.HaplotypeArray): Haplotype data represented as a HaplotypeArray.

    Returns:tuple: A tuple containing three elements:
        - hap_biallelic (allel.HaplotypeArray): Filtered biallelic haplotype data.
        - ac_biallelic (numpy.ndarray): Allele counts for the biallelic loci.
        - biallelic_mask (numpy.ndarray): Boolean mask indicating biallelic loci.
    """
    ac = hap.count_alleles()
    biallelic_mask = ac.is_biallelic_01()
    return (hap.subset(biallelic_mask), ac[biallelic_mask, :], biallelic_mask)


def filter_biallelics2(hap: HaplotypeArray) -> tuple:
    """
    Filter out non-biallelic loci from the haplotype data.

    Args:
        hap (allel.HaplotypeArray): Haplotype data represented as a HaplotypeArray.

    Returns:
        tuple: A tuple containing three elements:
            - hap_biallelic (allel.HaplotypeArray): Filtered biallelic haplotype data.
            - ac_biallelic (numpy.ndarray): Allele counts for the biallelic loci.
            - biallelic_mask (numpy.ndarray): Boolean mask indicating biallelic loci.
    """
    ac = hap.count_alleles()
    biallelic_mask = ac.is_biallelic_01()

    # Use a subset to filter directly, minimizing intermediate memory usage
    hap_biallelic = hap.subset(biallelic_mask)

    ac_biallelic = ac[biallelic_mask]

    return (hap_biallelic.values, ac_biallelic.values, biallelic_mask)


pd_merger = partial(pd.merge, how="outer")

# Define the inner namedtuple structure
# summaries = namedtuple("summaries", ["snps", "window", "K", "parameters"])
summaries = namedtuple("summaries", ["stats", "parameters"])

################## Summaries


def worker(args):
    ts, rec_map, index, center, step, neutral, mispolarize_ratio = args
    return calculate_stats(
        ts,
        rec_map,
        index,
        center=center,
        step=step,
        neutral=neutral,
        mispolarize_ratio=mispolarize_ratio,
    )


def calculate_stats(
    hap,
    rec_map,
    _iter=1,
    center=[5e5, 7e5],
    windows=[1000000],
    step=1e4,
    neutral=False,
    mispolarize_ratio=None,
    region=None,
):
    """
    Computes population genetic statistics across a given haplotype matrix,
    centered on specified genomic regions, and using a recombination map.
    It supports optional mispolarization of the haplotype matrix.
    If neutral flag the estimation will be performed by calculating whole-chromosome statistics
    to perfomr later neutral normalization.

    Statistics calculated:
    - iHS (Integrated haplotype score, Voight et al. 2006)
    - nSL (Number of segregating sites by length, Ferrer-Admetlla et al. 2014)
    - DIND (Derived intra-allelic nucleotide diversity, Barreiro et al. 2009)
    - iSAFE (Integrated selection of allele favored by evolution, Akbari et al. 2018)
    - HAF (Haplotype allele frequency, Ronen et al. 2015)
    - H12 (Frequencies of first and second most common haplotypes, modified to use 80% identity threshold, Garud et al. 2015)
    - hapdaf_o (Haplotype-derived allele frequency (old), Lauterbur et al. 2023)
    - hapdaf_s (Haplotype-derived allele frequency (standing), Lauterbur et al. 2023)
    - s_ratio (Segregating sites ratio, Lauterbur et al. 2023)
    - lowfreq (Low-frequency alleles on derived background, Lauterbur et al. 2023)
    - highfreq (High-frequency alleles on derived background, Lauterbur et al. 2023)

    Parameters
    ----------
    hap : HaplotypeArray or numpy.ndarray
        The input haplotype matrix or an object that can be converted to a haplotype matrix.

    rec_map : numpy.ndarray
        A 2D numpy array representing the recombination map, where each row corresponds
        to a variant and contains recombination information. The third column (index 2)
        is used for the physical positions of the variants.

    _iter : int, optional (default=1)
        An integer representing the iteration number or replicate for the analysis.

    center : list of float, optional (default=[5e5, 7e5])
        A list specifying the center positions (in base pairs) for the analysis window.
        If one center is provided, it will use that as a single point; otherwise, it
        calculates a range between the two provided points.

    windows : list of int, optional (default=[1000000])
        A list of window sizes (in base pairs) over which statistics will be calculated.

    step : float, optional (default=1e4)
        The step size (in base pairs) for sliding windows in the analysis.

    neutral : bool, optional (default=False)
        A flag indicating whether to normalize the statistics based on neutral expectations.
        If True, the estimation will be performed by calculating whole-chromosome statistics.

    mispolarize_ratio : float or None, optional (default=None)
        A float representing the proportion of variants to mispolarize in the haplotype matrix.
        If None, no mispolarization is applied.

    Returns
    -------
    df_stats : pandas.DataFrame
        A DataFrame containing the computed statistics for each genomic window and
        population genetic measure.

    df_stats_norm : pandas.DataFrame, optional
        If `neutral=True`, an additional DataFrame is returned containing the normalized
        statistics based on neutral expectations. If `neutral=False`, only `df_stats` is returned.
    """

    filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message="invalid value encountered in scalar divide",
    )
    np.seterr(divide="ignore", invalid="ignore")

    if mispolarize_ratio is not None:
        hap = mispolarize(hap, mispolarize_ratio)
    # Open and filtering data
    (
        hap_01,
        ac,
        biallelic_mask,
        hap_int,
        rec_map_01,
        position_masked,
        physical_position_masked,
        sequence_length,
        freqs,
    ) = filter_gt(hap, rec_map, region=region)

    if len(center) == 1:
        centers = np.arange(center[0], center[0] + step, step).astype(int)
    else:
        centers = np.arange(center[0], center[1] + step, step).astype(int)

    df_dind_high_low = dind_high_low(hap_int, ac.values, rec_map_01)
    df_s_ratio = s_ratio(hap_int, ac.values, rec_map_01)
    df_hapdaf_o = hapdaf_o(hap_int, ac.values, rec_map_01)
    df_hapdaf_s = hapdaf_s(hap_int, ac.values, rec_map_01)

    try:
        h12_v = h12_enard(hap, rec_map, window_size=int(5e5) if neutral else int(1.2e6))
        # h12_v = run_h12(hap, rec_map, _iter=_iter, neutral=neutral)
    except:
        h12_v = np.nan

    haf_v = haf_top(hap_int.astype(np.float64), position_masked)

    daf_w = 1.0
    pos_w = int(6e5)
    if np.isnan(h12_v) & np.isnan(haf_v):
        daf_w = np.nan
        pos_w = np.nan

    df_snps = reduce(
        pd_merger,
        [
            df_dind_high_low,
            df_s_ratio,
            df_hapdaf_o,
            df_hapdaf_s,
        ],
    )

    df_snps.insert(0, "window", int(1e6))
    df_snps.insert(0, "center", int(6e5))
    df_snps.insert(0, "iter", _iter)
    df_snps.positions = df_snps.positions.astype(int)

    df_window = pd.DataFrame(
        [[_iter, int(6e5), int(1e6), pos_w, daf_w, h12_v, haf_v]],
        columns=["iter", "center", "window", "positions", "daf", "h12", "haf"],
    )

    df_snps_centers = []
    for c, w in product(centers, windows):
        lower = c - w / 2
        upper = c + w / 2

        p_mask = (position_masked >= lower) & (position_masked <= upper)
        p_mask
        f_mask = freqs >= 0.05

        # Check whether the hap subset is empty or not
        if hap_int[p_mask].shape[0] == 0:
            df_centers_stats = pd.DataFrame(
                {
                    "iter": _iter,
                    "center": c,
                    "window": w,
                    "positions": np.nan,
                    "daf": np.nan,
                    "isafe": np.nan,
                    "ihs": np.nan,
                    "nsl": np.nan,
                },
                index=[0],
            )
        else:
            df_isafe = run_isafe(hap_int[p_mask], position_masked[p_mask])

            # iHS and nSL
            df_ihs = ihs_ihh(
                hap_01[p_mask],
                position_masked[p_mask],
                map_pos=physical_position_masked[p_mask],
                min_ehh=0.05,
                min_maf=0.05,
                include_edges=False,
            )

            # df_ihs = run_hapbin(hap_int[p_mask], rec_map_01[p_mask], _iter=i, cutoff=0.05)

            nsl_v = nsl(hap_01.subset((p_mask) & (f_mask)), use_threads=False)

            df_nsl = pd.DataFrame(
                {
                    "positions": position_masked[(p_mask) & (f_mask)],
                    "daf": freqs[(p_mask) & (f_mask)],
                    "nsl": nsl_v,
                }
            )

            df_centers_stats = reduce(pd_merger, [df_isafe, df_ihs, df_nsl])
            # df_centers_stats = reduce(pd_merger, [df_isafe, df_ihs])

            df_centers_stats.insert(0, "window", w)
            df_centers_stats.insert(0, "center", c)
            df_centers_stats.insert(0, "iter", _iter)
            df_centers_stats = df_centers_stats.astype(object)

            # df_nsl.insert(0, "window", w)
            # df_nsl.insert(0, "center", c)
            # df_nsl.insert(0, "iter", i)

            # nsl_d[c] = df_nsl

        df_snps_centers.append(df_centers_stats)

    df_snps_centers = pd.concat(df_snps_centers)
    df_snps_centers = df_snps_centers.infer_objects()
    df_snps = pd.merge(df_snps_centers, df_snps, how="outer")

    df_snps.sort_values(by=["center", "window", "positions"], inplace=True)
    df_snps.reset_index(drop=True, inplace=True)

    df_stats = pd.merge(df_snps, df_window, how="outer")

    if region is not None:
        df_stats["iter"] = df_stats.loc[:, "iter"].astype(str)
        df_stats.loc[:, "iter"] = region

    if neutral:
        # Whole chromosome statistic to normalize
        df_isafe = run_isafe(hap_int, position_masked)
        df_ihs = ihs_ihh(hap_01, position_masked, min_ehh=0.1, include_edges=True)
        # df_ihs = run_hapbin(hap_01, rec_map_01, _iter=i, cutoff=0.1)

        nsl_v = nsl(hap_01.subset(freqs >= 0.05), use_threads=False)

        df_nsl = pd.DataFrame(
            {
                "positions": position_masked[freqs >= 0.05],
                "daf": freqs[freqs >= 0.05],
                "nsl": nsl_v,
            }
        )

        df_snps_norm = reduce(
            pd_merger,
            [
                df_snps[df_snps.center == 6e5].iloc[
                    :,
                    ~df_snps.columns.isin(
                        [
                            "iter",
                            "center",
                            "window",
                            "delta_ihh",
                            "ihs",
                            "isafe",
                            "nsl",
                        ]
                    ),
                ],
                df_isafe,
                df_ihs,
                df_nsl,
            ],
        )

        df_snps_norm.insert(0, "window", int(1.2e6))
        df_snps_norm.insert(0, "center", int(6e5))
        df_snps_norm.insert(0, "iter", _iter)

        df_snps_norm = df_snps_norm.sort_values(
            by=["center", "window", "positions"]
        ).reset_index(drop=True)
        df_window.window = int(1.2e6)
        df_stats_norm = pd.merge(df_snps_norm, df_window, how="outer")

        return df_stats, df_stats_norm
    else:
        return df_stats


def calculate_stats2(
    hap_str,
    _iter=1,
    center=[5e5, 7e5],
    windows=[1000000],
    step=1e4,
    neutral=False,
    mispolarize_ratio=None,
    region=None,
):
    """
    Computes population genetic statistics across a given haplotype matrix,
    centered on specified genomic regions, and using a recombination map.
    It supports optional mispolarization of the haplotype matrix.
    If neutral flag the estimation will be performed by calculating whole-chromosome statistics
    to perfomr later neutral normalization.

    Statistics calculated:
    - iHS (Integrated haplotype score, Voight et al. 2006)
    - nSL (Number of segregating sites by length, Ferrer-Admetlla et al. 2014)
    - DIND (Derived intra-allelic nucleotide diversity, Barreiro et al. 2009)
    - iSAFE (Integrated selection of allele favored by evolution, Akbari et al. 2018)
    - HAF (Haplotype allele frequency, Ronen et al. 2015)
    - H12 (Frequencies of first and second most common haplotypes, modified to use 80% identity threshold, Garud et al. 2015)
    - hapdaf_o (Haplotype-derived allele frequency (old), Lauterbur et al. 2023)
    - hapdaf_s (Haplotype-derived allele frequency (standing), Lauterbur et al. 2023)
    - s_ratio (Segregating sites ratio, Lauterbur et al. 2023)
    - lowfreq (Low-frequency alleles on derived background, Lauterbur et al. 2023)
    - highfreq (High-frequency alleles on derived background, Lauterbur et al. 2023)

    Parameters
    ----------
    hap : HaplotypeArray or numpy.ndarray
        The input haplotype matrix or an object that can be converted to a haplotype matrix.

    rec_map : numpy.ndarray
        A 2D numpy array representing the recombination map, where each row corresponds
        to a variant and contains recombination information. The third column (index 2)
        is used for the physical positions of the variants.

    _iter : int, optional (default=1)
        An integer representing the iteration number or replicate for the analysis.

    center : list of float, optional (default=[5e5, 7e5])
        A list specifying the center positions (in base pairs) for the analysis window.
        If one center is provided, it will use that as a single point; otherwise, it
        calculates a range between the two provided points.

    windows : list of int, optional (default=[1000000])
        A list of window sizes (in base pairs) over which statistics will be calculated.

    step : float, optional (default=1e4)
        The step size (in base pairs) for sliding windows in the analysis.

    neutral : bool, optional (default=False)
        A flag indicating whether to normalize the statistics based on neutral expectations.
        If True, the estimation will be performed by calculating whole-chromosome statistics.

    mispolarize_ratio : float or None, optional (default=None)
        A float representing the proportion of variants to mispolarize in the haplotype matrix.
        If None, no mispolarization is applied.

    Returns
    -------
    df_stats : pandas.DataFrame
        A DataFrame containing the computed statistics for each genomic window and
        population genetic measure.

    df_stats_norm : pandas.DataFrame, optional
        If `neutral=True`, an additional DataFrame is returned containing the normalized
        statistics based on neutral expectations. If `neutral=False`, only `df_stats` is returned.
    """

    hap, rec_map, p = ms_parser(hap_str)

    filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message="invalid value encountered in scalar divide",
    )
    np.seterr(divide="ignore", invalid="ignore")

    if mispolarize_ratio is not None:
        hap = mispolarize(hap, mispolarize_ratio)

    # Open and filtering data
    (
        hap_int,
        rec_map_01,
        ac,
        biallelic_mask,
        position_masked,
        physical_position_masked,
    ) = filter_gt2(hap, rec_map, region=region)
    freqs = ac[:, 1] / ac.sum(axis=1)

    if len(center) == 1:
        centers = np.arange(center[0], center[0] + step, step).astype(int)
    else:
        centers = np.arange(center[0], center[1] + step, step).astype(int)

    df_dind_high_low = dind_high_low(hap_int, ac, rec_map_01)
    df_s_ratio = s_ratio(hap_int, ac, rec_map_01)
    df_hapdaf_o = hapdaf_o(hap_int, ac, rec_map_01)
    df_hapdaf_s = hapdaf_s(hap_int, ac, rec_map_01)

    try:
        h12_v = h12_enard(
            hap_int, rec_map_01, window_size=int(5e5) if neutral else int(1.2e6)
        )
        # h12_v = run_h12(hap, rec_map, _iter=_iter, neutral=neutral)
    except:
        h12_v = np.nan

    haf_v = haf_top(hap_int.astype(np.float64), position_masked)

    daf_w = 1.0
    pos_w = int(6e5)
    if np.isnan(h12_v) & np.isnan(haf_v):
        daf_w = np.nan
        pos_w = np.nan

    df_snps = reduce(
        pd_merger,
        [
            df_dind_high_low,
            df_s_ratio,
            df_hapdaf_o,
            df_hapdaf_s,
        ],
    )

    df_snps.insert(0, "iter", _iter)
    df_snps["positions"] = df_snps["positions"].astype(np.int32)

    d_centers = {}

    for c, w in product(centers, windows):
        lower = c - w / 2
        upper = c + w / 2

        p_mask = (position_masked >= lower) & (position_masked <= upper)
        p_mask
        f_mask = freqs >= 0.05

        # Check whether the hap subset is empty or not
        if hap_int[p_mask].shape[0] == 0:
            df_centers_stats = pd.DataFrame(
                {
                    "iter": _iter,
                    # "center": c,
                    # "window": w,
                    "positions": np.nan,
                    "daf": np.nan,
                    "isafe": np.nan,
                    "ihs": np.nan,
                    "nsl": np.nan,
                },
                index=[0],
            )
            d_centers[c] = df_centers_stats
        else:
            df_isafe = run_isafe(hap_int[p_mask], position_masked[p_mask])

            # iHS and nSL
            df_ihs = ihs_ihh(
                hap_int[p_mask],
                position_masked[p_mask],
                map_pos=physical_position_masked[p_mask],
                min_ehh=0.05,
                min_maf=0.05,
                include_edges=False,
            )

            nsl_v = nsl(hap_int[(p_mask) & (f_mask)], use_threads=False)

            df_nsl = pd.DataFrame(
                {
                    "positions": position_masked[(p_mask) & (f_mask)],
                    "daf": freqs[(p_mask) & (f_mask)],
                    "nsl": nsl_v,
                }
            )

            # Consolidate the merge to reduce memory usage
            df_centers_stats = reduce(pd_merger, [df_isafe, df_ihs, df_nsl])

            df_centers_stats.insert(0, "iter", _iter)

            # Avoid redundant merge
            if c == int(6e5):
                d_centers[c] = pd.merge(df_centers_stats, df_snps, how="outer")
            else:
                d_centers[c] = df_centers_stats

    if region is not None:
        for df in d_centers.values():
            df["iter"] = region

    if neutral:
        # Whole chromosome statistic to normalize
        df_isafe = run_isafe(hap_int, position_masked)
        df_ihs = ihs_ihh(hap_int, position_masked, min_ehh=0.1, include_edges=True)
        nsl_v = nsl(hap_int[(freqs >= 0.05)], use_threads=False)

        df_nsl = pd.DataFrame(
            {
                "positions": position_masked[freqs >= 0.05],
                "daf": freqs[freqs >= 0.05],
                "nsl": nsl_v,
            }
        )

        df_snps_norm = reduce(
            pd_merger,
            [
                df_snps.iloc[
                    :,
                    ~df_snps.columns.isin(
                        [
                            "iter",
                            "delta_ihh",
                            "ihs",
                            "isafe",
                            "nsl",
                        ]
                    ),
                ],
                df_isafe,
                df_ihs,
                df_nsl,
            ],
        )

        df_snps_norm.insert(0, "iter", _iter)

        df_snps_norm.sort_values(by=["positions"], inplace=True)
        df_snps_norm.reset_index(drop=True, inplace=True)
        # df_window.window = int(1.2e6)
        df_stats_norm = pd.merge(df_snps_norm, df_window, how="outer")

        return d_centers, df_stats_norm
    else:
        return d_centers


def calculate_stats2b(
    hap_str,
    _iter=1,
    center=[5e5, 7e5],
    windows=[1000000],
    step=1e4,
    neutral=False,
    mispolarize_ratio=None,
    region=None,
):
    """
    Computes population genetic statistics across a given haplotype matrix,
    centered on specified genomic regions, and using a recombination map.
    It supports optional mispolarization of the haplotype matrix.
    If neutral flag the estimation will be performed by calculating whole-chromosome statistics
    to perfomr later neutral normalization.

    Statistics calculated:
    - iHS (Integrated haplotype score, Voight et al. 2006)
    - nSL (Number of segregating sites by length, Ferrer-Admetlla et al. 2014)
    - DIND (Derived intra-allelic nucleotide diversity, Barreiro et al. 2009)
    - iSAFE (Integrated selection of allele favored by evolution, Akbari et al. 2018)
    - HAF (Haplotype allele frequency, Ronen et al. 2015)
    - H12 (Frequencies of first and second most common haplotypes, modified to use 80% identity threshold, Garud et al. 2015)
    - hapdaf_o (Haplotype-derived allele frequency (old), Lauterbur et al. 2023)
    - hapdaf_s (Haplotype-derived allele frequency (standing), Lauterbur et al. 2023)
    - s_ratio (Segregating sites ratio, Lauterbur et al. 2023)
    - lowfreq (Low-frequency alleles on derived background, Lauterbur et al. 2023)
    - highfreq (High-frequency alleles on derived background, Lauterbur et al. 2023)

    Parameters
    ----------
    hap : HaplotypeArray or numpy.ndarray
        The input haplotype matrix or an object that can be converted to a haplotype matrix.

    rec_map : numpy.ndarray
        A 2D numpy array representing the recombination map, where each row corresponds
        to a variant and contains recombination information. The third column (index 2)
        is used for the physical positions of the variants.

    _iter : int, optional (default=1)
        An integer representing the iteration number or replicate for the analysis.

    center : list of float, optional (default=[5e5, 7e5])
        A list specifying the center positions (in base pairs) for the analysis window.
        If one center is provided, it will use that as a single point; otherwise, it
        calculates a range between the two provided points.

    windows : list of int, optional (default=[1000000])
        A list of window sizes (in base pairs) over which statistics will be calculated.

    step : float, optional (default=1e4)
        The step size (in base pairs) for sliding windows in the analysis.

    neutral : bool, optional (default=False)
        A flag indicating whether to normalize the statistics based on neutral expectations.
        If True, the estimation will be performed by calculating whole-chromosome statistics.

    mispolarize_ratio : float or None, optional (default=None)
        A float representing the proportion of variants to mispolarize in the haplotype matrix.
        If None, no mispolarization is applied.

    Returns
    -------
    df_stats : pandas.DataFrame
        A DataFrame containing the computed statistics for each genomic window and
        population genetic measure.

    df_stats_norm : pandas.DataFrame, optional
        If `neutral=True`, an additional DataFrame is returned containing the normalized
        statistics based on neutral expectations. If `neutral=False`, only `df_stats` is returned.
    """

    filterwarnings(
        "ignore",
        category=RuntimeWarning,
        message="invalid value encountered in scalar divide",
    )
    np.seterr(divide="ignore", invalid="ignore")

    hap, rec_map, p = ms_parser(hap_str)

    if mispolarize_ratio is not None:
        hap = mispolarize(hap, mispolarize_ratio)

    # Open and filtering data
    (
        hap_int,
        rec_map_01,
        ac,
        biallelic_mask,
        position_masked,
        physical_position_masked,
    ) = filter_gt2(hap, rec_map, region=region)
    freqs = ac[:, 1] / ac.sum(axis=1)

    if len(center) == 1:
        centers = np.arange(center[0], center[0] + step, step).astype(int)
    else:
        centers = np.arange(center[0], center[1] + step, step).astype(int)

    df_dind_high_low = dind_high_low2(hap_int, ac, rec_map_01)
    df_s_ratio = s_ratio(hap_int, ac, rec_map_01)
    df_hapdaf_o = hapdaf_o(hap_int, ac, rec_map_01)
    df_hapdaf_s = hapdaf_s(hap_int, ac, rec_map_01)

    try:
        h12_v = h12_enard(hap, rec_map, window_size=int(5e5) if neutral else int(1.2e6))
        # h12_v = run_h12(hap, rec_map, _iter=_iter, neutral=neutral)
    except:
        h12_v = np.nan

    haf_v = haf_top2(hap_int.astype(np.float64), position_masked)

    daf_w = 1.0
    pos_w = int(6e5)
    if np.isnan(h12_v) & np.isnan(haf_v):
        daf_w = np.nan
        pos_w = np.nan

    df_snps = reduce(
        pd_merger,
        [
            df_dind_high_low,
            df_s_ratio,
            df_hapdaf_o,
            df_hapdaf_s,
        ],
    )

    df_snps.insert(0, "window", int(1e6))
    df_snps.insert(0, "center", int(6e5))
    df_snps.insert(0, "iter", _iter)
    df_snps.positions = df_snps.positions.astype(int)

    df_window = pd.DataFrame(
        [[_iter, int(6e5), int(1e6), pos_w, daf_w, h12_v, haf_v]],
        columns=["iter", "center", "window", "positions", "daf", "h12", "haf"],
    )

    df_snps_centers = []
    for c, w in product(centers, windows):
        lower = c - w / 2
        upper = c + w / 2

        p_mask = (position_masked >= lower) & (position_masked <= upper)
        p_mask
        f_mask = freqs >= 0.05

        # Check whether the hap subset is empty or not
        if hap_int[p_mask].shape[0] == 0:
            df_centers_stats = pd.DataFrame(
                {
                    "iter": _iter,
                    "center": c,
                    "window": w,
                    "positions": np.nan,
                    "daf": np.nan,
                    "isafe": np.nan,
                    "ihs": np.nan,
                    "nsl": np.nan,
                },
                index=[0],
            )
        else:
            df_isafe = run_isafe(hap_int[p_mask], position_masked[p_mask])

            # iHS and nSL
            df_ihs = ihs_ihh(
                hap_int[p_mask],
                position_masked[p_mask],
                map_pos=physical_position_masked[p_mask],
                min_ehh=0.05,
                min_maf=0.05,
                include_edges=False,
            )

            # df_ihs = run_hapbin(hap_int[p_mask], rec_map_01[p_mask], _iter=i, cutoff=0.05)

            nsl_v = nsl(hap_int[(p_mask) & (f_mask)], use_threads=False)

            df_nsl = pd.DataFrame(
                {
                    "positions": position_masked[(p_mask) & (f_mask)],
                    "daf": freqs[(p_mask) & (f_mask)],
                    "nsl": nsl_v,
                }
            )

            df_centers_stats = reduce(pd_merger, [df_isafe, df_ihs, df_nsl])

            df_centers_stats.insert(0, "window", w)
            df_centers_stats.insert(0, "center", c)
            df_centers_stats.insert(0, "iter", _iter)

        df_snps_centers.append(df_centers_stats)

    df_snps_centers = pd.concat(df_snps_centers)
    df_snps = pd.merge(df_snps_centers, df_snps, how="outer")

    df_snps.sort_values(by=["center", "window", "positions"], inplace=True)
    df_snps.reset_index(drop=True, inplace=True)

    df_stats = pd.merge(df_snps, df_window, how="outer")

    if region is not None:
        df_stats["iter"] = df_stats.loc[:, "iter"].astype(str)
        df_stats.loc[:, "iter"] = region

    if neutral:
        # Whole chromosome statistic to normalize
        df_isafe = run_isafe(hap_int, position_masked)
        df_ihs = ihs_ihh(hap_int, position_masked, min_ehh=0.1, include_edges=True)
        # df_ihs = run_hapbin(hap_01, rec_map_01, _iter=i, cutoff=0.1)

        nsl_v = nsl(hap_int[freqs >= 0.05], use_threads=False)

        df_nsl = pd.DataFrame(
            {
                "positions": position_masked[freqs >= 0.05],
                "daf": freqs[freqs >= 0.05],
                "nsl": nsl_v,
            }
        )

        df_snps_norm = reduce(
            pd_merger,
            [
                df_snps[df_snps.center == 6e5].iloc[
                    :,
                    ~df_snps.columns.isin(
                        [
                            "iter",
                            "center",
                            "window",
                            "delta_ihh",
                            "ihs",
                            "isafe",
                            "nsl",
                        ]
                    ),
                ],
                df_isafe,
                df_ihs,
                df_nsl,
            ],
        )

        df_snps_norm.insert(0, "window", int(1.2e6))
        df_snps_norm.insert(0, "center", int(6e5))
        df_snps_norm.insert(0, "iter", _iter)

        df_snps_norm = df_snps_norm.sort_values(
            by=["center", "window", "positions"]
        ).reset_index(drop=True)
        df_window.window = int(1.2e6)
        df_stats_norm = pd.merge(df_snps_norm, df_window, how="outer")

        return df_stats, df_stats_norm
    else:
        return df_stats


def summary_statistics(
    data,
    nthreads=1,
    center=[500000, 700000],
    windows=[1000000],
    step=10000,
    neutral_save=None,
    vcf=False,
):
    """
    Computes summary statistics across multiple simulations or empirical data, potentially using
    multiple threads for parallel computation. The statistics are calculated over
    defined genomic windows, with optional mispolarization applied to the haplotype data.
    Save the dataframe to a parquet file


    Only iHS, nSL and iSAFE are estimated across all windows/center combination. The other
    statistics used the actual center (1.2e6 / 2) extended to 500Kb each flank.

    Parameters
    ----------
    sims : str,
        Discoal simulation path or VCF file. If VCF file ensure you're use `vcf=True` argument.
    nthreads : int, optional (default=1)
        The number of threads to use for parallel computation. If set to 1,
        the function runs in single-threaded mode. Higher values will enable
        multi-threaded processing to speed up calculations.
    center : list of int, optional (default=[500000, 700000])
        A list specifying the center positions (in base pairs) for the analysis windows.
        If one center is provided, it will use that as a single point; otherwise,
        the analysis will cover the range between the two provided centers.

    windows : list of int, optional (default=[1000000])
        A list of window sizes (in base pairs) over which summary statistics will be computed.

    step : int, optional (default=10000)
        The step size (in base pairs) for sliding windows in the analysis. This determines
        how much the analysis window moves along the genome for each iteration.
    vcf : bool,
        If true parse vcf

    Returns
    -------
    summary_stats : pandas.DataFrame
        A DataFrame containing the computed summary statistics for each simulation and
        for each genomic window.

    """

    if not vcf:
        # Reading simulations
        fs_data = Data(data, nthreads=nthreads)
        sims, df_params = fs_data.read_simulations()

        # Default file names form simulations
        neutral_save = data + "/neutral_bins.pickle"
        fvs_file = data + "/fvs.parquet"

        # Opening neutral expectations
        if os.path.exists(neutral_save):
            with open(neutral_save, "rb") as handle:
                neutral_norm = pickle.load(handle)
        else:
            neutral_norm = None

        # Region as large as possible, later zip do the proper combination in case simulation number differs
        n_sims = (
            len(sims["sweep"])
            if len(sims["sweep"]) > len(sims["neutral"])
            else len(sims["neutral"])
        )
        regions = [None] * n_sims

        assert len(sims["sweep"]) > 0 and (
            len(sims["neutral"]) > 0 or neutral_save is not None
        ), "Please input neutral and sweep simulations"

    else:
        # elif isinstance(data, dict) and "region" in data.keys():

        # Force opening bins
        assert neutral_save is not None, "Input neutral bins"
        # Reading VCF
        fs_data = fs.Data(data, nthreads=nthreads)
        sims = fs_data.read_vcf()

        # sims = {"sweep": data["sweep"]}

        # Save region and remove from dict to iter only genotype data on summary_statistics.
        regions = sims["region"]
        sims.pop("region", None)

        with open(neutral_save, "rb") as handle:
            neutral_norm = pickle.load(handle)

        # Same folder custom fvs name based on input VCF.
        f_name = os.path.basename(data)
        for ext in [".vcf", ".bcf", ".gz"]:
            f_name = f_name.replace(ext, "")
        f_name = f_name.replace(".", "_")

        fvs_file = os.path.dirname(data) + "/fvs_" + f_name + ".parquet"

        # Empty params dataframe to process empirical data
        df_params = pd.DataFrame(
            {
                "model": np.repeat("sweep", len(sims["sweep"])),
                "s": np.zeros(len(sims["sweep"])),
                "t": np.zeros(len(sims["sweep"])),
                "saf": np.zeros(len(sims["sweep"])),
                "eaf": np.zeros(len(sims["sweep"])),
            }
        )

    for k, s in sims.items():
        # pars = s
        try:
            pars = [i[0][:2] + [i[1]] for i in zip(s, regions)]
        except:
            pars = [(i[0][:2] + (None,)) for i in zip(s, regions)]

        # Use joblib to parallelize the execution
        # summ_stats = Parallel(n_jobs=nthreads, backend="loky", verbose=5)(
        p_backend = "multiprocessing" if len(pars) < 5e4 else "loky"
        summ_stats = Parallel(n_jobs=nthreads, backend=p_backend, verbose=5)(
            delayed(calculate_stats)(
                hap,
                rec_map,
                _iter,
                center=center,
                step=step,
                neutral=True if k == "neutral" else False,
                region=region,
            )
            # for _iter, (hap) in enumerate(s, 1)
            for _iter, (hap, rec_map, region) in enumerate(pars, 1)
        )

        # Ensure params order
        # return params from summ_stats if reading
        params = df_params[df_params.model == k].iloc[:, 1:].values

        if k == "neutral":
            summ_stats, summ_stats_norm = zip(*summ_stats)
            neutral_stats = summaries(
                stats=summ_stats,
                parameters=params,
            )
            neutral_stats_norm = summaries(
                stats=summ_stats_norm,
                parameters=params,
            )
        else:
            if ~np.all(params[:, 3] == 0):
                params[:, 0] = -np.log(params[:, 0])
            # summ_stats, summ_nsl = zip(*summ_stats)
            sweeps_stats = summaries(
                stats=summ_stats,
                parameters=params,
            )

    df_fv_sweep, neutral_norm = normalization(
        sweeps_stats, neutral_stats_norm, norm_values=neutral_norm, nthreads=nthreads
    )

    df_fv_sweep["model"] = "sweep"

    df_fv_sweep.loc[
        (df_fv_sweep.t >= 2000) & (df_fv_sweep.f_t >= 0.9), "model"
    ] = "hard_old_complete"
    df_fv_sweep.loc[
        (df_fv_sweep.t >= 2000) & (df_fv_sweep.f_t < 0.9), "model"
    ] = "hard_old_incomplete"
    df_fv_sweep.loc[
        (df_fv_sweep.t < 2000) & (df_fv_sweep.f_t >= 0.9), "model"
    ] = "hard_young_complete"
    df_fv_sweep.loc[
        (df_fv_sweep.t < 2000) & (df_fv_sweep.f_t < 0.9), "model"
    ] = "hard_young_incomplete"

    df_fv_sweep.loc[df_fv_sweep.f_i != df_fv_sweep.f_i.min(), "model"] = df_fv_sweep[
        df_fv_sweep.f_i != df_fv_sweep.f_i.min()
    ].model.str.replace("hard", "soft")

    if np.all(df_fv_sweep.s.values == 0):
        df_fv_sweep.loc[:, "model"] = "neutral"

    # Unstack instead pivot since we only need to reshape based on window and center values
    df_fv_sweep.set_index(
        [
            "iter",
            "s",
            "t",
            "f_i",
            "f_t",
            "model",
            "window",
            "center",
        ],
        inplace=True,
    )
    df_fv_sweep_w = df_fv_sweep.unstack(level=["window", "center"])

    df_fv_sweep_w.columns = [
        f"{col[0]}_{int(col[1])}_{int(col[2])}" for col in df_fv_sweep_w.columns
    ]
    df_fv_sweep_w.reset_index(inplace=True)

    if "neutral" in sims.keys():
        # Save neutral expectations
        if os.path.exists(neutral_save) is False:
            with open(neutral_save, "wb") as handle:
                pickle.dump(neutral_norm, handle)

        # Normalizing neutral simulations
        df_fv_neutral, tmp_norm = normalization(
            neutral_stats,
            neutral_stats_norm,
            norm_values=neutral_norm,
            nthreads=nthreads,
        )
        df_fv_neutral["model"] = "neutral"

        # Unstack instead pivot since we only need to reshape based on window and center values
        df_fv_neutral.set_index(
            [
                "iter",
                "s",
                "t",
                "f_i",
                "f_t",
                "model",
                "window",
                "center",
            ],
            inplace=True,
        )

        df_fv_neutral_w = df_fv_neutral.unstack(level=["window", "center"])

        df_fv_neutral_w.columns = [
            f"{col[0]}_{int(col[1])}_{int(col[2])}" for col in df_fv_neutral_w.columns
        ]
        df_fv_neutral_w.reset_index(inplace=True)

        df_fv_w = pd.concat([df_fv_sweep_w, df_fv_neutral_w], axis=0)
    else:
        df_fv_w = df_fv_sweep_w

    # dump fvs with more than 10% nans
    num_nans = df_fv_w.iloc[:, 6:].isnull().sum(axis=1)
    df_fv_w = df_fv_w[int(df_fv_w.iloc[:, 6:].shape[1] * 0.1) > num_nans]
    df_fv_w = df_fv_w.fillna(0)

    df_fv_w.to_parquet(fvs_file)

    return df_fv_w


################## Normalization


def normalization(
    sweeps_stats,
    neutral_stats_norm,
    norm_values=None,
    center=[5e5, 7e5],
    windows=[50000, 100000, 200000, 500000, 1000000],
    nthreads=1,
):
    """
    Normalizes sweep statistics using neutral expectations or optionally using precomputed neutral normalized values.
    The function applies normalization across different genomic windows and supports multi-threading.

    Parameters
    ----------
    sweeps_stats : namedtuple
        A Namedtuple containing the statistics for genomic sweeps and sweep parameters across
        different genomic windows.

    neutral_stats_norm : namedtuple
        A Namedtuple containing the statistics for neutral region and neutral parameters across
        different genomic windows, used as the baselinefor normalizing the sweep statistics.
        This allows comparison of sweeps against neutral expectations.

    norm_values : dict or None, optional (default=None)
        A dictionary of precomputed neutral normalizated values. If provided, these values are
        used to directly normalize the statistics. If None, the function computes
        normalization values from the neutral statistics.

    center : list of float, optional (default=[5e5, 7e5])
        A list specifying the center positions (in base pairs) for the analysis windows.
        If a single center value is provided, normalization is centered around that value.
        Otherwise, it will calculate normalization for a range of positions between the two provided centers.

    windows : list of int, optional (default=[50000, 100000, 200000, 500000, 1000000])
        A list of window sizes (in base pairs) for which the normalization will be applied.
        The function performs normalization for each of the specified window sizes.

    nthreads : int, optional (default=1)
        The number of threads to use for parallel processing. If set to 1, the function
        runs in single-threaded mode. Higher values enable multi-threaded execution for
        faster computation.

    Returns
    -------
    normalized_stats : pandas.DataFrame
        A DataFrame containing the normalized sweep statistics across the specified
        windows and genomic regions. The sweep statistics are scaled relative to
        neutral expectations.
    """

    df_stats, params = sweeps_stats

    if norm_values is not None:
        expected, stdev = norm_values.values()
    else:
        df_stats_neutral, params_neutral = neutral_stats_norm
        expected, stdev = normalize_neutral(df_stats_neutral)

    # Tried different nthreads/batch_size combinations for 100k sims, 200 threads
    # p_backend = "multiprocessing" if len(df_stats) < 5e4 else "loky"
    p_backend = "loky"
    df_fv_n = Parallel(n_jobs=nthreads, backend=p_backend, verbose=5)(
        delayed(normalize_cut)(
            _iter, v, expected=expected, stdev=stdev, center=center, windows=windows
        )
        for _iter, v in enumerate(df_stats, 1)
    )

    df_window = (
        pd.concat([i.loc[:, ["iter", "h12", "haf"]] for i in df_stats])
        .dropna()
        .reset_index(drop=True)
    )
    df_fv_n = pd.concat(df_fv_n)
    df_fv_n = pd.merge(df_fv_n, df_window, how="outer")

    # params = params[:, [0, 1, 3, 4, ]]
    df_fv_n = pd.concat(
        [
            pd.DataFrame(
                np.repeat(
                    params.copy(),
                    df_fv_n.loc[:, ["center", "window"]].drop_duplicates().shape[0],
                    axis=0,
                ),
                columns=["s", "t", "f_i", "f_t"],
            ),
            df_fv_n,
        ],
        axis=1,
    )

    return df_fv_n, {"expected": expected, "stdev": stdev}


def normalize_neutral(df_stats_neutral):
    """
    Calculates the expected mean and standard deviation of summary statistics
    from neutral simulations, used for normalization in downstream analyses.

    This function processes a DataFrame of neutral simulation statistics, bins the
    values based on frequency, and computes the mean (expected) and standard deviation
    for each bin. These statistics are used as a baseline to normalize sweep or neutral simulations

    Parameters
    ----------
    df_stats_neutral : list or pandas.DataFrame
        A list or concatenated pandas DataFrame containing the neutral simulation statistics.
        The DataFrame should contain frequency data and various summary statistics,
        including H12 and HAF, across multiple windows and bins.

    Returns
    -------
    expected : pandas.DataFrame
        A DataFrame containing the mean (expected) values of the summary statistics
        for each frequency bin. The frequency bins are the index, and the columns
        are the summary statistics.

    stdev : pandas.DataFrame
        A DataFrame containing the standard deviation of the summary statistics
        for each frequency bin. The frequency bins are the index, and the columns
        are the summary statistics.

    Notes
    -----
    - The function first concatenates the neutral statistics, if provided as a list,
      and bins the values by frequency using the `bin_values` function.
    - It computes both the mean and standard deviation for each frequency bin, which
      can later be used to normalize observed statistics (e.g., from sweeps).
    - The summary statistics processed exclude window-specific statistics such as "h12" and "haf."

    """
    # df_snps, df_window = df_stats_neutral

    window_stats = ["h12", "haf"]

    # Get std and mean values from dataframe
    tmp_neutral = pd.concat(df_stats_neutral)
    df_binned = bin_values(tmp_neutral.loc[:, ~tmp_neutral.columns.isin(window_stats)])

    # get expected value (mean) and standard deviation
    expected = df_binned.iloc[:, 5:].groupby("freq_bins").mean()
    stdev = df_binned.iloc[:, 5:].groupby("freq_bins").std()

    expected.index = expected.index.astype(str)
    stdev.index = stdev.index.astype(str)

    return expected, stdev


def bin_values(values, freq=0.02):
    """
    Bins allele frequency data into discrete frequency intervals (bins) for further analysis.

    This function takes a DataFrame containing a column of derived allele frequencies ("daf")
    and bins these values into specified frequency intervals. The resulting DataFrame will
    contain a new column, "freq_bins", which indicates the frequency bin for each data point.

    Parameters
    ----------
    values : pandas.DataFrame
        A DataFrame containing at least a column labeled "daf", which represents the derived
        allele frequency for each variant.

    freq : float, optional (default=0.02)
        The width of the frequency bins. This value determines how the frequency range (0, 1)
        is divided into discrete bins. For example, a value of 0.02 will create bins
        such as [0, 0.02], (0.02, 0.04], ..., [0.98, 1.0].

    Returns
    -------
    values_copy : pandas.DataFrame
        A copy of the original DataFrame, with an additional column "freq_bins" that contains
        the frequency bin label for each variant. The "freq_bins" are categorical values based
        on the derived allele frequencies.

    Notes
    -----
    - The `pd.cut` function is used to bin the derived allele frequencies into intervals.
    - The bins are inclusive of the lowest boundary (`include_lowest=True`) to ensure that
      values exactly at the boundary are included in the corresponding bin.
    - The resulting bins are labeled as strings with a precision of two decimal places.
    """
    # Create a deep copy of the input variable
    values_copy = values.copy()

    # Modify the copy
    values_copy.loc[:, "freq_bins"] = pd.cut(
        x=values["daf"],
        bins=np.arange(0, 1 + freq, freq),
        include_lowest=True,
        precision=2,
    ).astype(str)

    return values_copy


def normalize_cut(
    _iter,
    snps_values,
    expected,
    stdev,
    center=[5e5, 7e5],
    windows=[50000, 100000, 200000, 500000, 1000000],
):
    """
    Normalizes SNP-level statistics by comparing them to neutral expectations, and aggregates
    the statistics within sliding windows around specified genomic centers.

    This function takes SNP statistics, normalizes them based on the expected mean and standard
    deviation from neutral simulations, and computes the average values within windows
    centered on specific genomic positions. It returns a DataFrame with the normalized values
    for each window across the genome.

    Parameters
    ----------
    _iter : int
        The iteration or replicate number associated with the current set of SNP statistics.

    snps_values : pandas.DataFrame
        A DataFrame containing SNP-level statistics such as iHS, nSL, and iSAFE. The DataFrame
        should contain derived allele frequencies ("daf") and other statistics to be normalized.

    expected : pandas.DataFrame
        A DataFrame containing the expected mean values of the SNP statistics for each frequency bin,
        computed from neutral simulations.

    stdev : pandas.DataFrame
        A DataFrame containing the standard deviation of the SNP statistics for each frequency bin,
        computed from neutral simulations.

    center : list of float, optional (default=[5e5, 7e5])
        A list specifying the center positions (in base pairs) for the analysis. Normalization is
        performed around these genomic centers using the specified window sizes.

    windows : list of int, optional (default=[50000, 100000, 200000, 500000, 1000000])
        A list of window sizes (in base pairs) over which the SNP statistics will be aggregated
        and normalized. The function performs normalization for each specified window size.

    Returns
    -------
    out : pandas.DataFrame
        A DataFrame containing the normalized SNP statistics for each genomic center and window.
        The columns include the iteration number, center, window size, and the average values
        of normalized statistics iSAFE within the window.

    Notes
    -----
    - The function first bins the SNP statistics based on derived allele frequencies using the
      `bin_values` function. The statistics are then normalized by subtracting the expected mean
      and dividing by the standard deviation for each frequency bin.
    - After normalization, SNPs are aggregated into windows centered on specified genomic positions.
      The average values of the normalized statistics are calculated for each window.
    - The window size determines how far upstream and downstream of the center position the SNPs
      will be aggregated.

    """
    binned_values = bin_values(snps_values.iloc[:, :-2]).copy()

    for stat in binned_values.columns[5:-1]:
        binned_values[stat] -= (
            binned_values.loc[:, [stat, "freq_bins"]]
            .dropna()
            .freq_bins.map(expected[stat])
        )
        binned_values[stat] /= binned_values["freq_bins"].map(stdev[stat])

    binned_values = binned_values.drop(
        ["daf", "freq_bins"], axis=1, inplace=False
    ).copy()
    out = []
    # cut window stats to only SNPs within the window around center
    centers = np.arange(center[0], center[1] + 1e4, 1e4).astype(int)
    iter_c_w = list(product(centers, windows))

    tmp_2 = binned_values.loc[
        (binned_values.center == 6e5) & (binned_values.window == 1e6),
        ~binned_values.columns.isin(
            ["isafe", "delta_ihh", "ihs", "nsl", "center", "window"]
        ),
    ]

    for c, w in iter_c_w:
        tmp_1 = binned_values.loc[
            (binned_values.center == c) & (binned_values.window == 1e6),
            ["iter", "positions", "isafe", "ihs", "nsl"],
        ]
        tmp = pd.merge(tmp_1, tmp_2, how="outer")
        lower = c - w / 2
        upper = c + w / 2
        cut_values = (
            tmp[(tmp["positions"] >= lower) & (tmp["positions"] <= upper)]
            .iloc[:, 2:]
            .mean()
        )

        out.append(cut_values)

    out = pd.concat(out, axis=1).T
    out = pd.concat([pd.DataFrame(iter_c_w), out], axis=1)
    out.columns = ["center", "window"] + list(out.columns)[2:]
    out.insert(0, "iter", _iter)

    out
    return out


################## Haplotype length stats


def ihs_ihh(
    h,
    pos,
    map_pos=None,
    min_ehh=0.05,
    min_maf=0.05,
    include_edges=False,
    gap_scale=20000,
    max_gap=200000,
    is_accessible=None,
):
    """
    Computes iHS (integrated Haplotype Score) and delta iHH (difference in integrated
    haplotype homozygosity) for a given set of haplotypes and positions.
    delta iHH represents the absolute difference in iHH between the
    derived and ancestral alleles.

    Parameters
    ----------
    h : numpy.ndarray
        A 2D array of haplotypes where each row corresponds to a SNP (variant), and each
        column corresponds to a haplotype for an individual. The entries are expected to
        be binary (0 or 1), representing the ancestral and derived alleles.

    pos : numpy.ndarray
        A 1D array of physical positions corresponding to the SNPs in `h`. The length
        of `pos` should match the number of rows in `h`.

    map_pos : numpy.ndarray or None, optional (default=None)
        A 1D array representing the genetic map positions (in centiMorgans or other genetic distance)
        corresponding to the SNPs. If None, physical positions (`pos`) are used instead to compute
        gaps between SNPs for EHH integration.

    min_ehh : float, optional (default=0.05)
        The minimum EHH value required for integration. EHH values below this threshold are ignored
        when calculating iHH.

    min_maf : float, optional (default=0.05)
        The minimum minor allele frequency (MAF) required for computing iHS. Variants with lower MAF
        are excluded from the analysis.

    include_edges : bool, optional (default=False)
        Whether to include SNPs at the edges of the haplotype array when calculating iHH. If False,
        edge SNPs may be excluded if they don't meet the `min_ehh` threshold.

    gap_scale : int, optional (default=20000)
        The scaling factor for gaps between consecutive SNPs, used when computing iHH over physical
        distances. If `map_pos` is provided, this scaling factor is not used.

    max_gap : int, optional (default=200000)
        The maximum allowed gap between SNPs when integrating EHH. Gaps larger than this are capped
        to `max_gap` to avoid overly large contributions from distant SNPs.

    is_accessible : numpy.ndarray or None, optional (default=None)
        A boolean array of the same length as `pos`, indicating whether each SNP is in a genomic region
        accessible for analysis (e.g., non-repetitive or non-masked regions). If None, all SNPs are
        assumed to be accessible.

    Returns
    -------
    df_ihs : pandas.DataFrame
        A DataFrame containing the following columns:
        - "positions": The physical positions of the SNPs.
        - "daf": The derived allele frequency (DAF) at each SNP.
        - "ihs": The iHS value for each SNP.
        - "delta_ihh": The absolute difference in integrated haplotype homozygosity (iHH) between
          the derived and ancestral alleles at each SNP.

    Notes
    -----
    - The function first computes the iHH (integrated haplotype homozygosity) for both the forward
      and reverse scans of the haplotypes. iHH represents the area under the EHH decay curve, which
      measures the extent of haplotype homozygosity extending from the focal SNP.
    - iHS is calculated as the natural logarithm of the ratio of iHH for the ancestral and derived
      alleles at each SNP.
    - SNPs with missing or invalid iHS values (e.g., due to low MAF) are removed from the output DataFrame.

    Example Workflow:
    - Compute iHH for forward and reverse directions using the haplotype data.
    - Calculate iHS as `log(iHH_derived / iHH_ancestral)`.
    - Calculate delta iHH as the absolute difference between the iHH values for derived and ancestral alleles.

    """
    # check inputs
    h = asarray_ndim(h, 2)
    check_integer_dtype(h)
    pos = asarray_ndim(pos, 1)
    check_dim0_aligned(h, pos)
    h = memoryview_safe(h)
    pos = memoryview_safe(pos)

    # compute gaps between variants for integration
    gaps = compute_ihh_gaps(pos, map_pos, gap_scale, max_gap, is_accessible)

    # setup kwargs
    kwargs = dict(min_ehh=min_ehh, min_maf=min_maf, include_edges=include_edges)

    # scan forward
    ihh0_fwd, ihh1_fwd = ihh01_scan(h, gaps, **kwargs)

    # scan backward
    ihh0_rev, ihh1_rev = ihh01_scan(h[::-1], gaps[::-1], **kwargs)

    # handle reverse scan
    ihh0_rev = ihh0_rev[::-1]
    ihh1_rev = ihh1_rev[::-1]

    # compute unstandardized score
    ihh0 = ihh0_fwd + ihh0_rev
    ihh1 = ihh1_fwd + ihh1_rev

    # og estimation
    ihs = np.log(ihh0 / ihh1)

    delta_ihh = np.abs(ihh1 - ihh0)

    df_ihs = pd.DataFrame(
        {
            "positions": pos,
            "daf": h.sum(1) / h.shape[1],
            "ihs": ihs,
            "delta_ihh": delta_ihh,
        }
    ).dropna()

    return df_ihs


def run_hapbin(
    hap,
    rec_map,
    _iter=0,
    cutoff=0.05,
    hapbin="/home/jmurgamoreno/software/hapbin/build/ihsbin",
    binom=False,
):
    df_hap = pd.DataFrame(hap)

    df_rec_map = pd.DataFrame(rec_map)

    # Generate a temporary file name
    hap_file = "/tmp/tmp_" + str(_iter) + ".hap"
    map_file = "/tmp/tmp_" + str(_iter) + ".map"

    df_hap.to_csv(hap_file, index=False, header=None, sep=" ")
    df_rec_map.to_csv(map_file, index=False, header=None, sep=" ")

    hapbin_ihs = (
        hapbin
        + " --hap "
        + hap_file
        + " --map "
        + map_file
        + " --minmaf 0.05 --cutoff "
        + str(cutoff)
    )
    if binom:
        hapbin_ihs += " -a"

    with subprocess.Popen(hapbin_ihs.split(), stdout=subprocess.PIPE) as process:
        df_ihs = pd.read_csv(process.stdout, sep="\t").iloc[:, [1, 2, 5]]

    os.remove(hap_file)
    os.remove(map_file)

    df_ihs.columns = ["positions", "daf", "ihs"]
    df_ihs.loc[:, "positions"] = (
        df_rec_map[df_rec_map.iloc[:, 1].isin(df_ihs.positions.values.tolist())]
        .iloc[:, -1]
        .values
    )
    return df_ihs


def haf_top(hap, pos, cutoff=0.1, start=None, stop=None):
    """
    Calculates the Haplotype Allele Frequency (HAF) for the top proportion of haplotypes,
    which is a measure used to summarize haplotype diversity. The function computes the
    HAF statistic for a filtered set of variants and returns the sum of the top `cutoff`
    proportion of the HAF values.

    Parameters
    ----------
    hap : numpy.ndarray
        A 2D array where each row represents a SNP (variant), and each column represents
        a haplotype for an individual. The entries are expected to be binary (0 or 1),
        indicating the presence of ancestral or derived alleles.

    pos : numpy.ndarray
        A 1D array of physical positions corresponding to the SNPs in the `hap` matrix.
        The length of `pos` should match the number of rows in `hap`.

    cutoff : float, optional (default=0.1)
        The proportion of HAF values to exclude from the top and bottom when calculating the final HAF score.
        For example, a `cutoff` of 0.1 excludes the lowest 10% and highest 10% of HAF values,
        and the function returns the sum of the remaining HAF values.

    start : float or None, optional (default=None)
        The starting physical position (in base pairs) for the genomic region of interest.
        If provided, only SNPs at or after this position are included in the calculation.

    stop : float or None, optional (default=None)
        The ending physical position (in base pairs) for the genomic region of interest.
        If provided, only SNPs at or before this position are included in the calculation.

    Returns
    -------
    haf_top : float
        The sum of the top `cutoff` proportion of HAF values, which represents the
        higher end of the haplotype diversity distribution within the specified region.

    Notes
    -----
    - The function first filters the SNPs by the specified genomic region (using `start` and `stop`).
    - HAF (Haplotype Allele Frequency) is computed by summing the pairwise dot product of
      haplotypes and dividing by the total number of haplotypes.
    - The HAF values are sorted, and the top proportion (based on the `cutoff`) is returned.

    """
    if start is not None or stop is not None:
        loc = (pos >= start) & (pos <= stop)
        pos = pos[loc]
        hap = hap[loc, :]

    freqs = hap.sum(axis=1) / hap.shape[1]
    hap_tmp = hap[(freqs > 0) & (freqs < 1)]
    haf_num = (np.dot(hap_tmp.T, hap_tmp) / hap.shape[1]).sum(axis=1)
    haf_den = hap_tmp.sum(axis=0)

    haf = np.sort(haf_num / haf_den)

    idx_low = int(cutoff * haf.size)
    idx_high = int((1 - cutoff) * haf.size)

    # 10% higher
    return haf[idx_high:].sum()


@njit
def process_hap_map(ts, rec_map):
    derived_freq = ts.sum(1) / ts.shape[1]
    okfreq_indices = np.where((derived_freq >= 0.05) & (derived_freq <= 1))[0] + 1

    # okfreq = {i: "yes" for i in okfreq_indices}

    coord = rec_map[okfreq_indices - 1, -1]
    int_coord = (coord // 100) * 100
    coords = {}
    haplos = {}
    true_coords = {}
    count_coords = {}

    coords = {v: "" for v in int_coord}
    for i, v in enumerate(int_coord):
        coord_index = okfreq_indices[i]
        coords[v] += f"{coord[i]} "

        true_coords[coord[i]] = coord_index
        count_coords[coord_index] = coord[i]

        haplos[coord[i]] = "".join(map(str, ts[coord_index - 1]))

    return coords, haplos, true_coords, count_coords


def h12_enard(ts, rec_map, window_size=500000):
    coords, haplos, true_coords, count_coords = process_hap_map(ts, rec_map)

    maxhaplos = {}
    secondhaplos = {}
    thirdhaplos = {}
    keep_haplo_freq = {}

    key_001 = 600000
    coord = key_001
    int_coord = (coord // 100) * 100
    inf = int_coord - window_size // 2
    sup = int_coord + window_size // 2
    hap_line = "1" * ts.shape[1]
    hap = list(hap_line)

    ongoing_haplos = defaultdict(str)

    for i in range(1, window_size // 200):
        inf_i = int_coord - i * 100
        low_bound = inf_i

        if inf_i <= 0:
            break

        if inf_i in coords.keys():
            chain = coords[inf_i]
            splitter_chain = chain.split()
            for true_coord in splitter_chain:
                true_coord = int(true_coord)
                if true_coord != coord:
                    haplotype = haplos[true_coord]
                    current_haplo = list(haplotype)
                    for k, h in enumerate(hap):
                        if h == "1":
                            ongoing_haplos[str(k)] += f"{current_haplo[k]} "

        if i * 100 >= window_size // 2:
            break

    for i in range(1, window_size // 200):
        sup_i = int_coord + i * 100
        up_bound = sup_i

        if sup_i >= 1200000:
            break

        if sup_i in coords.keys():
            chain = coords[sup_i]
            splitter_chain = chain.split()
            for true_coord in splitter_chain:
                true_coord = int(true_coord)
                if true_coord != coord:
                    haplotype = haplos[true_coord]
                    current_haplo = list(haplotype)
                    for k, h in enumerate(hap):
                        if h == "1":
                            ongoing_haplos[str(k)] += f"{current_haplo[k]} "

        if i * 100 >= window_size // 2:
            break

    haplos_number = defaultdict(int)
    for key_ongo in sorted(ongoing_haplos.keys()):
        haplo = ongoing_haplos[key_ongo]
        haplos_number[haplo] += 1

    max_haplo = ""
    second_haplo = ""
    third_haplo = ""

    best_haplos = {}
    revert_number = defaultdict(str)

    # Populate revert_number dictionary
    for key_numb in sorted(haplos_number.keys()):
        number = haplos_number[key_numb]
        revert_number[number] += f"{key_numb}_"

    counter_rev = 0
    done_rev = 0

    # Sort revert_number keys in descending order and process
    for key_rev in sorted(revert_number.keys(), reverse=True):
        chain = revert_number[key_rev]
        splitter_chain = chain.split("_")
        for f, haplo in enumerate(splitter_chain):
            if haplo:  # Check if the haplo is not empty
                done_rev += 1
                best_haplos[done_rev] = haplo
                keep_haplo_freq[done_rev] = key_rev

        counter_rev += done_rev

        if counter_rev >= 10:
            break

    similar_pairs = defaultdict(str)
    done = {}

    # Ensure best_haplos has string keys
    best_haplos = {str(k): v for k, v in best_haplos.items()}

    # Initialize similar_pairs
    for key_compf in sorted(best_haplos.keys(), key=int):
        similar_pairs[key_compf] = ""

    sorted_keys = sorted(best_haplos.keys(), key=int)  # Sort keys only once

    # Pre-split haplotypes to avoid calling split() multiple times
    split_haplos = {key: best_haplos[key].split() for key in sorted_keys}

    for i, key_comp in enumerate(sorted_keys):
        haplo_1 = split_haplos[key_comp]

        for key_comp2 in sorted_keys:
            # Only compare each pair once (key_comp < key_comp2)
            if key_comp != key_comp2:
                pair_key_1_2 = f"{key_comp} {key_comp2}"

                if pair_key_1_2 not in done:
                    # print(pair_key_1_2)
                    haplo_2 = split_haplos[key_comp2]

                    # Compare the two haplotypes using optimized compare_haplos
                    identical, different, total = compare_haplos(haplo_1, haplo_2)

                    if total > 0 and different / total <= 0.2:
                        similar_pairs[key_comp] += f"{key_comp2} "
                        done[pair_key_1_2] = "yes"
                        done[f"{key_comp2} {key_comp}"] = "yes"

    exclude = {}
    counter_rev2 = 0
    max_haplo = ""
    second_haplo = ""
    third_haplo = ""

    for key_rev2 in sorted(similar_pairs, key=int):
        if key_rev2 not in exclude:
            chain = best_haplos[key_rev2]
            similar = similar_pairs[key_rev2]
            if similar != "":
                splitter_similar = similar.split()
                for cur_rev in splitter_similar:
                    exclude[cur_rev] = "yes"
                    chain += "_" + best_haplos[cur_rev]

            counter_rev2 += 1

            if counter_rev2 == 1:
                max_haplo = chain
            elif counter_rev2 == 2:
                second_haplo = chain
            elif counter_rev2 == 3:
                third_haplo = chain
                break

    freq_1 = 0
    freq_2 = 0
    freq_3 = 0
    toto = 0

    for key_ongo2 in sorted(ongoing_haplos.keys()):
        ongoing = ongoing_haplos[key_ongo2]
        toto += 1

        if ongoing in max_haplo:
            freq_1 += 1
        elif ongoing in second_haplo:
            freq_2 += 1
        elif ongoing in third_haplo:
            freq_3 += 1

    H12 = ((freq_1 / toto) + (freq_2 / toto)) ** 2

    return H12


def compare_haplos(haplo_1, haplo_2):
    identical = haplo_1.count("1")  # Count "1"s in haplo_1
    different = sum(1 for h1, h2 in zip(haplo_1, haplo_2) if h1 != h2)
    total = identical + different  # Total equals identical + different

    return identical, different, total


def run_h12(
    hap,
    rec_map,
    _iter=1,
    neutral=True,
    script="/home/jmurgamoreno/software/calculate_H12_modified.pl",
):
    df_hap = pd.DataFrame(hap)
    df_rec_map = pd.DataFrame(rec_map)
    hap_file = "/tmp/tmp_" + str(_iter) + ".hap"
    map_file = "/tmp/tmp_" + str(_iter) + ".map"
    with open(hap_file, "w") as f:
        for row in df_hap.itertuples(index=False, name=None):
            f.write("".join(map(str, row)) + "\n")

    df_rec_map.to_csv(map_file, index=False, header=None, sep=" ")

    h12_enard = "perl " + script + " " + hap_file + " " + map_file + " out "
    h12_enard += "500000 " if neutral else "1200000"

    with subprocess.Popen(h12_enard.split(), stdout=subprocess.PIPE) as process:
        h12_v = float(process.stdout.read())

    os.remove(hap_file)
    os.remove(map_file)

    return h12_v


################## FS stats


@njit
def sq_freq_pairs(hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size):
    # Compute counts and freqs once, then iter pairs combinations
    hap_derived = hap
    hap_ancestral = np.bitwise_xor(hap_derived, 1)

    derived_count = ac[:, 1]
    ancestral_count = ac[:, 0]
    # freqs = ac.to_frequencies()[:, 1]
    freqs = ac[:, 1] / ac.sum(axis=1)
    focal_filter = (freqs >= min_focal_freq) & (freqs <= max_focal_freq)

    focal_derived = hap_derived[focal_filter, :]
    focal_derived_count = derived_count[focal_filter]
    focal_ancestral = hap_ancestral[focal_filter, :]
    focal_ancestral_count = ancestral_count[focal_filter]
    focal_index = focal_filter.nonzero()[0]

    sq_out = []
    info = []
    for j in range(len(focal_index)):
        i = focal_index[j]

        # Calculate the size of the window
        size = window_size / 2

        # Find indices within the window
        z = np.flatnonzero(np.abs(rec_map[i, -1] - rec_map[:, -1]) <= size)

        # Determine indices for slicing the arrays
        x_r, y_r = (i + 1, z[-1])
        x_l, y_l = (z[0], i - 1)

        derived_l = hap_derived[x_l : (y_l + 1), :]
        derived_count_l = derived_count[x_l : (y_l + 1)]

        derived_r = hap_derived[x_r : (y_r + 1), :]
        derived_count_r = derived_count[x_r : (y_r + 1)]

        f_d_l = (focal_derived[j] & derived_l).sum(axis=1) / focal_derived_count[j]
        f_a_l = (focal_ancestral[j] & derived_l).sum(axis=1) / focal_ancestral_count[j]
        f_tot_l = freqs[x_l : y_l + 1]

        f_d_r = (focal_derived[j] & derived_r).sum(axis=1) / focal_derived_count[j]
        f_a_r = (focal_ancestral[j] & derived_r).sum(axis=1) / focal_ancestral_count[j]
        f_tot_r = freqs[x_r : y_r + 1]

        sq_freqs = np.concatenate(
            (
                np.vstack((f_d_l[::-1], f_a_l[::-1], f_tot_l[::-1])).T,
                np.vstack((f_d_r, f_a_r, f_tot_r)).T,
            )
        )

        sq_out.append(sq_freqs)

        info.append(
            (rec_map[i, -1], freqs[i], focal_derived_count[j], focal_ancestral_count[j])
        )

    return (sq_out, info)


def s_ratio(
    hap,
    ac,
    rec_map,
    max_ancest_freq=1,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )
    results = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        f_d2 = np.zeros(f_d.shape)
        f_a2 = np.zeros(f_a.shape)

        f_d2[(f_d > 0.0000001) & (f_d < 1)] = 1
        f_a2[(f_a > 0.0000001) & (f_a < 1)] = 1

        num = (f_d2 - f_d2 + f_a2 + 1).sum()
        den = (f_a2 - f_a2 + f_d2 + 1).sum()
        # redefine to add one to get rid of blowup issue introduced by adding 0.001 to denominator

        s_ratio_v = num / den
        s_ratio_v_flip = den / num
        results.append((s_ratio_v, s_ratio_v_flip))

    try:
        # out = np.hstack([info, np.array(results).reshape(len(results), 1)])
        out = np.hstack([info, np.array(results)])
        df_out = pd.DataFrame(
            out[:, [0, 1, 4, 5]],
            columns=["positions", "daf", "s_ratio", "s_ratio_flip"],
        )
    except:
        df_out = pd.DataFrame(
            [], columns=["positions", "daf", "s_ratio", "s_ratio_flip"]
        )

    return df_out


def dind(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )

    results = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        focal_derived_count = info[i][-2]
        focal_ancestral_count = info[i][-1]

        f_d2 = f_d * (1 - f_d) * focal_derived_count / (focal_derived_count - 1)
        f_a2 = (
            f_a
            * (1 - f_a)
            * focal_ancestral_count
            / (focal_ancestral_count - 1 + 0.001)
        )

        num = (f_d2 - f_d2 + f_a2).sum()
        den = (f_a2 - f_a2 + f_d2).sum() + 0.001

        dind_v = num / den
        dind_v_flip = den / num

        results.append((dind_v, dind_v_flip))

    # out = np.hstack([info, np.array(results).reshape(len(results), 1)])
    out = np.hstack([info, np.array(results)])

    df_out = pd.DataFrame(
        out[:, [0, 1, 4, 5]], columns=["positions", "daf", "dind", "dind_flip"]
    )

    return df_out


def high_freq(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )

    results = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        f_diff = f_d[f_d > max_ancest_freq] ** 2
        f_diff_flip = f_a[f_a > max_ancest_freq] ** 2

        hf_v = f_diff.sum() / len(f_diff)
        hf_v_flip = f_diff_flip.sum() / len(f_diff_flip)
        results.append((hf_v, hf_v_flip))

    # out = np.hstack([info, np.array(results).reshape(len(results), 1)])
    out = np.hstack([info, np.array(results)])

    df_out = pd.DataFrame(
        out[:, [0, 1, 4, 5]],
        columns=["positions", "daf", "high_freq", "high_freq_flip"],
    )

    return df_out


def low_freq(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )
    results = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        f_diff = (1 - f_d[f_d < max_ancest_freq]) ** 2
        f_diff_flip = (1 - f_a[f_a < max_ancest_freq]) ** 2

        lf_v = f_diff.sum() / len(f_diff)
        lf_v_flip = f_diff_flip.sum() / len(f_diff_flip)
        results.append((lf_v, lf_v_flip))

    # out = np.hstack([info, np.array(results).reshape(len(results), 1)])
    out = np.hstack([info, np.array(results)])

    df_out = pd.DataFrame(
        out[:, [0, 1, 4, 5]], columns=["positions", "daf", "low_freq", "low_freq_flip"]
    )

    return df_out


def hapdaf_o(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0.25,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )

    results = []
    nan_index = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]
        f_tot = v[:, 2]

        f_d2 = (
            f_d[(f_d > f_a) & (f_a <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )
        f_a2 = (
            f_a[(f_d > f_a) & (f_a <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )

        # Flipping derived to ancestral, ancestral to derived
        f_d2f = (
            f_a[(f_a > f_d) & (f_d <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )
        f_a2f = (
            f_d[(f_a > f_d) & (f_d <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )

        if len(f_d2) != 0 and len(f_a2) != 0:
            hapdaf = (f_d2 - f_a2).sum() / f_d2.shape[0]
        else:
            hapdaf = np.nan

        if len(f_d2f) != 0 and len(f_a2f) != 0:
            hapdaf_flip = (f_d2f - f_a2f).sum() / f_d2f.shape[0]
        else:
            hapdaf_flip = np.nan

        results.append((hapdaf, hapdaf_flip))

    try:
        out = np.hstack(
            [
                info,
                np.array(results),
                # np.array(results).reshape(len(results), 1),
            ]
        )
        df_out = pd.DataFrame(
            out[:, [0, 1, 4, 5]],
            columns=["positions", "daf", "hapdaf_o", "hapdaf_o_flip"],
        )
    except:
        df_out = pd.DataFrame(
            [], columns=["positions", "daf", "hapdaf_o", "hapdaf_o_flip"]
        )

    return df_out


def hapdaf_s(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.1,
    min_tot_freq=0.1,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )
    results = []
    nan_index = []
    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]
        f_tot = v[:, 2]

        f_d2 = (
            f_d[(f_d > f_a) & (f_a <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )
        f_a2 = (
            f_a[(f_d > f_a) & (f_a <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )

        # Flipping derived to ancestral, ancestral to derived
        f_d2f = (
            f_a[(f_a > f_d) & (f_d <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )
        f_a2f = (
            f_d[(f_a > f_d) & (f_d <= max_ancest_freq) & (f_tot >= min_tot_freq)] ** 2
        )

        if len(f_d2) != 0 and len(f_a2) != 0:
            hapdaf = (f_d2 - f_a2).sum() / f_d2.shape[0]
        else:
            hapdaf = np.nan

        if len(f_d2f) != 0 and len(f_a2f) != 0:
            hapdaf_flip = (f_d2f - f_a2f).sum() / f_d2f.shape[0]
        else:
            hapdaf_flip = np.nan

        results.append((hapdaf, hapdaf_flip))

    try:
        out = np.hstack(
            [
                info,
                np.array(results),
                # np.array(results).reshape(len(results), 1),
            ]
        )
        df_out = pd.DataFrame(
            out[:, [0, 1, 4, 5]],
            columns=["positions", "daf", "hapdaf_s", "hapdaf_s_flip"],
        )
    except:
        df_out = pd.DataFrame(
            [], columns=["positions", "daf", "hapdaf_s", "hapdaf_s_flip"]
        )

    return df_out


@njit
def sq_freq_pairs(hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size):
    # Compute counts and frequencies
    hap_derived = hap
    hap_ancestral = np.bitwise_xor(hap_derived, 1)
    derived_count = ac[:, 1]
    ancestral_count = ac[:, 0]
    freqs = ac[:, 1] / ac.sum(axis=1)

    # Focal filter
    focal_filter = (freqs >= min_focal_freq) & (freqs <= max_focal_freq)
    focal_derived = hap_derived[focal_filter, :]
    focal_derived_count = derived_count[focal_filter]
    focal_ancestral = hap_ancestral[focal_filter, :]
    focal_ancestral_count = ancestral_count[focal_filter]
    focal_index = focal_filter.nonzero()[0]

    # Allocate fixed-size lists to avoid growing lists
    sq_out = [np.zeros((0, 3))] * len(focal_index)
    # info = [None] * len(focal_index)
    info = np.zeros((len(focal_index), 4))
    # Main loop to calculate frequencies
    for j in range(len(focal_index)):
        i = focal_index[j]
        size = window_size / 2

        # Find indices within the window
        z = np.flatnonzero(np.abs(rec_map[i, -1] - rec_map[:, -1]) <= size)

        # Index range
        x_r, y_r = i + 1, z[-1]
        x_l, y_l = z[0], i - 1

        # Calculate derived and ancestral frequencies
        f_d_l = (
            np.sum(focal_derived[j] & hap_derived[x_l : y_l + 1], axis=1)
            / focal_derived_count[j]
        )
        f_a_l = (
            np.sum(focal_ancestral[j] & hap_derived[x_l : y_l + 1], axis=1)
            / focal_ancestral_count[j]
        )
        f_tot_l = freqs[x_l : y_l + 1]

        f_d_r = (
            np.sum(focal_derived[j] & hap_derived[x_r : y_r + 1], axis=1)
            / focal_derived_count[j]
        )
        f_a_r = (
            np.sum(focal_ancestral[j] & hap_derived[x_r : y_r + 1], axis=1)
            / focal_ancestral_count[j]
        )
        f_tot_r = freqs[x_r : y_r + 1]

        # Concatenate frequencies into a single array
        sq_freqs = np.empty((f_d_l.size + f_d_r.size, 3))
        sq_freqs[: f_d_l.size, 0] = f_d_l[::-1]
        sq_freqs[: f_d_l.size, 1] = f_a_l[::-1]
        sq_freqs[: f_d_l.size, 2] = f_tot_l[::-1]
        sq_freqs[f_d_l.size :, 0] = f_d_r
        sq_freqs[f_d_l.size :, 1] = f_a_r
        sq_freqs[f_d_l.size :, 2] = f_tot_r

        sq_out[j] = sq_freqs
        info[j] = np.array(
            [rec_map[i, -1], freqs[i], focal_derived_count[j], focal_ancestral_count[j]]
        )

    return sq_out, info


def dind_high_low(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )

    results_dind = []
    results_high = []
    results_low = []

    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        focal_derived_count = info[i][-2]
        focal_ancestral_count = info[i][-1]

        f_d2 = f_d * (1 - f_d) * focal_derived_count / (focal_derived_count - 1)
        f_a2 = (
            f_a
            * (1 - f_a)
            * focal_ancestral_count
            / (focal_ancestral_count - 1 + 0.001)
        )

        num = (f_d2 - f_d2 + f_a2).sum()
        den = (f_a2 - f_a2 + f_d2).sum() + 0.001

        dind_v = num / den
        dind_v_flip = den / num

        if np.isinf(dind_v):
            dind_v = np.nan

        if np.isinf(dind_v_flip):
            dind_v_flip = np.nan

        hap_dind = (dind_v, dind_v_flip)
        #####
        f_diff = f_d[f_d > max_ancest_freq] ** 2
        f_diff_flip = f_a[f_a > max_ancest_freq] ** 2

        hf_v = f_diff.sum() / len(f_diff)
        hf_v_flip = f_diff_flip.sum() / len(f_diff_flip)

        hap_high = (hf_v, hf_v_flip)
        #####

        f_diff = (1 - f_d[f_d < max_ancest_freq]) ** 2
        f_diff_flip = (1 - f_a[f_a < max_ancest_freq]) ** 2

        lf_v = f_diff.sum() / len(f_diff)
        lf_v_flip = f_diff_flip.sum() / len(f_diff_flip)
        hap_low = (lf_v, lf_v_flip)
        #####
        results_dind.append(hap_dind)
        results_high.append(hap_high)
        results_low.append(hap_low)

    try:
        out = np.hstack(
            [
                info,
                np.array(results_dind),
                np.array(results_high),
                np.array(results_low),
            ]
        )
        df_out = pd.DataFrame(
            out[:, [0, 1, 4, 5, 6, 7, 8, 9]],
            columns=[
                "positions",
                "daf",
                "dind",
                "dind_flip",
                "high_freq",
                "high_freq_flip",
                "low_freq",
                "low_freq_flip",
            ],
        )
    except:
        df_out = pd.DataFrame(
            [],
            columns=[
                "positions",
                "daf",
                "dind",
                "dind_flip",
                "high_freq",
                "high_freq_flip",
                "low_freq",
                "low_freq_flip",
            ],
        )

    return df_out


def dind_high_low2(
    hap,
    ac,
    rec_map,
    max_ancest_freq=0.25,
    min_tot_freq=0,
    min_focal_freq=0.25,
    max_focal_freq=0.95,
    window_size=50000,
):
    # Extract frequency pairs and info array
    sq_freqs, info = sq_freq_pairs(
        hap, ac, rec_map, min_focal_freq, max_focal_freq, window_size
    )

    # Pre-allocate arrays for results to avoid growing lists
    n_rows = len(sq_freqs)
    results_dind = np.empty((n_rows, 2), dtype=np.float64)
    results_high = np.empty((n_rows, 2), dtype=np.float64)
    results_low = np.empty((n_rows, 2), dtype=np.float64)

    # Main computation loop
    for i, v in enumerate(sq_freqs):
        f_d = v[:, 0]
        f_a = v[:, 1]

        focal_derived_count = info[i][-2]
        focal_ancestral_count = info[i][-1]

        # Calculate derived and ancestral components with in-place operations
        f_d2 = f_d * (1 - f_d) * focal_derived_count / (focal_derived_count - 1)
        f_a2 = (
            f_a
            * (1 - f_a)
            * focal_ancestral_count
            / (focal_ancestral_count - 1 + 0.001)
        )

        # Calculate dind values
        num = (f_d2 - f_d2 + f_a2).sum()
        den = (f_a2 - f_a2 + f_d2).sum() + 0.001
        dind_v = num / den if not np.isinf(num / den) else np.nan
        dind_v_flip = den / num if not np.isinf(den / num) else np.nan

        results_dind[i] = [dind_v, dind_v_flip]

        # Calculate high and low frequency values
        hf_v = (f_d[f_d > max_ancest_freq] ** 2).sum() / max(
            len(f_d[f_d > max_ancest_freq]), 1
        )
        hf_v_flip = (f_a[f_a > max_ancest_freq] ** 2).sum() / max(
            len(f_a[f_a > max_ancest_freq]), 1
        )
        results_high[i] = [hf_v, hf_v_flip]

        lf_v = ((1 - f_d[f_d < max_ancest_freq]) ** 2).sum() / max(
            len(f_d[f_d < max_ancest_freq]), 1
        )
        lf_v_flip = ((1 - f_a[f_a < max_ancest_freq]) ** 2).sum() / max(
            len(f_a[f_a < max_ancest_freq]), 1
        )
        results_low[i] = [lf_v, lf_v_flip]

        # Free memory explicitly for large arrays
        del f_d, f_a, f_d2, f_a2

    # Final DataFrame creation
    try:
        out = np.hstack([info, results_dind, results_high, results_low])
        df_out = pd.DataFrame(
            out[:, [0, 1, 4, 5, 6, 7, 8, 9]],
            columns=[
                "positions",
                "daf",
                "dind",
                "dind_flip",
                "high_freq",
                "high_freq_flip",
                "low_freq",
                "low_freq_flip",
            ],
        )
    except:
        df_out = pd.DataFrame(
            [],
            columns=[
                "positions",
                "daf",
                "dind",
                "dind_flip",
                "high_freq",
                "high_freq_flip",
                "low_freq",
                "low_freq_flip",
            ],
        )

    return df_out


################## iSAFE


@njit("int64[:](float64[:])", cache=True)
def rank_with_duplicates(x):
    # sorted_arr = sorted(x, reverse=True)
    sorted_arr = np.sort(x)[::-1]
    rank_dict = {}
    rank = 1
    prev_value = -1

    for value in sorted_arr:
        if value != prev_value:
            rank_dict[value] = rank
        rank += 1
        prev_value = value

    return np.array([rank_dict[value] for value in x])


# @njit("float64[:,:](float64[:,:])", cache=True)
@njit(parallel=False)
def dot_nb(hap):
    return np.dot(hap.T, hap)


@njit
def dot_two_nb(x, y):
    return np.dot(x, y)


@njit
def neutrality_divergence_proxy(kappa, phi, freq, method=3):
    sigma1 = (kappa) * (1 - kappa)
    sigma1[sigma1 == 0] = 1.0
    sigma1 = sigma1**0.5
    p1 = (phi - kappa) / sigma1
    sigma2 = (freq) * (1 - freq)
    sigma2[sigma2 == 0] = 1.0
    sigma2 = sigma2**0.5
    p2 = (phi - kappa) / sigma2
    nu = freq[np.argmax(p1)]
    p = p1 * (1 - nu) + p2 * nu

    if method == 1:
        return p1
    elif method == 2:
        return p2
    elif method == 3:
        return p


@njit
def calc_H_K(hap, haf):
    """
    :param snp_matrix: Binary SNP Matrix
    :return: H: Sum of HAF-score of carriers of each mutation.
    :return: N: Number of distinct carrier haplotypes of each mutation.

    """
    num_snps, num_haplotypes = hap.shape

    haf_matrix = haf * hap

    K = np.zeros((num_snps))

    for j in range(num_snps):
        ar = haf_matrix[j, :]
        K[j] = len(np.unique(ar[ar > 0]))
    H = np.sum(haf_matrix, 1)
    return (H, K)


def safe(hap):
    num_snps, num_haplotypes = hap.shape

    haf = dot_nb(hap.astype(np.float64)).sum(1)
    # haf = np.dot(hap.T, hap).sum(1)
    H, K = calc_H_K(hap, haf)

    phi = 1.0 * H / haf.sum()
    kappa = 1.0 * K / (np.unique(haf).shape[0])
    freq = hap.sum(1) / num_haplotypes
    safe_values = neutrality_divergence_proxy(kappa, phi, freq)

    # rank = np.zeros(safe_values.size)
    # rank = rank_with_duplicates(safe_values)
    rank = (
        pd.DataFrame(safe_values).rank(method="min", ascending=False).values.flatten()
    )

    return haf, safe_values, rank, phi, kappa, freq


def creat_windows_summary_stats_nb(hap, pos, w_size=300, w_step=150):
    num_snps, num_haplotypes = hap.shape
    rolling_indices = create_rolling_indices_nb(num_snps, w_size, w_step)
    windows_stats = {}
    windows_haf = []
    snp_summary = []
    for i, I in enumerate(rolling_indices):
        window_i_stats = {}
        haf, safe_values, rank, phi, kappa, freq = safe(hap[I[0] : I[1], :])
        tmp = pd.DataFrame(
            np.asarray(
                [
                    safe_values,
                    rank,
                    phi,
                    kappa,
                    freq,
                    pos[I[0] : I[1]],
                    np.arange(I[0], I[1]),
                    np.repeat(i, w_size),
                ]
            ).T,
            columns=[
                "safe",
                "rank",
                "phi",
                "kappa",
                "freq",
                "pos",
                "ordinal_pos",
                "window",
            ],
        )
        # tmp = np.vstack((safe_values, rank, phi, kappa, freq, pos[I[0]:I[1]],np.arange(I[0],I[1]),np.repeat(i,w_size))).T
        window_i_stats["safe"] = tmp
        windows_haf.append(haf)
        windows_stats[i] = window_i_stats
        snp_summary.append(tmp)
    return (
        windows_stats,
        windows_haf,
        pd.concat(snp_summary).reset_index(drop=True).astype(float),
    )


@njit
def create_rolling_indices_nb(total_variant_count, w_size, w_step):
    assert total_variant_count < w_size or w_size > 0

    rolling_indices = []
    w_start = 0
    while True:
        w_end = min(w_start + w_size, total_variant_count)
        if w_end >= total_variant_count:
            break
        rolling_indices.append([w_start, w_end])
        # rolling_indices += [range(int(w_start), int(w_end))]
        w_start += w_step

    return rolling_indices


def run_isafe(
    hap,
    positions,
    max_freq=1,
    min_region_size_bp=49000,
    min_region_size_ps=300,
    ignore_gaps=True,
    window=300,
    step=150,
    top_k=1,
    max_rank=15,
):
    """
    Estimate iSAFE or SAFE when not possible using default Flex-Sweep values.

    Args:
     hap (TYPE): Description
     total_window_size (TYPE): Description
     positions (TYPE): Description
     max_freq (int, optional): Description
     min_region_size_bp (int, optional): Description
     min_region_size_ps (int, optional): Description
     ignore_gaps (bool, optional): Description
     window (int, optional): Description
     step (int, optional): Description
     top_k (int, optional): Description
     max_rank (int, optional): Description

    Returns:
     TYPE: Description

    Raises:
     ValueError: Description
    """

    total_window_size = positions.max() - positions.min()

    dp = np.diff(positions)
    num_gaps = sum(dp > 6000000)
    f = hap.mean(1)
    freq_filter = ((1 - f) * f) > 0
    hap_filtered = hap[freq_filter, :]
    positions_filtered = positions[freq_filter]
    num_snps = hap_filtered.shape[0]

    if (num_snps <= min_region_size_ps) | (total_window_size < min_region_size_bp):
        haf, safe_values, rank, phi, kappa, freq = safe(hap_filtered)

        df_safe = pd.DataFrame(
            np.asarray(
                [
                    safe_values,
                    rank,
                    phi,
                    kappa,
                    freq,
                    positions_filtered,
                ]
            ).T,
            columns=["isafe", "rank", "phi", "kappa", "daf", "positions"],
        )

        return df_safe.loc[:, ["positions", "daf", "isafe"]].sort_values("positions")
    else:
        df_isafe = isafe(
            hap_filtered, positions_filtered, window, step, top_k, max_rank
        )
        df_isafe = (
            df_isafe.loc[df_isafe.freq < max_freq]
            .sort_values("ordinal_pos")
            .rename(columns={"id": "positions", "isafe": "isafe", "freq": "daf"})
        )

        df_isafe = df_isafe[df_isafe.daf < max_freq]
        return df_isafe.loc[:, ["positions", "daf", "isafe"]]


def isafe(hap, pos, w_size=300, w_step=150, top_k=1, max_rank=15):
    windows_summaries, windows_haf, snps_summary = creat_windows_summary_stats_nb(
        hap, pos, w_size, w_step
    )
    df_top_k1 = get_top_k_snps_in_each_window(snps_summary, k=top_k)

    ordinal_pos_snps_k1 = np.sort(df_top_k1["ordinal_pos"].unique()).astype(np.int64)

    psi_k1 = step_function(creat_matrix_Psi_k_nb(hap, windows_haf, ordinal_pos_snps_k1))

    df_top_k2 = get_top_k_snps_in_each_window(snps_summary, k=max_rank)
    temp = np.sort(df_top_k2["ordinal_pos"].unique())

    ordinal_pos_snps_k2 = np.sort(np.setdiff1d(temp, ordinal_pos_snps_k1)).astype(
        np.int64
    )

    psi_k2 = step_function(creat_matrix_Psi_k_nb(hap, windows_haf, ordinal_pos_snps_k2))

    alpha = psi_k1.sum(0) / psi_k1.sum()

    iSAFE1 = pd.DataFrame(
        data={"ordinal_pos": ordinal_pos_snps_k1, "isafe": np.dot(psi_k1, alpha)}
    )
    iSAFE2 = pd.DataFrame(
        data={"ordinal_pos": ordinal_pos_snps_k2, "isafe": np.dot(psi_k2, alpha)}
    )

    iSAFE1["tier"] = 1
    iSAFE2["tier"] = 2
    iSAFE = pd.concat([iSAFE1, iSAFE2]).reset_index(drop=True)
    iSAFE["id"] = pos[iSAFE["ordinal_pos"].values]
    freq = hap.mean(1)
    iSAFE["freq"] = freq[iSAFE["ordinal_pos"]]
    df_isafe = iSAFE[["ordinal_pos", "id", "isafe", "freq", "tier"]]

    return df_isafe


@njit
def creat_matrix_Psi_k_nb(hap, hafs, Ifp):
    P = np.zeros((len(Ifp), len(hafs)))
    for i in range(len(Ifp)):
        for j in range(len(hafs)):
            P[i, j] = isafe_kernel_nb(hafs[j], hap[Ifp[i], :])
    return P


@njit
def isafe_kernel_nb(haf, snp):
    phi = haf[snp == 1].sum() * 1.0 / haf.sum()
    kappa = len(np.unique(haf[snp == 1])) / (1.0 * len(np.unique(haf)))
    f = np.mean(snp)
    sigma2 = (f) * (1 - f)
    if sigma2 == 0:
        sigma2 = 1.0
    sigma = sigma2**0.5
    p = (phi - kappa) / sigma
    return p


def step_function(P0):
    P = P0.copy()
    P[P < 0] = 0
    return P


def get_top_k_snps_in_each_window(df_snps, k=1):
    """
    :param df_snps:  this datafram must have following columns: ["safe","ordinal_pos","window"].
    :param k:
    :return: return top k snps in each window.
    """
    return df_snps.loc[
        df_snps.groupby("window")["safe"].nlargest(k).index.get_level_values(1), :
    ].reset_index(drop=True)


################## LD stats


def Ld(
    hap: np.ndarray, pos: np.ndarray, min_freq=0.05, max_freq=1, start=None, stop=None
) -> tuple:
    """
    Compute Kelly Zns statistic (1997) and omega_max. Average r2
    among every pair of loci in the genomic window.

    Args:hap (numpy.ndarray): 2D array representing haplotype data. Rows correspond to different mutations, and columnscorrespond to chromosomes.
    pos (numpy.ndarray): 1D array representing the positions of mutations.
    min_freq (float, optional): Minimum frequency threshold. Default is 0.05.
    max_freq (float, optional): Maximum frequency threshold. Default is 1.
    window (int, optional): Genomic window size. Default is 500000.

    Returns:tuple: A tuple containing two values:
    - kelly_zns (float): Kelly Zns statistic.
    - omega_max (float): Nielsen omega max.
    """

    if start is not None or stop is not None:
        loc = (pos >= start) & (pos <= stop)
        pos = pos[loc]
        hap = hap[loc, :]

    freqs = hap.sum(axis=1) / hap.shape[1]

    hap_filter = hap[(freqs >= min_freq) & (freqs <= max_freq)]

    r2_matrix = compute_r2_matrix(hap_filter)
    # r2_matrix = r2_torch(hap_filter)
    S = hap_filter.shape[0]
    zns = r2_matrix.sum() / comb(S, 2)
    # Index combination to iter
    # omega_max = omega(r2_matrix)
    # omega_max = dps.omega(r2_matrix)[0]

    return zns, 0
    # return zns, omega_max


def r2_matrix(
    hap: np.ndarray, pos: np.ndarray, min_freq=0.05, max_freq=1, start=None, stop=None
):
    """
    Compute Kelly Zns statistic (1997) and omega_max. Average r2
    among every pair of loci in the genomic window.

    Args:
        hap (numpy.ndarray): 2D array representing haplotype data. Rows correspond to different mutations, and columns correspond to chromosomes.
        pos (numpy.ndarray): 1D array representing the positions of mutations.
        min_freq (float, optional): Minimum frequency threshold. Default is 0.05.
        max_freq (float, optional): Maximum frequency threshold. Default is 1.
        window (int, optional): Genomic window size. Default is 500000.

    Returns: tuple: A tuple containing two values:
        - kelly_zns (float): Kelly Zns statistic.
        - omega_max (float): Nielsen omega max.
    """

    # if start is not None or stop is not None:
    #     loc = (pos >= start) & (pos <= stop)
    #     pos = pos[loc]
    #     hap = hap[loc, :]

    freqs = hap.sum(axis=1) / hap.shape[1]
    freq_filter = (freqs >= min_freq) & (freqs <= max_freq)
    hap_filter = hap[freq_filter]

    r2_matrix = compute_r2_matrix(hap_filter)
    # r2_matrix = r2_torch(hap_filter)
    # S = hap_filter.shape[0]
    # zns = r2_matrix.sum() / comb(S, 2)
    # Index combination to iter
    # omega_max = omega(r2_matrix)
    # omega_max = dps.omega(r2_matrix)[0]

    return r2_matrix, freq_filter
    # return zns, omega_max


def Ld(
    r2_subset,
    freq_filter,
    pos: np.ndarray,
    min_freq=0.05,
    max_freq=1,
    start=None,
    stop=None,
):
    pos_filter = pos[freq_filter]
    if start is not None or stop is not None:
        loc = (pos_filter >= start) & (pos_filter <= stop)
        pos_filter = pos_filter[loc]
        r2_subset = r2_subset[loc, :][:, loc]

    # r2_subset_matrix = compute_r2_subset_matrix(hap_filter)
    # r2_subset_matrix = r2_subset_torch(hap_filter)
    S = r2_subset.shape[0]
    kelly_zns = r2_subset.sum() / comb(S, 2)
    # omega_max = omega(r2_subset)

    return kelly_zns, 0


@njit("float64(int8[:], int8[:])", cache=True)
def r2(locus_A: np.ndarray, locus_B: np.ndarray) -> float:
    """
    Calculate r^2 and D between the two loci A and B.

    Args: locus_A (numpy.ndarray): 1D array representing alleles at locus A.
    locus_B (numpy.ndarray): 1D array representing alleles at locus B.

    Returns:
        float: r^2 value.
    """
    n = locus_A.size
    # Frequency of allele 1 in locus A and locus B
    a1 = 0
    b1 = 0
    count_a1b1 = 0

    for i in range(n):
        a1 += locus_A[i]
        b1 += locus_B[i]
        count_a1b1 += locus_A[i] * locus_B[i]

    a1 /= n
    b1 /= n
    a1b1 = count_a1b1 / n
    D = a1b1 - a1 * b1

    r_squared = (D**2) / (a1 * (1 - a1) * b1 * (1 - b1))
    return r_squared


@njit("float64[:,:](int8[:,:])", cache=True)
def compute_r2_matrix(hap):
    num_sites = hap.shape[0]

    # r2_matrix = OrderedDict()
    sum_r_squared = 0
    r2_matrix = np.zeros((num_sites, num_sites))
    # Avoid itertool.combination, not working on numba
    # for pair in combinations(range(num_sites), 2):

    # Check index from triangular matrix of size num_sites x num_sites. Each indices correspond to one one dimension of the array. Same as combinations(range(num_sites), 2)
    c_1, c_2 = np.triu_indices(num_sites, 1)

    for i, j in zip(c_1, c_2):
        r2_matrix[i, j] = r2(hap[i, :], hap[j, :])
        # r2_matrix[pair[0], pair[1]] = r2(hap[pair[0], :], hap[pair[1], :])

    return r2_matrix


@njit("float64(float64[:,:])", cache=True)
def omega(r2_matrix):
    """
    Calculates Kim and Nielsen's (2004, Genetics 167:1513) omega_max statistic. Adapted from PG-Alignments-GAN

    Args:r2_matrix (numpy.ndarray): 2D array representing r2 values.

    Returns:
        float: Kim and Nielsen's omega max.
    """

    omega_max = 0
    S_ = r2_matrix.shape[1]

    if S_ < 3:
        omega_max = 0
    else:
        for l_ in range(3, S_ - 2):
            sum_r2_L = 0
            sum_r2_R = 0
            sum_r2_LR = 0

            for i in range(S_):
                for j in range(i + 1, S_):
                    ld_calc = r2_matrix[i, j]
                    if i < l_ and j < l_:
                        sum_r2_L += ld_calc

                    elif i >= l_ and j >= l_:
                        sum_r2_R += ld_calc

                    elif i < l_ and j >= l_:
                        sum_r2_LR += ld_calc

            # l_ ## to keep the math right outside of indexing
            omega_numerator = (
                1 / ((l_ * (l_ - 1) / 2) + ((S_ - l_) * (S_ - l_ - 1) / 2))
            ) * (sum_r2_L + sum_r2_R)
            omega_denominator = (1 / (l_ * (S_ - l_))) * sum_r2_LR

            if omega_denominator == 0:
                omega = 0
            else:
                omega = np.divide(omega_numerator, omega_denominator)

            if omega > omega_max:
                omega_max = omega

    return omega_max


################## Spectrum stats


def fay_wu_h_normalized(hap: np.ndarray, pos, start=None, stop=None) -> tuple:
    """
    Compute Fay-Wu's H test statistic and its normalized version.

    Args:hap (numpy.ndarray): 2D array representing haplotype data. Rows correspond to different mutations, and columns correspond to chromosomes.

    Returns:tuple: A tuple containing two values:
        - h (float): Fay-Wu H test statistic.
        - h_normalized (float): Normalized Fay-Wu H test statistic.
    """

    if start is not None or stop is not None:
        loc = (pos >= start) & (pos <= stop)
        pos = pos[loc]
        hap = hap[loc, :]

    # Count segregating and chromosomes
    S, n = hap.shape
    # Create SFS to count ith mutation in sample
    Si = sfs(hap.sum(axis=1), n)[1:-1]
    # ith mutations
    i = np.arange(1, n)

    # (n-1)th harmonic numbers
    an = np.sum(1 / i)
    bn = np.sum(1 / i**2)
    bn_1 = bn + 1 / (n**2)

    # calculate theta_w absolute value
    theta_w = S / an

    # calculate theta_pi absolute value
    theta_pi = ((2 * Si * i * (n - i)) / (n * (n - 1))).sum()

    # calculate theta_h absolute value
    theta_h = ((2 * Si * np.power(i, 2)) / (n * (n - 1))).sum()

    # calculate theta_l absolute value
    theta_l = (np.arange(1, n) * Si).sum() / (n - 1)

    theta_square = (S * (S - 1)) / (an**2 + bn)

    h = theta_pi - theta_h

    var_1 = (n - 2) / (6 * (n - 1)) * theta_w

    var_2 = (
        (
            (18 * (n**2) * (3 * n + 2) * bn_1)
            - ((88 * (n**3) + 9 * (n**2)) - (13 * n + 6))
        )
        / (9 * n * ((n - 1) ** 2))
    ) * theta_square

    # cov = (((n+1) / (3*(n-1)))*theta_w) + (((7*n*n+3*n-2-4*n*(n+1)*bn_1)/(2*(n-1)**2))*theta_square)

    # var_theta_l = (n * theta_w)/(2.0 * (n - 1.0)) + (2.0 * np.power(n/(n - 1.0), 2.0) * (bn_1 - 1.0) - 1.0) * theta_square;
    # var_theta_pi = (3.0 * n *(n + 1.0) * theta_w + 2.0 * ( n * n + n + 3.0) * theta_square)/ (9 * n * (n -1.0));

    h_normalized = h / np.sqrt(var_1 + var_2)

    # h_prime = h / np.sqrt(var_theta_l+var_theta_pi - 2.0 * cov)

    return (h, h_normalized)


def zeng_e(hap: np.ndarray, pos, start=None, stop=None) -> float:
    """
    Compute Zeng's E test statistic.

    Args:hap (numpy.ndarray): 2D array representing haplotype data. Rows correspond to different mutations, and columnscorrespond to chromosomes.

    Returns:
    float: Zeng's E test statistic.
    """

    if start is not None or stop is not None:
        loc = (pos >= start) & (pos <= stop)
        pos = pos[loc]
        hap = hap[loc, :]

    # Count segregating and chromosomes
    S, n = hap.shape
    # Create SFS to count ith mutation in sample
    Si = sfs(hap.sum(axis=1), n)[1:-1]
    # ith mutations
    i = np.arange(1, n)

    # (n-1)th harmonic numbers
    an = np.sum(1.0 / i)
    bn = np.sum(1.0 / i**2.0)

    # calculate theta_w absolute value
    theta_w = S / an

    # calculate theta_l absolute value
    theta_l = (np.arange(1, n) * Si).sum() / (n - 1)

    theta_square = S * (S - 1.0) / (an**2 + bn)

    # Eq. 14
    var_1 = (n / (2.0 * (n - 1.0)) - 1.0 / an) * theta_w
    var_2 = (
        bn / an**2
        + 2 * (n / (n - 1)) ** 2 * bn
        - 2 * (n * bn - n + 1) / ((n - 1) * an)
        - (3 * n + 1) / (n - 1)
    ) * theta_square

    (
        (bn / an**2)
        + (2 * (n / (n - 1)) ** 2 * bn)
        - (2 * (n * bn - n + 1) / ((n - 1) * an))
        - ((3 * n + 1) / (n - 1)) * theta_square
    )
    e = (theta_l - theta_w) / (var_1 + var_2) ** 0.5
    return e


def fuli_f_star(hap, ac):
    """Calculates Fu and Li's D* statistic"""
    S, n = hap.shape

    an = np.sum(np.divide(1.0, range(1, n)))
    bn = np.sum(np.divide(1.0, np.power(range(1, n), 2)))
    an1 = an + np.true_divide(1, n)

    vfs = (
        (
            (2 * (n**3.0) + 110.0 * (n**2.0) - 255.0 * n + 153)
            / (9 * (n**2.0) * (n - 1.0))
        )
        + ((2 * (n - 1.0) * an) / (n**2.0))
        - ((8.0 * bn) / n)
    ) / ((an**2.0) + bn)
    ufs = (
        (
            n / (n + 1.0)
            + (n + 1.0) / (3 * (n - 1.0))
            - 4.0 / (n * (n - 1.0))
            + ((2 * (n + 1.0)) / ((n - 1.0) ** 2)) * (an1 - ((2.0 * n) / (n + 1.0)))
        )
        / an
    ) - vfs

    pi = mean_pairwise_difference(ac).sum()
    ss = np.sum(np.sum(hap, axis=1) == 1)
    Fstar1 = (pi - (((n - 1.0) / n) * ss)) / ((ufs * S + vfs * (S**2.0)) ** 0.5)
    return Fstar1


def fuli_f(hap, ac):
    an = np.sum(np.divide(1.0, range(1, n)))
    an1 = an + 1.0 / n
    bn = np.sum(np.divide(1.0, np.power(range(1, n), 2)))

    ss = np.sum(np.sum(hap, axis=1) == 1)
    pi = mean_pairwise_difference(ac).sum()

    if n == 2:
        cn = 1
    else:
        cn = 2.0 * (n * an - 2.0 * (n - 1.0)) / ((n - 1.0) * (n - 2.0))

    v = (
        cn + 2.0 * (np.power(n, 2) + n + 3.0) / (9.0 * n * (n - 1.0)) - 2.0 / (n - 1.0)
    ) / (np.power(an, 2) + bn)
    u = (
        1.0
        + (n + 1.0) / (3.0 * (n - 1.0))
        - 4.0 * (n + 1.0) / np.power(n - 1, 2) * (an1 - 2.0 * n / (n + 1.0))
    ) / an - v
    F = (pi - ss) / sqrt(u * S + v * np.power(S, 2))

    return F


def fuli_d_star(hap):
    """Calculates Fu and Li's D* statistic"""

    S, n = hap.shape
    an = np.sum(np.divide(1.0, range(1, n)))
    bn = np.sum(np.divide(1.0, np.power(range(1, n), 2)))
    an1 = an + np.true_divide(1, n)

    cn = 2 * (((n * an) - 2 * (n - 1))) / ((n - 1) * (n - 2))
    dn = (
        cn
        + np.true_divide((n - 2), ((n - 1) ** 2))
        + np.true_divide(2, (n - 1)) * (3.0 / 2 - (2 * an1 - 3) / (n - 2) - 1.0 / n)
    )

    vds = (
        ((n / (n - 1.0)) ** 2) * bn
        + (an**2) * dn
        - 2 * (n * an * (an + 1)) / ((n - 1.0) ** 2)
    ) / (an**2 + bn)
    uds = ((n / (n - 1.0)) * (an - n / (n - 1.0))) - vds

    ss = np.sum(np.sum(hap, axis=1) == 1)
    Dstar1 = ((n / (n - 1.0)) * S - (an * ss)) / (uds * S + vds * (S ^ 2)) ** 0.5
    return Dstar1


def fuli_d(hap):
    S, n = hap.shape

    an = np.sum(np.divide(1.0, range(1, n)))
    bn = np.sum(np.divide(1.0, np.power(range(1, n), 2)))

    ss = np.sum(np.sum(hap, axis=1) == 1)

    if n == 2:
        cn = 1
    else:
        cn = 2.0 * (n * an - 2.0 * (n - 1.0)) / ((n - 1.0) * (n - 2.0))

    v = 1.0 + (np.power(an, 2) / (bn + np.power(an, 2))) * (cn - (n + 1.0) / (n - 1.0))
    u = an - 1.0 - v
    D = (S - ss * an) / sqrt(u * S + v * np.power(S, 2))
    return D


################## LASSI
def get_empir_freqs_np(hap):
    """
    Calculate the empirical frequencies of haplotypes.

    Parameters:
    - hap (numpy.ndarray): Array of haplotypes where each column represents an individual and each row represents a SNP.

    Returns:
    - k_counts (numpy.ndarray): Counts of each unique haplotype.
    - h_f (numpy.ndarray): Empirical frequencies of each unique haplotype.
    """
    S, n = hap.shape

    # Count occurrences of each unique haplotype
    hap_f, k_counts = np.unique(hap, axis=1, return_counts=True)

    # Sort counts in descending order
    k_counts = np.sort(k_counts)[::-1]

    # Calculate empirical frequencies
    h_f = k_counts / n
    return k_counts, h_f


def process_spectra(
    k: np.ndarray, h_f: np.ndarray, K_truncation: int, n_ind: int
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Process haplotype count and frequency spectra.

    Parameters:
    - k (numpy.ndarray): Counts of each unique haplotype.
    - h_f (numpy.ndarray): Empirical frequencies of each unique haplotype.
    - K_truncation (int): Number of haplotypes to consider.
    - n_ind (int): Number of individuals.

    Returns:
    - Kcount (numpy.ndarray): Processed haplotype count spectrum.
    - Kspect (numpy.ndarray): Processed haplotype frequency spectrum.
    """
    # Truncate count and frequency spectrum
    Kcount = k[:K_truncation]
    Kspect = h_f[:K_truncation]

    # Normalize count and frequency spectra
    Kcount = Kcount / Kcount.sum() * n_ind
    Kspect = Kspect / Kspect.sum()

    # Pad with zeros if necessary
    if Kcount.size < K_truncation:
        Kcount = np.concatenate([Kcount, np.zeros(K_truncation - Kcount.size)])
        Kspect = np.concatenate([Kspect, np.zeros(K_truncation - Kspect.size)])

    return Kcount, Kspect


def LASSI_spectrum_and_Kspectrum(
    ts, rec_map, K_truncation: int, window: int, step: int
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Compute haplotype count and frequency spectra within sliding windows.

    Parameters:
    - hap (numpy.ndarray): Array of haplotypes where each column represents an individual and each row represents a SNP.
    - pos (numpy.ndarray): Array of SNP positions.
    - K_truncation (int): Number of haplotypes to consider.
    - window (int): Size of the sliding window.
    - step (int): Step size for sliding the window.

    Returns:
    - K_count (numpy.ndarray): Haplotype count spectra for each window.
    - K_spectrum (numpy.ndarray): Haplotype frequency spectra for each window.
    - windows_centers (numpy.ndarray): Centers of the sliding windows.
    """
    (
        hap_01,
        ac,
        biallelic_mask,
        hap_int,
        rec_map_01,
        position_masked,
        sequence_length,
        freqs,
    ) = filter_gt(ts, rec_map)

    K_count = []
    K_spectrum = []
    windows_centers = []
    S, n = hap_int.shape
    for i in range(0, S, step):
        hap_subset = hap_int[i : i + window, :]

        # Calculate window center based on median SNP position
        windows_centers.append(np.median(position_masked[i : i + window]))

        # Compute empirical frequencies and process spectra for the window
        k, h_f = get_empir_freqs_np(hap_subset)
        K_count_subset, K_spectrum_subset = process_spectra(k, h_f, K_truncation, n)

        K_count.append(K_count_subset)
        K_spectrum.append(K_spectrum_subset)
        if hap_subset.shape[0] < window:
            break

    return np.array(K_count), np.array(K_spectrum), np.array(windows_centers)


def neut_average(K_spectrum: np.ndarray) -> np.ndarray:
    """
    Compute the neutral average of haplotype frequency spectra.

    Parameters:
    - K_spectrum (numpy.ndarray): Haplotype frequency spectra.

    Returns:
    - out (numpy.ndarray): Neutral average haplotype frequency spectrum.
    """
    weights = []
    S, n = K_spectrum.shape
    # Compute mean spectrum
    gwide_K = np.mean(K_spectrum, axis=0)

    # Calculate weights for averaging
    if S % 5e4 == 0:
        weights.append(5e4)
    else:
        small_weight = S % 5e4
        weights.append(small_weight)

    # Compute weighted average
    out = np.average([gwide_K], axis=0, weights=weights)

    return out


@njit("float64(float64[:],float64[:],int64)", cache=True)
def easy_likelihood(K_neutral, K_count, K_truncation):
    """
    Basic computation of the likelihood function; runs as-is for neutrality, but called as part of a larger process for sweep model
    """

    likelihood_list = []

    for i in range(K_truncation):
        likelihood_list.append(K_count[i] * np.log(K_neutral[i]))

    likelihood = sum(likelihood_list)

    return likelihood


@njit("float64(float64[:],float64[:],int64,int64,float64,float64)", cache=True)
def sweep_likelihood(K_neutral, K_count, K_truncation, m_val, epsilon, epsilon_max):
    """
    Computes the likelihood of a sweep under optimized parameters
    """

    if m_val != K_truncation:
        altspect = np.zeros(K_truncation)
        tailclasses = np.zeros(K_truncation - m_val)
        neutdiff = np.zeros(K_truncation - m_val)
        tailinds = np.arange(m_val + 1, K_truncation + 1)

        for i in range(len(tailinds)):
            ti = tailinds[i]
            denom = K_truncation - m_val - 1
            if denom != 0:
                the_ns = epsilon_max - ((ti - m_val - 1) / denom) * (
                    epsilon_max - epsilon
                )
            else:
                the_ns = epsilon
            tailclasses[i] = the_ns
            neutdiff[i] = K_neutral[ti - 1] - the_ns

        headinds = np.arange(1, m_val + 1)

        for hd in headinds:
            altspect[hd - 1] = K_neutral[hd - 1]

        neutdiff_all = np.sum(neutdiff)

        for ival in headinds:
            # class 3
            # total_exp = np.sum(np.exp(-headinds))
            # theadd = (np.exp(-ival) / total_exp) * neutdiff_all
            # class 5
            theadd = (1 / float(m_val)) * neutdiff_all
            altspect[ival - 1] += theadd

        altspect[m_val:] = tailclasses

        output = easy_likelihood(altspect, K_count, K_truncation)
    else:
        output = easy_likelihood(K_neutral, K_count, K_truncation)

    return output


def T_m_statistic(K_counts, K_neutral, windows, K_truncation, sweep_mode=5, i=0):
    output = []
    m_vals = K_truncation + 1
    epsilon_min = 1 / (K_truncation * 100)

    _epsilon_values = list(map(lambda x: x * epsilon_min, range(1, 101)))
    epsilon_max = K_neutral[-1]
    epsilon_values = []

    for ev in _epsilon_values:
        # ev = e * epsilon_min
        if ev <= epsilon_max:
            epsilon_values.append(ev)
    epsilon_values = np.array(epsilon_values)

    for j, w in enumerate(windows):
        # if(i==132):
        # break
        K_iter = K_counts[j]

        null_likelihood = easy_likelihood(K_neutral, K_iter, K_truncation)

        alt_likelihoods_by_e = []

        for e in epsilon_values:
            alt_likelihoods_by_m = []
            for m in range(1, m_vals):
                alt_like = sweep_likelihood(
                    K_neutral, K_iter, K_truncation, m, e, epsilon_max
                )
                alt_likelihoods_by_m.append(alt_like)

            alt_likelihoods_by_m = np.array(alt_likelihoods_by_m)
            likelihood_best_m = 2 * (alt_likelihoods_by_m.max() - null_likelihood)

            if likelihood_best_m > 0:
                ml_max_m = (alt_likelihoods_by_m.argmax()) + 1
            else:
                ml_max_m = 0

            alt_likelihoods_by_e.append([likelihood_best_m, ml_max_m, e])

        alt_likelihoods_by_e = np.array(alt_likelihoods_by_e)

        likelihood_real = max(alt_likelihoods_by_e[:, 0])

        out_index = np.flatnonzero(alt_likelihoods_by_e[:, 0] == likelihood_real)

        out_intermediate = alt_likelihoods_by_e[out_index]

        if out_intermediate.shape[0] > 1:
            constarg = min(out_intermediate[:, 1])

            outcons = np.flatnonzero(out_intermediate[:, 1] == constarg)

            out_cons_intermediate = out_intermediate[outcons]

            if out_cons_intermediate.shape[0] > 1:
                out_cons_intermediate = out_cons_intermediate[0]

            out_intermediate = out_cons_intermediate

        outshape = out_intermediate.shape

        if len(outshape) != 1:
            out_intermediate = out_intermediate[0]

        out_intermediate = np.concatenate(
            [out_intermediate, np.array([K_neutral[-1], sweep_mode, w]), K_iter]
        )

        output.append(out_intermediate)

    # output = np.array(output)
    # return output[output[:, 0].argmax(), :]

    K_names = ["Kcounts_" + str(i) for i in range(1, K_iter.size + 1)]
    output = pd.DataFrame(output)
    output.insert(output.shape[1], "iter", i)

    output.columns = (
        [
            "t_statistic",
            "m",
            "frequency",
            "e",
            "model",
            "window_lassi",
        ]
        + K_names
        + ["iter"]
    )
    return output


def neutral_hfs(sims, K_truncation, w_size, step, nthreads=1):
    pars = [(i[0], i[1]) for i in sims]

    # Use joblib to parallelize the execution
    hfs_stats = Parallel(n_jobs=nthreads, verbose=5)(
        delayed(LASSI_spectrum_and_Kspectrum)(ts, rec_map, K_truncation, w_size, step)
        for index, (ts, rec_map) in enumerate(pars, 1)
    )

    K_counts, K_spectrum, windows = zip(*hfs_stats)

    return neut_average(np.vstack(K_spectrum))

    # t_m = Parallel(n_jobs=nthreads, verbose=5)(
    #     delayed(T_m_statistic)(kc, K_neutral, windows[index], K_truncation)
    #     for index, (kc) in enumerate(K_counts)
    # )
    # return (
    #     pd.DataFrame(t_m, columns=["t", "m", "frequency", "e", "model", "window"]),
    #     K_neutral,
    # )


def compute_t_m(
    sims,
    K_truncation,
    w_size,
    step,
    K_neutral=None,
    windows=[50000, 100000, 200000, 500000, 1000000],
    center=[5e5, 7e5],
    nthreads=1,
):
    pars = [(i[0], i[1]) for i in sims]

    # Log the start of the scheduling

    # Use joblib to parallelize the execution
    hfs_stats = Parallel(n_jobs=nthreads, verbose=5)(
        delayed(LASSI_spectrum_and_Kspectrum)(ts, rec_map, K_truncation, w_size, step)
        for index, (ts, rec_map) in enumerate(pars, 1)
    )

    K_counts, K_spectrum, windows_lassi = zip(*hfs_stats)

    if K_neutral is None:
        K_neutral = neut_average(np.vstack(K_spectrum))

    t_m = Parallel(n_jobs=nthreads, verbose=5)(
        delayed(T_m_statistic)(
            kc, K_neutral, windows_lassi[index - 1], K_truncation, i=index
        )
        for index, (kc) in enumerate(K_counts, 1)
    )
    t_m_cut = Parallel(n_jobs=nthreads, verbose=0)(
        delayed(cut_t_m_argmax)(t, windows=windows, center=center) for t in t_m
    )

    return pd.concat(t_m_cut)


def cut_t_m(df_t_m, windows=[50000, 100000, 200000, 500000, 1000000], center=6e5):
    out = []
    for w in windows:
        # for w in [1000000]:
        lower = center - w / 2
        upper = center + w / 2

        df_t_m_subset = df_t_m[
            (df_t_m.iloc[:, 5] > lower) & (df_t_m.iloc[:, 5] < upper)
        ]
        try:
            # max_t = df_t_m_subset.iloc[:, 0].argmax()
            max_t = df_t_m_subset.iloc[:, 1].argmin()
            # df_t_m_subset = df_t_m_subset.iloc[max_t:max_t+1, [0,1,-1]]
            # df_t_m_subset.insert(0,'window',w*2)
            m = df_t_m_subset.m.mode()

            if m.size > 1:
                m = df_t_m_subset.iloc[max_t : max_t + 1, 1]

            out.append(
                pd.DataFrame(
                    {
                        "iter": df_t_m_subset["iter"].unique(),
                        "window": w,
                        "t_statistic": df_t_m_subset.t.mean(),
                        "m": m,
                    }
                )
            )
        except:
            out.append(
                pd.DataFrame(
                    {
                        "iter": df_t_m["iter"].unique(),
                        "window": w,
                        "t_statistic": 0,
                        "m": 0,
                    }
                )
            )

    out = pd.concat(out).reset_index(drop=True)

    return out


def cut_t_m_argmax(
    df_t_m,
    windows=[50000, 100000, 200000, 500000, 1000000],
    center=[5e5, 7e5],
    step=1e4,
):
    out = []
    centers = np.arange(center[0], center[1] + step, step).astype(int)
    iter_c_w = list(product(centers, windows))
    for c, w in iter_c_w:
        # for w in [1000000]:
        lower = c - w / 2
        upper = c + w / 2

        df_t_m_subset = df_t_m[
            (df_t_m.iloc[:, 5] > lower) & (df_t_m.iloc[:, 5] < upper)
        ]
        try:
            max_t = df_t_m_subset.iloc[:, 0].argmax()

            # df_t_m_subset = df_t_m_subset[df_t_m_subset.m > 0]
            # max_t = df_t_m_subset[df_t_m_subset.m > 0].m.argmin()
            df_t_m_subset = df_t_m_subset.iloc[max_t : max_t + 1, :]

            df_t_m_subset = df_t_m_subset.loc[
                :,
                ~df_t_m_subset.columns.isin(
                    ["iter", "frequency", "e", "model", "window_lassi"]
                ),
            ]
            df_t_m_subset.insert(0, "window", w)
            df_t_m_subset.insert(0, "center", c)
            df_t_m_subset.insert(0, "iter", df_t_m.iter.unique())

            out.append(df_t_m_subset)

        except:
            K_names = pd.DataFrame(
                {
                    k: 0
                    for k in df_t_m.columns[
                        df_t_m.columns.str.contains("Kcount")
                    ].values
                },
                index=[0],
            )

            out.append(
                pd.concat(
                    [
                        pd.DataFrame(
                            {
                                "iter": df_t_m["iter"].unique(),
                                "center": c,
                                "window": w,
                                "t_statistic": 0,
                                "m": 0,
                            }
                        ),
                        K_names,
                    ],
                    axis=1,
                )
            )

    out = pd.concat(out).reset_index(drop=True)

    return out


def ms_parser(ms_file, param=None, seq_len=1.2e6):
    """Read a ms file and output the positions and the genotypes.
    Genotypes are a numpy array of 0s and 1s with shape (num_segsites, num_samples).
    """

    assert (
        ms_file.endswith(".out")
        or ms_file.endswith(".out.gz")
        or ms_file.endswith(".ms")
        or ms_file.endswith(".ms.gz")
    )

    open_function = gzip.open if ms_file.endswith(".gz") else open

    with open_function(ms_file, "rt") as file:
        file_content = file.read()

    # Step 2: Split by pattern (e.g., `---`)
    pattern = r"//"
    partitions = re.split(pattern, file_content)

    positions = []
    haps = []
    rec_map = []
    for r in partitions[1:]:
        # Read in number of segregating sites and positions
        data = []
        for line in r.splitlines()[1:]:
            if line == "":
                continue
            # if "discoal" in line or "msout" in line:
            # seq_len = int(line.strip().split()[3])
            if line.startswith("segsites"):
                num_segsites = int(line.strip().split()[1])
                if num_segsites == 0:
                    continue
                    #     # Shape of data array for 0 segregating sites should be (0, 1)
                    # return np.array([]), np.array([], ndmin=2, dtype=np.uint8).T
            elif line.startswith("positions"):
                tmp_pos = np.array([float(x) for x in line.strip().split()[1:]])
                tmp_pos = np.round(tmp_pos * seq_len).astype(int)

                # Find duplicates in the array
                duplicates = np.diff(tmp_pos) == 0

                # While there are any duplicates, increment them by 1
                for i in np.where(duplicates)[0]:
                    tmp_pos[i + 1] += 1
                tmp_pos += 1
                positions.append(tmp_pos)
                tmp_map = np.column_stack(
                    [
                        np.repeat(1, tmp_pos.size),
                        np.arange(tmp_pos.size),
                        tmp_pos,
                        tmp_pos,
                    ]
                )
                rec_map.append(tmp_map)

            else:
                # Now read in the data
                data.append(np.array(list(line), dtype=np.int8))
        data = np.vstack(data).T
        haps.append(data)

    if param is None:
        param = np.zeros(4)

    return (haps[0], rec_map[0], param)
