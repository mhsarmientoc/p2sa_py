#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from astroquery.utils.tap.model import modelutils, taptable
from requests.models import Response

__all__ = ['DummyP2SAHandler']


class DummyResponse(object):
    def __init__(self):
        self.message = None
        self.status = 200
        self.reason = "OK"

    def raise_for_status(self):
        return self.message


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_dir, filename)


def get_file(filename, response=None, verbose=False):
    return None


def request(t="GET", link=None, params=None,
            cache=None,
            timeout=None):
    return None


def get_table(filename=None, response=None, output_format='votable_plain',
              verbose=False):
    return None


class DummyP2SAHandler(object):

    def __init__(self, method, parameters):
        self._invokedMethod = method
        self._parameters = parameters
        self.response = DummyResponse()
        self.encodedLink = "http://p2sa.esac.esa.int/p2sa-sl-tap/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=votable&" \
                           "PHASE=RUN&QUERY=SELECT%20obs.observation_oid,%20obs.instrument_name," \
                           "%20obs.observation_type,%20obs.begin_date,%20obs.end_date,%20obs.processing_level," \
                           "%20obs.science_objective,%20obs.wavelength_range,%20obs.science_object_name," \
                           "%20obs.file_name,%20obs.file_format,%20obs.file_size,%20obs.observatory_name," \
                           "%20obs.calibrated%20FROM%20p2sa.v_observation%20as%20obs%20" \
                           "%20WHERE%20%20((instrument_name=%27SWAP%27))" \
                           "%20AND%20(obs.end_date%20%3E%20%272018-07-01%2000:00:00%27)" \
                           "%20ORDER%20BY%20obs.begin_date%20ASC "

    def execute_tapget(self, link, verbose):
        return self.response

    def HTTPError(self, error_reason):
        return self.response

    def check_launch_response_status(self, response, verbose, status, validate):
        return self.response

    def execute_tappost(self, subcontext, data, verbose):
        return self.response

    def _TapConn__execute_get(self, link=None):
        return self.response

    def url_encode(self, link=None):
        return self.encodedLink

    def reset(self):
        self._parameters = {}
        self._invokedMethod = None

    def check_call(self, method_name, parameters):
        self.check_method(method_name)
        self.check_parameters(parameters, method_name)

    def check_method(self, method):
        if method == self._invokedMethod:
            return
        else:
            raise ValueError("".join(("Method '",
                                      str(method),
                                      "' not invoked. (Invoked method is '",
                                      str(self._invokedMethod) + "')")))

    def check_parameters(self, parameters, method_name):
        if parameters is None:
            return len(self._parameters) == 0
        if len(parameters) != len(self._parameters):
            raise ValueError("Wrong number of parameters for method '%s'. Found: %d. Expected %d", (method_name,
                                                                                                    len(
                                                                                                        self._parameters),
                                                                                                    len(parameters)))
        for key in parameters:
            if key in self._parameters:
                # check value
                if self._parameters[key] != parameters[key]:
                    raise ValueError("".join(("Wrong '%s' parameter ",
                                              "value for method '%s'. ",
                                              "Found:'%s'. Expected:'%s'",
                                              (method_name,
                                               key,
                                               self._parameters[key],
                                               parameters[key]))))
                else:
                    raise ValueError("Parameter '%s' not found in method '%s'" %
                                     (str(key), method_name))
        return False
