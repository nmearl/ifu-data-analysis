# Global imports
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from astropy.modeling import models, fitting
from utils import frame_convert, wave_convert


def line_measure(x, y, f=None, region=None, continuum=None, display=False):
    """
    Measure the line (if present) in a given region of an 
    input spectrum.
    
    Parameters
    ----------
    x : array
        The wavelength array of the input spectrum (in $\mu$m)
        
    y : array
        The spectrum counts array
        
    f : array, optional
        The frame array that corresponts to the input 
        wavelength (default is None.)
                       
    region : list of ints, optional
             The region for which to measure the line.
             (default is None, in which the entire spectrum
             is used.)
             
    continnum : string
                Method for continuum subtraction. Available will
                be 'linear', 'poly2', and 'polyn' (defaults to 
                'linear').
             
    display : bool, optinal
              Display the line with diagnostic values.
              (default is False, diagnostic values displayed 
              to screen).
    
    Returns
    -------
    line : list of floats
           Line location (wavelength), FWHM, and intensity.
    
    """
    # Initialize the output spectrum
    # If zero, then something went wrong!
    line, inSpectrum = [], []
    
    index, = np.where((x >= region[0]) & (x <= region[1]))

    if region[0] >= x[0] and region[1] <= x[-1]:
        print('Indeces: ', index[0], index[-1])
        print('Wavelength range: ', x[index[0]], x[index[-1]])
        inWave = x[index[0]:index[-1]]
        inSpectrum = y[index[0]:index[-1]]
        
        # If a frame array is available, assign range as well
        if f != None: inFrame = f[index[0]:index[-1]]
        
    else:    
        print('Wavelength range is outside that available:')
        print('Input spectrum range: ', x[index[0]], x[index[-1]])
        return line

#    #if continuum == 'linear':
#    #
#    # If a continuum-subtracted spectrum is required, calculate
#    # and return...
#    if continuum:                
#        pTemp = np.polyfit(spec_wave, spectrum, 1)
#        
#        if spectrum.ndim == 1:
#            p = pTemp
#            continuum = p[0] * spec_wave + p[1]
#        else:
#            p = pTemp.T
#            continuum = np.zeros(spectrum.shape)
#            for rec, pfit in enumerate(p):
#                continuum[:, rec] = pfit[0] * spec_wave + pfit[1]
#
#        # Compute continuum-subtracted spectrum
#        spectrum = spectrum - continuum


    # Initial gaussian fit parameter guesses
    amp_0 = inSpectrum.max()
    index, = np.where(inSpectrum == amp_0)
    mean_0 = inWave[index[0]]

    # Fit the data using a Gaussian
    g_init = models.Gaussian1D(amplitude=0., mean=mean_0, stddev=3.)
    fit_g = fitting.LevMarLSQFitter()
    g = fit_g(g_init, inWave, inSpectrum)

    print(g)    
    
    # Display spectrum if set (DEBUG)
    if display:
        
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(inWave, inSpectrum, color='green', lw=2., label = 'Spectrum')
        
        
        # Plot gaussian fit
        ax.plot(inWave, g(inWave), color='red', lw=1., label='Gauss Fit')
        xl = g.mean.value
        yl = ax.get_ylim()
        ax.plot([xl, xl], yl, color='black', lw=1.5, ls='--', label='Line Location')
        print('Limits: ', g.mean.value, yl)
        
        ax.set_xlim(inWave[0], inWave[-1])
        ax.set_xlabel('Wavelength ($\mu m$)')
        ax.set_ylabel('Counts (D/n)')
        
        if f != None:
            ax_twin = ax.twiny()
            ax_twin.set_xlim(inFrame[0], inFrame[-1])
            ax_twin.set_xlabel('Datacube Frame')

        # Now add the legend with some customizations.
        ax.legend(loc='best', numpoints = 1, shadow=True)

    
    line = np.empty(2*len(inWave)).reshape(2, len(inWave))
    line[0, :] = inWave
    line[1, :] = inSpectrum
    return line


if __name__ == "__main__":
    line_measure(spectrum, region=[], display=False)