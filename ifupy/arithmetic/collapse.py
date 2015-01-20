# Import necessary modules
from __future__ import print_function
import numpy as np


def _arrayCollapse(array_in, method):
    """
    Collapse a slice of a datacube, with a given mode, along the wavelength (z) slice.
    
    This is an internal function that will handle the actual cube
    collapse with a given method, for numpy.array types. 
    Specifically for computed collapse without sigma clipping.
    
    Parameters
    ----------
    array_in : numpy.ndarray
               Input array over which to calculate the collapse.
    
    method : string
             Passed from the main function call.
             
    Returns
    -------
    collapsed_array : numpy.ndarray
                      The collapsed array with the desired method.
    """

    # Perform an numpy.array collapse along the z-axis
    if method == 'sum':
        print('(3d_collapse): Sum collapse of extracted slices ...')
        collapsed_array = np.sum(array_in, axis=0)

    elif method == 'mean':
        print('(3d_collapse): Mean collapse of extracted slices ...')
        collapsed_array = np.mean(array_in, axis=0)

    elif method == 'median':
        print('(3d_collapse): Median collapse of extracted slices ...')
        collapsed_array = np.median(array_in, axis=0)

    # Returns an array of type numpy.array    
    return collapsed_array


def _maskedCollapse(array_in, method):
    """
    Collapse a slice of a datacube, with a given mode, along the 
    wavelength (z) slice.
    
    This is an internal function that will handle the actual cube
    collapse with a given method, for numpy.ma (MaskedArray) types. 
    Specifically for computed collapse with sigma clipping.

    Parameters
    ----------
    array_in : numpy array
               Input array over which to calculate the collapse.
    
    method : string
             Passed from the main function call.
             
    Returns
    -------
    collapsed_array.data : numpy array
                           The collapsed array with the desired method.
    """
    import numpy.ma as ma

    # Perform an numpy.ma array collapse along the z-axis
    if method == 'sum':
        print('(3d_collapse): Masked sum collapse of extracted slices ...')
        collapsed_array = ma.sum(array_in, axis=0)

    elif method == 'mean':
        print('(3d_collapse): Masked mean of extracted slices:')
        collapsed_array = ma.mean(array_in, axis=0)

    elif method == 'median':
        print('(3d_collapse): Masked median of extracted slices:')
        collapsed_array = ma.extras.median(array_in, axis=0)

    # Returns an array of type numpy.array    
    return collapsed_array.data


def collapse_slice(array_in, region=None, method='sum', sigma=False):
    """
    Collapse a slice of a datacube, with a given mode, along the 
    wavelength slice.
    
    This function handles both numpy.array (with no sigma clipping) 
    and numpy.ma masked arrays (with sigma clipping, from astropy.stast.funcs)
    
    Parameters
    ----------
    array_in : numpy.ndarray
               The input datacube array.
    region :  The region of the datacube to collapse, in the form of [a, b], 
              where a is the 1st slice boundary, and b is the 2nd + 1 slice boundary. 
              Can be omitted to collapse entire z-axis.
            
    method : {'median', 'sum', 'mean'}
             The method of collapse.
             
    sigma : bool, optional
            Flag for wether to perform sigma clipping or not (default is False).
                
    Returns
    -------
    collapsedArray : numpy.ndarray
                     Collapsed image.
    
    Example usage:
    
        1. >> result = ifu_3d_collapse(cube, region=[1000, 1999], method='median')
        
        Median collapse cube from z-axis frames 1000-2000.
        
        2. >> result = ifu_3d_collapsed(cube, method='mean', sigma=2.5)
        
        Mean collapse a cube along the entire z-axis, performing a sigma
        clipping of 2.5.
    """

    # Extract the desired slice...
    if not region:
        print('(3d_collapse): Entire z-axis will be collapsed!')
        slice_array = array_in
    else:
        print('(3d_collapse): z-axis collapse limits: ', region)
        slice_array = array_in[region[0]:region[1], :, :]

    # ... and perform the desired operation, based on input mode.
    collapsed_array = _arrayCollapse(slice_array, method=method)

    if sigma:
        # Import sigma_clip from astropy
        from astropy.stats.funcs import sigma_clip

        # Perform sigma clipping on input cube
        print('(3d_collapse): Clipping data ...')
        clipped = sigma_clip(slice_array, sigma, iters=None, axis=0, copy=True)


        # Compare the clipped sample to determine wether we need to 
        # recalculate the collapse        
        if np.array_equal(clipped.compressed(), slice_array.flatten()):
            print('Arrays are exactly the same, no clipping required.')
        else:
            # Now that we have the sigma mask, recalculate the collapse...            
            collapsed_array = _maskedCollapse(clipped, method)

    # Returns the collapsed array
    # print('(3d_collapse): Shape of returned array:', collapsed_array.shape)
    return collapsed_array


if __name__ == "__main__":
    collapse(array_in, region=None, method='sum', sigma=False)