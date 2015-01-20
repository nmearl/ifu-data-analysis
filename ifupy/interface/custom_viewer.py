from glue import custom_viewer
from glue.core.subset import RoiSubsetState

from matplotlib.colors import LogNorm
from matplotlib.patches import Circle, Rectangle, Arc
from matplotlib.lines import Line2D
import numpy as np
import sys

sys.path.append('/Users/nearl/projects/ifupy/ifupy')
from arithmetic import collapse_slice
from arithmetic import extract_spectrum

collapse = custom_viewer('Collapse Plot',
                         sci='att',
                         # frame=(0, 2039),
                         method=['sum', 'mean', 'median']
                         # dq='att(dq)'
)


@collapse.plot_data
def collapse_show_data(axes, sci, method):
    if len(sci) > 0:
        vmin = np.log10(np.min(sci))
        vmax = np.log10(np.max(sci))
        axes.imshow(collapse_slice(sci, method=method),
                    interpolation='nearest',
                    norm=LogNorm())


@collapse.select
def collapse_select(roi, x, y):
    return roi.contains(x, y)


extract = custom_viewer('Extract Plot',
                        sci='att',
                        x_pos=(0, 82),
                        y_pos=(0, 82),
)


@extract.plot_data
def extract_show_data(axes, sci, x_pos, y_pos):
    if len(sci) > 0:
        extspec = extract_spectrum(sci, [[x_pos, y_pos]], [1.0, 1.0, 1.0])
        axes.plot(extspec[0, :], extspec[2, :])


@extract.select
def extract_select(roi, x, y):
    return roi.contains(x, y)


line_measure = custom_viewer('Line Measure Plot',
                             sci='att',
)

# @line_measure.plot_data
# def line_measure_show_data(axes, sci):
# if len(sci) > 0:
# test_spec = extract_spectrum(sci, [[40,40]], [1.0, 1.0, 1.0])
#         line = line_measure(test_spec[0, :], test_spec[2, :])
#
#         inWave, inSpectrum = line[0, :], line[2, :]
#
#         axes.plot(inWave, inSpectrum, color='green', lw=2., label = 'Spectrum')
#
#         # Plot gaussian fit
#         axes.plot(inWave, g(inWave), color='red', lw=1., label='Gauss Fit')
#         xl = g.mean.value
#         yl = axes.get_ylim()
#         axes.plot([xl, xl], yl, color='black', lw=1.5, ls='--', label='Line '
#                                                                      'Location')
#         print('Limits: ', g.mean.value, yl)
#
#         axes.set_xlim(inWave[0], inWave[-1])
#         axes.set_xlabel('Wavelength ($\mu m$)')
#         axes.set_ylabel('Counts (D/n)')
#
#         # Now add the legend with some customizations.
#         axes.legend(loc='best', numpoints = 1, shadow=True)
#
# @line_measure.select
# def line_measure_select(roi, x, y):
#     return roi.contains(x, y)