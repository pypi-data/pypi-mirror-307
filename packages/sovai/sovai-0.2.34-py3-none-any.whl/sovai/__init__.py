"""
Main SovAI SDK Tool Kit package
"""
from .api_config import read_key, save_key, ApiConfig
from .get_data import data
from .basic_auth import basic_auth
from .token_auth import token_auth
from .utils.file_management import save_or_update_tickers, save_or_update_codes


import warnings
warnings.filterwarnings("ignore")


__version__ = "0.1.25"

# Call the function to ensure tickers data is up-to-date
save_or_update_tickers()

save_or_update_codes()

try:
    from .get_plots import plot
    from .get_reports import report
    from .get_compute import compute
    from .studies.nowcasting import nowcast
    from .extensions.pandas_extensions import CustomDataFrame as extension
    from .get_tools import sec_search, sec_filing, code, sec_graph
    HAS_FULL_INSTALL = True
except ImportError as e:
    print(f"ImportError: {e}")
    HAS_FULL_INSTALL = False


__all__ = ['read_key', 'save_key', 'ApiConfig', 'data', 'basic_auth', 'token_auth']

if HAS_FULL_INSTALL:
    __all__ += ['plot', 'report', 'compute', 'nowcast', 'extension', 'sec_search', 'sec_filing', 'code', 'sec_graph']