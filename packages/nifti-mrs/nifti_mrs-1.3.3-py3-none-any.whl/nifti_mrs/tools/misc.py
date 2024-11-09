""" Miscellaneous tools for NIfTI-MRS

    Author: Will Clarke <william.clarke@ndcn.ox.ac.uk>
    Copyright (C) 2021 University of Oxford
"""

import numpy as np

from nifti_mrs.nifti_mrs import NIFTI_MRS


def conjugate(nmrs):
    """Conjugate a nifti-mrs object.

    :param nmrs: NIFTI_MRS object to conjugate
    :type nmrs: NIFTI_MRS
    :return: Conjugated NIFTI_MRS
    :rtype: NIFTI_MRS
    """

    return NIFTI_MRS(np.conjugate(nmrs[:]), header=nmrs.header)
