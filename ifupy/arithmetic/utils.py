# Global imports
import numpy as np

def frame_convert(frame, cals):
    """ 
    Convert the frame to a wavelength using a starting value and 
    delta (in microns).
    
    Parameters
    ----------
    frame : int
        Datacube frame to convert to a wavelength.
    
    cals : list of floats
           Calibration values for the input datacube; 
           (crpix, crval, crdelt).
        
    Returns
    -------
    wavelength : float
        The converted wavelength of the datacube frame.
        
    Raises
    ------
    Not yet implemented.
    """
    
    # Calculate the frame conversion
    wavelength = (frame - cals[0]) * cals[2] + cals[1]
    
    return wavelength

def wave_convert(wavelength, cals):
    """
    Convert the wavelength to a frame using a starting value and 
    delta (in microns).
    
    Parameters
    ----------
    wavelength : float
        The wavelength to convert to a datacube frame.
    
    cals : list of floats
           Calibration values for the input datacube; 
           (crpix, crval, crdelt).
        
    Returns
    -------
    frame : int
        Datacube frame to converted from the input wavelength.
        
    Raises
    ------
    Not yet implemented.
    """
    
    from numpy import round
    from numpy import int

    # Calculate the wavelength conversion
    frame = cals[0] + ((wavelength - cals[1]) / cals[2])
    
    frame = np.int(np.round(frame))
    return frame