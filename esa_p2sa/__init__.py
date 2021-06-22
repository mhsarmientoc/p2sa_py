"""
@author: Maria H. Sarmiento Carrion
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 6 Aug. 2018
"""

from astropy import config as _config


class Conf(_config.ConfigNamespace):
    """
    Configuration parameters for `esa_p2sa`.
    """

    DATA_URL = "http://p2sa.esac.esa.int/p2sa-sl-tap/data?"
    HOST_URL = "http://p2sa.esac.esa.int/"
    VIDEO_URL = "http://p2sa.esac.esa.int/p2sa-sl-tap/video?"
    METADATA_URL = "http://p2sa.esac.esa.int/p2sa-sl-tap/tap/sync?"
    TAP_CONTEXT = "p2sa-sl-tap"

    DATA_ACTION = _config.ConfigItem(DATA_URL,
                                     "Main url for retrieving p2sa files")
    METADATA_ACTION = _config.ConfigItem(METADATA_URL,
                                         "Main url for retrieving p2sa metadata")
    VIDEO_ACTION = _config.ConfigItem(VIDEO_URL,
                                      "Main url for retrieving p2sa movie files")
    P2SA_BASE_URL = _config.ConfigItem(HOST_URL,
                                       "Base url of P2SA TAP")
    SERVER_CONTEXT = _config.ConfigItem(TAP_CONTEXT,
                                       "Server context of P2SA TAP")
    TIMEOUT = 60


conf = Conf()

from .p2sa_core import ESAP2SA, ESAP2SAClass

__all__ = ['ESAP2SA', 'ESAP2SAClass', 'Conf', 'conf']
