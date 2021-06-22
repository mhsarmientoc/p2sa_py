#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Maria H. Sarmiento
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 6 Aug. 2019
"""
import pytest
import os

# from astroquery.utils.tap.conn.tests.DummyConnHandler import DummyConnHandler

from esa_p2sa.p2sa_core import ESAP2SAClass
from esa_p2sa.tests.dummy_handler import DummyP2SAHandler

from esa_p2sa.tests.dummy_tap_handler import DummyTapHandler
from astroquery.utils.tap.xmlparser import utils
from astroquery.utils.tap.conn.tests.DummyResponse import DummyResponse

from astroquery.utils.tap import TapPlus


def data_path(filename):
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    return os.path.join(data_dir, filename)


def get_dummy_tap_handler():
    parameters = {'query': "select top 10 * from p2sa.v_observation",
                  'output_file': "test_query_p2sa_tap.vot",
                  'output_format': "votable",
                  'verbose': False}
    dummy_tap_handler = DummyTapHandler("launch_job", parameters)
    return dummy_tap_handler


class TestESAP2SA:

    def test_query_p2sa_observations_1Instrument(self):
        instrument_list = ["SWAP"]
        parameters = {'input_instruments': instrument_list,
                      'input_to_date': "2015-08-06 00:00:00",
                      'input_from_date': "2015-08-04 00:00:00",
                      'output_format': "votable",
                      'filename': 'output',
                      'verbose': False}
        connHandler = DummyTapHandler()
        p2sa = ESAP2SAClass(connHandler)
        p2sa.query_p2sa_observations(instruments=parameters['input_instruments'],
                                     from_date=parameters['input_from_date'],
                                     to_date=parameters['input_to_date'],
                                     output_format=parameters['output_format'],
                                     filename=parameters['filename'],
                                     verbose=parameters['verbose'])

    def test_query_p2sa_observations_1Instrument1Date(self):
        instrument_list = ["SWAP", "LYRA"]
        parameters = {'input_instruments': instrument_list,
                      'input_to_date': "",
                      'input_from_date': "2015-08-04 00:00:00",
                      'output_format': "votable",
                      'filename': 'output',
                      'verbose': False}
        connHandler = DummyTapHandler()
        p2sa = ESAP2SAClass(connHandler)
        p2sa.query_p2sa_observations(instruments=parameters['input_instruments'],
                                     from_date=parameters['input_from_date'],
                                     to_date=parameters['input_to_date'],
                                     output_format=parameters['output_format'],
                                     filename=parameters['filename'],
                                     verbose=parameters['verbose'])

    def test_query_p2sa_observations(self):
        instrument_list = ["SWAP", "LYRA"]
        parameters = {'input_instruments': instrument_list,
                      'input_to_date': "2015-08-06 00:00:00",
                      'input_from_date': "2015-08-04 00:00:00",
                      'output_format': "votable",
                      'filename': 'output',
                      'verbose': False}
        connHandler = DummyTapHandler()
        p2sa = ESAP2SAClass(connHandler)
        p2sa.query_p2sa_observations(instruments=parameters['input_instruments'],
                                     from_date=parameters['input_from_date'],
                                     to_date=parameters['input_to_date'],
                                     output_format=parameters['output_format'],
                                     filename=parameters['filename'],
                                     verbose=parameters['verbose'])

    def test_download_p2sa_product(self):
        file_oid_list = ["6605", "6606"]

        parameters = {'file_oid_list': file_oid_list,
                      'data_retrieval_origin': 'P2SAPY',
                      'retrieval_type': "PRODUCT",
                      'filename': 'output',
                      'verbose': False}

        connHandler = DummyTapHandler()
        p2sa = ESAP2SAClass(connHandler)
        p2sa.get_p2sa_product(file_oid_list=parameters['file_oid_list'],
                              data_retrieval_origin=parameters['data_retrieval_origin'],
                              filename=parameters['filename'],
                              retrieval_type=parameters['retrieval_type'],
                              verbose=parameters['verbose'])

    def test_get_p2sa_postcard(self):
        parameters = {'input_observation_oid': "198028195",
                      'input_resolution': "low",
                      'input_data_retrieval_origin': "P2SAPY",
                      'input_retrieval_type': "PRODUCT",
                      'input_product_type': "POSTCARD",
                      'filename': 'output',
                      'verbose': False}
        connHandler = DummyTapHandler()
        p2sa = ESAP2SAClass(connHandler)

        p2sa.get_p2sa_postcard(observation_oid=parameters['input_observation_oid'],
                               resolution=parameters['input_resolution'],
                               data_retrieval_origin=parameters['input_data_retrieval_origin'],
                               filename=parameters['filename'],
                               retrival_type=parameters['input_retrieval_type'],
                               product_type=parameters['input_product_type'],
                               verbose=parameters['verbose'])

    def test_query_p2sa_observations_no_instrument_2dates(self):
        instrument_list = []

        parameters = {'input_instruments': instrument_list,
                      'input_to_date': "2015-08-06 00:00:00",
                      'input_from_date': "2015-08-04 00:00:00",
                      'output_format': "votable",
                      'filename': 'output',
                      'verbose': False}

        responseLoadTable = DummyResponse()
        responseLoadTable.set_status_code(200)
        responseLoadTable.set_message("OK")
        tableDataFile = data_path('test_p2sa_obs_by_dates.vot')
        tableData = utils.read_file_content(tableDataFile)
        responseLoadTable.set_data(method='GET',
                                   context=None,
                                   body=tableData,
                                   headers=None)

        request = "sync?FORMAT=votable&LANG=ADQL&PHASE=RUN&QUERY=SELECT++TOP+2000+obs.observation_oid%2C+obs" \
                  ".instrument_name%2C+obs.observation_type%2C+obs.begin_date%2C+obs.end_date%2C+obs.processing_level" \
                  "%2C+obs.science_objective%2C+obs.wavelength_range%2C+obs.science_object_name%2C+obs.file_name%2C" \
                  "+obs.file_format%2C+obs.file_size%2C+obs.observatory_name%2C+obs.calibrated+FROM+p2sa" \
                  ".v_observation+as+obs++WHERE+%28obs.end_date+%3E+%272015-08-04+00%3A00%3A00%27%29+AND+%28obs" \
                  ".begin_date+%3C+%272015-08-06+00%3A00%3A00%27%29+ORDER+BY+obs.begin_date+ASC&REQUEST=doQuery" \
                  "&tapclient=aqtappy-1.2.1"

        connHandler = DummyTapHandler()

        connHandler.set_response(request, responseLoadTable)

        p2sa = ESAP2SAClass(connHandler)

        results_table = p2sa.query_p2sa_observations(instruments=parameters['input_instruments'],
                                                     from_date=parameters['input_from_date'],
                                                     to_date=parameters['input_to_date'],
                                                     output_format=parameters['output_format'],
                                                     filename=parameters['filename'],
                                                     verbose=parameters['verbose'])
        print(results_table)

    def test_query_p2sa_tap(self):
        parameters = {'query': "select top 10 * from p2sa.v_observation",
                      # 'output_file': "test_query_p2sa_tap.vot",
                      'output_format': "votable",
                      'verbose': False}

        responseLoadTable = DummyResponse()
        responseLoadTable.set_status_code(200)
        responseLoadTable.set_message("OK")
        tableDataFile = data_path('test_basic_p2sa_obs.vot')
        tableData = utils.read_file_content(tableDataFile)
        responseLoadTable.set_data(method='POST',
                                   context=None,
                                   body=tableData,
                                   headers=None)

        connHandler = DummyTapHandler()

        tableRequest = 'sync?FORMAT=votable&LANG=ADQL&PHASE=RUN&QUERY=select+top+10+%2A+from+p2sa.v_observation' \
                       '&REQUEST=doQuery&tapclient=aqtappy-1.2.1'
        connHandler.set_response(tableRequest, responseLoadTable)

        p2sa = ESAP2SAClass(connHandler)

        result_table = p2sa.query_p2sa_tap(query=parameters['query'],
                                           # output_file=parameters['output_file'],
                                           output_format=parameters['output_format'],
                                           verbose=parameters['verbose'])

        if result_table is None:
            raise ValueError('No results found')

        rows = len(result_table)
        cols = result_table.colnames

        if rows != 10:
            raise ValueError('Expected 10 rows, found: %s' % rows)

        if len(cols) != 16:
            raise ValueError('Expected 16 columns, found: %s' % (len(cols)))

        # get_dummy_tap_handler().check_call("launch_job", parameters)
        # connHandler.check_call("execute_post", parameters)

    def test_get_tables(self):
        parameters = {'query': "select top 10 * from p2sa.v_observation",
                      'output_file': "test_get_tables.vot",
                      'output_format': "votable_plain",
                      'verbose': False}

        parameters2 = {'only_names': True,
                       'verbose': True}

        responseLoadTable = DummyResponse()
        responseLoadTable.set_status_code(200)
        responseLoadTable.set_message("OK")
        tableDataFile = data_path('test_tables.xml')
        tableData = utils.read_file_content(tableDataFile)
        responseLoadTable.set_data(method='GET',
                                   context=None,
                                   body=tableData,
                                   headers=None)

        connHandler = DummyTapHandler()

        tableRequest = "tables?only_tables=true"
        connHandler.set_response(tableRequest, responseLoadTable)

        p2sa = ESAP2SAClass(connHandler)

        p2sa.get_p2sa_tables(True, True)

    def test_get_columns(self):
        parameters = {'query': "select top 10 * from p2sa.v_observation",
                      'output_file': "test_get_Columns.vot",
                      "output_format": "votable_plain",
                      'verbose': False}

        parameters2 = {'table_name': "table",
                       'only_names': True,
                       'verbose': True}

        responseLoadTable = DummyResponse()
        responseLoadTable.set_status_code(200)
        responseLoadTable.set_message("OK")
        tableDataFile = data_path('test_tables.xml')
        tableData = utils.read_file_content(tableDataFile)
        responseLoadTable.set_data(method='GET',
                                   context=None,
                                   body=tableData,
                                   headers=None)

        connHandler = DummyTapHandler()

        # Add response for: tables
        tableRequest = "tables"
        connHandler.set_response(tableRequest, responseLoadTable)

        p2sa = ESAP2SAClass(connHandler)
        p2sa.get_p2sa_columns("table", True, True)


if __name__ == "__main__":
    pytest.main()

# Tests #
test = TestESAP2SA()
