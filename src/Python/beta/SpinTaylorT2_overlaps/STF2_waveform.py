#===============================================================================
# Generate SpinTaylorF2 waveform with sidebands.
# Soham M  9/2016
# TODO: Add support for generating SpinTaylorT2
#===============================================================================

import numpy as np
import pycbc
from pycbc.types import TimeSeries, FrequencySeries, zeros
from pycbc.waveform import get_fd_waveform, get_td_waveform
from pycbc.waveform import td_approximants, fd_approximants
from lal import MTSUN_SI
import STF2_to_lal_coords as coords

def generate_template(**options):

    incl, psi0, spin1 = coords.to_lal_coords(options['M1'], options['M2'], \
                        options['CHI1'], options['KAPPA'], options['THETAJ'], \
                        options['PSIJ'], options['ALPHA0'], options['F_INJ'])

    # FIXME: Number of samples of the waveform.
    nsamples  = int((options['F_MAX'])/options['DEL_F']) + 1

    hpluss, hcross = get_fd_waveform(

        approximant = options['APPROX'], #Input

        mass1 = options['M1'], #Input
        mass2 = options['M2'], #Input

        delta_f = options['DEL_F'],    #Input
        f_lower = options['F_MIN'],    #Input
        f_final = options['F_MAX'],    #Input, can be turned off.

        distance    = 400.0,              #Default
        inclination = incl,               #to_lal_coords
        coa_phase   = options['PHI0'],    #Input

        spin1x = spin1[0],    #to_lal_coords
        spin1y = spin1[1],    #to_lal_coords
        spin1z = spin1[2],    #to_lal_coords
        spin2x = 0.0,         #Default
        spin2y = 0.0,         #Default
        spin2z = 0.0,         #Default

        phase_order     = 7,   #Default
        spin_order      = 6,   #Default
        amplitude_order = 0,   #Default

        sideband = options['BAND']   #Input
        )

    sin2Y, cos2Y = np.sin(2.*psi0), np.cos(2.*psi0)

    hp   = pycbc.DYN_RANGE_FAC*hpluss
    hc   = pycbc.DYN_RANGE_FAC*hcross

    waveform =  hp*cos2Y + hc*sin2Y
    waveform.resize(nsamples)

    return waveform

#TODO: Get the sizes of equal length.

def generate_STT2_template(**options):

    incl, psi0, spin1 = coords.to_lal_coords(options['M1'], options['M2'], \
                        options['CHI1'], options['KAPPA'], options['THETAJ'], \
                        options['PSIJ'], options['ALPHA0'], options['F_INJ'])

    # FIXME: Number of samples of the waveform.
    nsamples  = int((options['F_MAX'])/options['DEL_F']) + 1
    DEL_T = 1./((2*nsamples-1)*options['DEL_F'])

    hpluss, hcross = get_td_waveform(

        approximant = options['APPROX'], #Input

        mass1 = options['M1'], #Input
        mass2 = options['M2'], #Input

        delta_t = DEL_T,    #Compute
        f_lower = options['F_MIN'],    #Input
        f_final = options['F_MAX'],    #Input, can be turned off.

        distance    = 400.0,              #Default
        inclination = incl,               #to_lal_coords
        coa_phase   = options['PHI0'],    #Input

        spin1x = spin1[0],    #to_lal_coords
        spin1y = spin1[1],    #to_lal_coords
        spin1z = spin1[2],    #to_lal_coords
        spin2x = 0.0,         #Default
        spin2y = 0.0,         #Default
        spin2z = 0.0,         #Default

        phase_order     = 7,   #Default
        spin_order      = 6,   #Default
        amplitude_order = 0,   #Default
        )

    sin2Y, cos2Y = np.sin(2.*psi0), np.cos(2.*psi0)

    #Converting to frequency domain here.
    hpluss = hpluss.to_frequencyseries(options['DEL_F'])
    hcross = hcross.to_frequencyseries(options['DEL_F'])

    hp   = pycbc.DYN_RANGE_FAC*hpluss
    hc   = pycbc.DYN_RANGE_FAC*hcross

    waveform =  hp*cos2Y + hc*sin2Y
    waveform.resize(nsamples)

    return waveform
