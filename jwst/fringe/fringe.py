#
#  Module for applying fringe correction
#

import numpy as np
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def do_correction(input_model, fringe_model):
    """
    Short Summary
    -------------
    Fringe-correct a JWST data model using a fringe model

    Parameters
    ----------
    input_model: JWST data model
        input science data model to be fringe-corrected

    fringe_model: JWST data model
        data model containing fringe

    Returns
    -------
    output_model: JWST data model
        fringe-corrected science data model

    """
    output_model = apply_fringe(input_model, fringe_model)
    output_model.meta.cal_step.fringe = 'COMPLETE'

    return output_model


def apply_fringe(input_model, fringe):
    """
    Short Summary
    -------------
    Fringe Correction: fringe-corrects data and error arrays by dividing these
    arrays by the respective values in the reference array (for the reference
    pixels having good values), and updates the data quality array based on
    bad pixels in the reference array.

    Parameters
    ----------
    input_model: JWST data model
        input science data model to be fringe-corrected

    fringe: JWST data model
         ImageModel of fringe

    Returns
    -------
    output_model: JWST data model
        input science data model which has been fringe-corrected
    """

    # Initialize the output model as a copy of the input
    output_model = input_model.copy()

    fringe_data = fringe.data
    # fringe_dq = fringe.dq

    # Fringe-correct data and error arrays, applying correction only
    #    to pixels having good reference values
    good_pix = np.isfinite(fringe_data)
    output_model.data[good_pix] /= fringe_data[good_pix]
    output_model.err[good_pix] /= fringe_data[good_pix]

### 05/22/14: For now, commenting out the following updating of the output
###    DQ based on the DQ of the reference file. This is done now because the
###    current DQ values in the ref file do not correspond to 'bad' data
###    values in the SCI array of the ref file.  Accordingly, this information
###    will be logged for now. This behavior may be changed later.
###
    # set DQ flag for bad pixels in the fringe
#       dq_mask = fringe_dq * 0
#       dq_mask[np.where(fringe_dq != 0)] = dqflags.pixel['DEAD']

    # update DQ array based on fringe's DQ values
#       output_model.dq = np.bitwise_or(output_model.dq, dq_mask)
    log.info('The DQ values in the reference file will NOT be used to update the\
    DQ values in the output DQ array.')

    return output_model
