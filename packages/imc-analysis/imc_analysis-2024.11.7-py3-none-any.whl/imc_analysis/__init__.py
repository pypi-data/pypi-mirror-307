from . import pl
from . import tl
from . import utils

from .pl import celltype_heatmap, plot_mwu, umap_var
from .tl import celltype_density, patient_density, compute_mean, grouped_mwu_test
from .utils import parse_yaml

import scanpy as sc
import matplotlib as mpl

sc.settings.set_figure_params(dpi=200, dpi_save=300, fontsize=12)
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["axes.grid"] = False