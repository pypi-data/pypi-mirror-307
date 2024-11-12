# read version from installed package
from importlib.metadata import version
from pycount_caseexample.pycount_caseexample import count_words
from pycount_caseexample.plotting import plot_words
__version__ = version("pycount_caseexample")