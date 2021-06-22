# -*- coding: utf-8 -*-
"""
@author: Maria H. Sarmiento Carrión
@contact: mhsarmiento@sciops.esa.int
European Space Astronomy Centre (ESAC)
European Space Agency (ESA)
Created on 5 Aug. 2019
"""
import datetime
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Union

import dateutil
from astropy import log
from astroquery.utils.tap.core import TapPlus
from astroquery.utils.tap.model import modelutils

from . import conf

__all__ = ['ESAP2SA', 'ESAP2SAClass']


# -------------------------------
# CLASS ESAP2SAClass
# -------------------------------

class ESAP2SAClass(TapPlus):
    data_url = conf.DATA_ACTION
    metadata_url = conf.METADATA_ACTION
    video_url = conf.VIDEO_ACTION
    p2sa_url = conf.P2SA_BASE_URL
    server_context = conf.SERVER_CONTEXT

    TIMEOUT = conf.TIMEOUT

    def __init__(self, tap_plus_conn_handler=None):
        super(ESAP2SAClass, self).__init__(url=self.p2sa_url,
                                           server_context=self.server_context,
                                           tap_context="tap",
                                           data_context="data",
                                           connhandler=tap_plus_conn_handler)

    def get_p2sa_observation(self, **kwargs):

        """
        Example: http://p2sa.esac.esa.int/p2sa-sl-tap/data?retrieval_type=PRODUCT&observation_oid=197889204
        &product_type=OBSERVATION&data_retrieval_origin=P2SAPY
        
        Download observation products from P2SA
        
        Parameters
        ----------
        input_retrieval_type: string
        
            (Description TBD)
            
        input_obs_oid : string
         
            (Description TBD)
        
        input_product_type: string 
        
            (Description TBD)
            
        input_data_retrieval_origin: string
            (Description TBD)

        filename: string
            (Description TBD)
        
        verbose : bool
            optional, default 'False'
            flag to display information about the process

        Returns
        -------
        None. It downloads the observation indicated

        """

        # Default values for variables
        # -----------------------------------
        obs_oid = None
        product_type = 'OBSERVATION'
        data_retrieval_origin = 'P2SAPY'
        filename = None
        retrieval_type = 'PRODUCT'
        verbose = False
        # -- end of local variables declaration

        # Load variables values from the call
        # -----------------------------------
        for kwarg in kwargs:
            if kwarg == "obs_oid":
                obs_oid = kwargs[kwarg]
            elif kwarg == "product_type":
                product_type = kwargs[kwarg]
            elif kwarg == "data_retrieval_origin":
                data_retrieval_origin = kwargs[kwarg]
            elif kwarg == "filename":
                filename = kwargs[kwarg]
            elif kwarg == "retrieval_type":
                retrieval_type = kwargs[kwarg]
            elif kwarg == "verbose":
                verbose = kwargs[kwarg]
            # print current value
            print(kwarg, "=>", kwargs[kwarg])

        # -- end of local variables declaration

        # Build download condition

        retrieval_condition = ""

        # Check retrieval type
        if retrieval_type is not None:
            retrieval_condition = 'retrieval_type=' + retrieval_type
        else:
            raise ValueError("Value for mandatory parameter 'retrieval_type' is missed")

        # Check obs_oid
        if obs_oid is not None:
            retrieval_condition = retrieval_condition + "&" + 'observation_oid=' + obs_oid
        else:
            raise ValueError("Value for mandatory parameter 'observation_oid' is missed")

        # Check product_type
        if product_type is not None:
            retrieval_condition = retrieval_condition + "&" + 'product_type=' + product_type
        else:
            raise ValueError("Value for mandatory parameter 'product_type' is missed")

        # Check data_retrieval_origin
        if data_retrieval_origin is not None:
            retrieval_condition = retrieval_condition + "&" + 'data_retrieval_origin=' + data_retrieval_origin
        else:
            raise ValueError("Value for mandatory parameter 'data_retrieval_origin' is missed")

        # Build link to download P2SA observation
        link = self.data_url + retrieval_condition

        # #######################################################
        # The following lines are only for debug purposes
        # #######################################################
        log.info("Get p2sa observation link: %s" % link)
        # #######################################################

        try:
            # Sending download request to P2SA TAP
            response = self.execute_query(link)
            if response is not None:
                if filename is not None:
                    output_file_name = filename + ".tar"
                else:
                    output_file_name = obs_oid + ".tar"
                self.get_file(
                    output_file_name, response=response)
                if verbose:
                    log.info("[get_p2sa_observation()] Wrote {0} to {1}".format(link, output_file_name))
                # __end_if
                # return link
            # __end_if
            else:
                log.error("Error occurred when downloading the requested observation: " + response.raise_for_status())

        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        #     log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # _end_of_get_p2sa_observation

    def get_p2sa_product(self, **kwargs):
        """
        Example: http://p2sa.esac.esa.int/p2sa-sl-tap/data?retrieval_type=PRODUCT&QUERY=SELECT%20*%20
        FROM%20p2sa.file%20where%20file_oid%20%20in%20(6550)&data_retrieval_origin=P2SAPY

        Parameters
        ----------
        input_retrieval_type: string

            (Description TBD)

        input_file_oid_list : Array

            (List of fileOids to download.

        input_data_retrieval_origin: string
            (Description TBD)

        filename: string
            (Description TBD)

        verbose : bool
            optional, default 'False'
            flag to display information about the process

        Returns
        -------
        None. It downloads the files indicated
        """

        # Default values for variables
        # -----------------------------------
        select_query = 'QUERY=SELECT+file_name%2C+file_path+FROM+p2sa.file+where+file_oid+in+%28@fileOidList@%29'
        replace_pattern = '@fileOidList@'
        file_oid_list = None
        selected_oids = ""
        download_filename = ""
        retrieval_condition = ""
        retrieval_type = 'PRODUCT'
        filename = None
        data_retrieval_origin = 'P2SAPY'
        verbose = False
        array_index = 0

        # Load variables values from the call
        # -----------------------------------
        for kwarg in kwargs:
            if kwarg == "file_oid_list":
                file_oid_list = kwargs[kwarg]
            elif kwarg == "retrieval_type":
                retrieval_type = kwargs[kwarg]
            elif kwarg == "data_retrieval_origin":
                data_retrieval_origin = kwargs[kwarg]
            elif kwarg == "filename":
                filename = kwargs[kwarg]
            elif kwarg == "verbose":
                verbose = kwargs[kwarg]
            # print current value
            print(kwarg, "=>", kwargs[kwarg])

        # Check parameters and build the request
        # ---------------------------------------

        # Check product_type
        if retrieval_type is not None:
            retrieval_condition = retrieval_condition + 'retrieval_type=' + retrieval_type
        else:
            raise ValueError("Value for mandatory parameter 'product_type' is missed")

        # Check list of file_oids
        if file_oid_list is not None:

            for file_oid in file_oid_list:
                selected_oids = selected_oids + file_oid
                download_filename = download_filename + file_oid
                array_index = array_index + 1
                if array_index < len(file_oid_list):
                    selected_oids = selected_oids + ","
                    download_filename = download_filename + "_"
                # __end_if
            # __end_for
            # Replace the list of file_oids in the query String
            select_query_with_oids = select_query.replace(replace_pattern, selected_oids)

        else:
            raise ValueError("Value for mandatory parameter 'file_oid_list' is missed")

        # With the list of file_oids replaced now we can build the final query
        retrieval_condition = retrieval_condition + "&" + select_query_with_oids

        # Check data_retrieval_origin
        if data_retrieval_origin is not None:
            retrieval_condition = retrieval_condition + "&" + 'data_retrieval_origin=' + data_retrieval_origin
        else:
            raise ValueError("Value for mandatory parameter 'data_retrieval_origin' is missed")

        # Build link to download P2SA observation
        link = self.data_url + retrieval_condition

        try:
            # Launch the request to P2SA tap
            result = self.execute_download_query(link)

            ########################################################
            # The following lines are only for debug purposes
            ########################################################
            log.info("Filename: %s" % filename)
            log.info("Download url: %s" % str(link))
            ########################################################
            # return link

            if result is not None:

                if filename is None:
                    filename = "" + download_filename + ".tar"
                # __end_if

                self.get_file(filename, response=result)

                if verbose:
                    log.info("[get_p2sa_product()] Wrote {0} to {1}".format(link, filename))
                # __end_if
                # return link
            else:
                log.error("Error occurred when downloading the requested product")
            # __end_if
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        # log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # _end_of_get_p2sa_product

    def display_p2sa_movie_file(self, **kwargs):
        """Download postcards from P2SA

        Example: http://p2sa.esac.esa.int/p2sa-sl-tap/video?file_oid=13785&data_retrieval_origin=P2SAPY

        Parameters
        ----------
        :param kwargs, undefined number of parameters in a format of key=value. The following is a list with the
        accepted parameters, file_oid, data_retrieval_origin, verbose, retrieval_condition.

        Returns
        -------
        Link to download the movie

        Raises
        ------
        ValueError, IOError, ImportError, EOFError, KeyboardInterrupt
        """

        # Default values for variables
        # -----------------------------------
        file_oid = None
        data_retrieval_origin = 'P2SAPY'
        verbose = False
        retrieval_condition = ""

        # Load variables values from the call
        # -----------------------------------
        for kwarg in kwargs:
            if kwarg == "file_oid":
                file_oid = kwargs[kwarg]
            elif kwarg == "data_retrieval_origin":
                data_retrieval_origin = kwargs[kwarg]
            elif kwarg == "verbose":
                verbose = kwargs[kwarg]
            # print current value
            # print(kwarg, "=>", kwargs[kwarg])

        # Check parameters and build the request
        # ---------------------------------------

        # Check product_type
        if file_oid is not None:
            retrieval_condition = retrieval_condition + 'file_oid=' + file_oid
        else:
            raise ValueError("Value for mandatory parameter 'file_oid' is missed")

        # Check data_retrieval_origin
        if data_retrieval_origin is not None:
            retrieval_condition = retrieval_condition + "&" + 'data_retrieval_origin=' + data_retrieval_origin
        else:
            raise ValueError("Value for mandatory parameter 'file_oid' is missed")

        # Build link to display P2SA video.
        link: object = self.video_url + retrieval_condition
        try:
            # Launch the request to P2SA tap
            result = self.execute_download_query(link)

            if result is not None:

                ########################################################
                # The following lines are only for debug purposes
                ########################################################
                # log.info("Download url: %s" % str(link))
                ########################################################
                return link
            else:
                log.error("Error occurred when downloading the requested observation: " + result.raise_for_status())

            if verbose:
                log.info(link)
            # __end_if
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        #   log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # display_p2sa_movie_file

    def get_p2sa_postcard(self, **kwargs):
        """
        Download postcards from P2SA

        Example: /p2sa-sl-tap/data?retrieval_type=PRODUCT&observation_oid=198026707&resolution=low&product_type
        =POSTCARD&data_retrieval_origin=P2SAPY

        Parameters
        ----------

        input_retrieval_type: string

            (Description TBD)

        input_observation_oid : string

            (Description TBD)

        input_resolution: string

            (Description TBD)

        input_data_retrieval_origin: string

            (Description TBD)

        filename: string
            (Description TBD)

        input_product_type: string

            (Description TBD)

        verbose : bool
            optional, default 'False'
            flag to display information about the process

        Returns
        -------
        None. It downloads the observation postcard indicated
        """

        # Default values for variables
        # -----------------------------------
        observation_oid = None
        resolution = "low"
        filename = None
        retrieval_type = "PRODUCT"
        product_type = "POSTCARD"
        verbose = False
        data_retrieval_origin = "P2SAPY"
        retrieval_condition = None

        # Load variables values from the call
        # -----------------------------------
        for kwarg in kwargs:
            if kwarg == "observation_oid":
                observation_oid = kwargs[kwarg]
            elif kwarg == "resolution":
                resolution = kwargs[kwarg]
            elif kwarg == "filename":
                filename = kwargs[kwarg]
            elif kwarg == "retrieval_type":
                retrieval_type = kwargs[kwarg]
            elif kwarg == "product_type":
                product_type = kwargs[kwarg]
            elif kwarg == "data_retrieval_origin":
                data_retrieval_origin = kwargs[kwarg]
            elif kwarg == "verbose":
                verbose = kwargs[kwarg]
            # print current value
            print(kwarg, "=>", kwargs[kwarg])

        # Check parameters and build the request
        # ---------------------------------------

        # Check retrieval_type
        if retrieval_type is not None:
            retrieval_condition = 'RETRIEVAL_TYPE=' + retrieval_type
        else:
            raise ValueError("Value for mandatory parameter 'retrieval_type' is missed")

        # Check observation_oid
        if observation_oid is not None:
            retrieval_condition = retrieval_condition + "&" + 'observation_oid=' + observation_oid
        else:
            raise ValueError("Value for mandatory parameter 'observation_oid' is missed")

        # Check Resolution
        if resolution is not None:
            retrieval_condition = retrieval_condition + "&" + "resolution=" + resolution
        else:
            raise ValueError("Value for mandatory parameter 'resolution' is missed")

        # Check product_type
        if product_type is not None:
            retrieval_condition = retrieval_condition + "&" + 'PRODUCT_TYPE=' + product_type
        else:
            raise ValueError("Value for mandatory parameter 'product_type' is missed")

        # Check data_retrieval_origin
        if data_retrieval_origin is not None:
            retrieval_condition = retrieval_condition + "&" + 'data_retrieval_origin=' + data_retrieval_origin
        else:
            raise ValueError("Value for mandatory parameter 'data_retrieval_origin' is missed")

        # Build link to download P2SA postcard
        link = self.data_url + retrieval_condition

        try:
            # Launch the request to P2SA tap
            result = self.execute_download_query(link)

            if result is not None:
                if filename is None:
                    filename = "postcard_" + observation_oid + ".jpg"
                # __end_if

                self.get_file(filename, response=result)

                if verbose:
                    log.info("[get_p2sa_postcard()] Wrote {0} to {1}".format(link, filename))
                # __end_if

                ########################################################
                # The following lines are only for debug purposes
                ########################################################
                log.info("Filename: %s" % filename)
                log.info("Download url: %s" % str(link))
                ########################################################
                return link
            else:
                log.error("Error occurred when downloading the requested observation: ")
            # __end_if
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        # log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # _end_of_get_p2sa_postcard

    def query_carrington_movie(self, **kwargs):
        """
        It executes a query over P2SA observations and download the xml with the results.

        Parameters
        ----------
        Returns
        -------
        Table with the result of the query. It downloads metadata as a file.


        Examples
        --------

        http://p2sa.esac.esa.int/p2sa-sl-tap/tap/sync?REQUEST=doQuery&LANG=ADQL&FORMAT=JSON&PHASE=RUN&QUERY=
        SELECT file_oid FROM p2sa.v_carrington_rotation_file
        WHERE  (end_date > '2010-10-12 00:00:00')
        AND   (start_date < '2010-10-13 00:00:00')
        AND   (file_type  in  ('CR','CR_YELLOW'))
        ORDER BY start_date ASC
        """
        # Global variables declaration
        # -----------------------------
        from_date = ""
        to_date = ""
        file_type = None
        input_date = None
        links_to_movies_array: Dict[Union[int, Any], object] = {}

        # Query Pattern
        # -----------------------------------
        initial = "REQUEST=doQuery&LANG=ADQL&FORMAT=JSON&PHASE=RUN"
        query = "&QUERY=SELECT file_oid FROM p2sa.v_carrington_rotation_file"
        where_condition = " WHERE "
        date_condition = " (end_date > '@to_date_pattern@') AND (start_date < '@from_date_pattern@') "
        file_type_condition = " AND (file_type  in  (@file_type_pattern@))"
        default_file_type = "'CR','CR_YELLOW'"
        final = " ORDER BY start_date ASC "

        to_date_pattern = "@to_date_pattern@"
        from_date_pattern = "@from_date_pattern@"
        file_type_pattern = "@file_type_pattern@"

        for kwarg in kwargs:
            if kwarg == "input_date":
                input_date = kwargs[kwarg]
            elif kwarg == "file_type":
                file_type = kwargs[kwarg]
            # print current value
            print(kwarg, "=>", kwargs[kwarg])

        # Check fromDate parameter
        if file_type is not None:
            # replace day patterns by their values
            file_type = "'" + file_type + "'"
            file_type_condition = file_type_condition.replace(file_type_pattern, file_type)
        else:
            file_type_condition = file_type_condition.replace(file_type_pattern, default_file_type)
        # __end_if

        if input_date is not None:
            # parse date and add 24h
            from_date = input_date
            dt = dateutil.parser.parse(input_date)
            date = datetime.strptime(input_date, "%Y-%m-%d")

            # now add 24h
            modified_date = date + timedelta(days=1)
            to_date = modified_date.strftime('%Y-%m-%d 00:00:00')

            # replace day patterns by their values
            date_condition = date_condition.replace(to_date_pattern, to_date)
            date_condition = date_condition.replace(from_date_pattern, from_date)

        else:
            raise ValueError("Error!!!! Missed mandatory parameter 'input_date'")
        # __end_if

        # build metadata search query
        metadata_query = initial + query + where_condition + date_condition + file_type_condition + final

        # Encode metadata query
        encoded_metadata_query = self.encode_string_if_needed(metadata_query)

        # Build final query
        link = self.metadata_url + encoded_metadata_query

        ########################################################
        # The following lines are only for debug purposes
        ########################################################
        log.info("Metadata Query: %s" % link)
        ########################################################

        try:
            # Launch the request to P2SA tap
            result = self.execute_download_query(link)
            index = 0
            if result is not None:
                response_content = result.read()
                result_text = json.loads(response_content)
                file_oid_list = result_text["data"]
                for file_oid_element in file_oid_list:
                    movie_link = self.display_p2sa_movie_file(file_oid=file_oid_element[0])
                    links_to_movies_array[index] = movie_link
                    if index < len(file_oid_list):
                        index = index + 1
                    # end_if
                # end_for
                return links_to_movies_array
            else:
                raise ValueError("Error occurred when downloading the requested observation")
            # __end_if
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        # log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")
        return links_to_movies_array

    # _end_of_query_carrington_movie

    def query_p2sa_observations(self, **kwargs):

        """
        It executes a query over P2SA observations and download the xml with the results.

        Parameters
        ----------
        input_instruments : array of strings
            optional
            output format of the query

        input_fromDate: String
            TBD

        input_toDate: String
            TBD
        filename : string
            file name to be used to store the metadata, optional, default None
        output_format : array of string
            optional, default 'votable'
            output format of the query
        verbose : bool
            optional, default 'False'
            Flag to display information about the process

        Returns
        -------
        Table with the result of the query. It downloads metadata as a file.


        Examples
        --------
        REQUEST=doQuery&LANG=ADQL&FORMAT=json&QUERY=SELECT+*+FROM+v_observation+ WHERE+((instrument_name='SWAP')+OR+(instrument_name='LYRA'))+AND+begin_date>'2017-01-07'&PAGE=1&PAGE_SIZE=1000

        """

        # Default values for variables
        # -----------------------------------

        where_condition = " WHERE "
        where_instrument_condition = ""
        where_date_condition = ""

        instruments_query_pattern = "(instrument_name='@instrument@')"
        instrument_pattern = "@instrument@"
        from_date_query_pattern = "(obs.end_date > '@date@')"
        date_pattern = "@date@"
        to_date_query_pattern = "(obs.begin_date < '@date@')"
        instruments_query_string = ""
        from_date_query_string = ""
        to_date_query_string = ""
        verbose = False
        filename = ""
        from_date = ""
        to_date = ""
        instruments = ""
        output_format = "csv"

        # Load variables values from the call
        # -----------------------------------
        for kwarg in kwargs:
            if kwarg == "instruments":
                instruments = kwargs[kwarg]
            elif kwarg == "from_date":
                from_date = kwargs[kwarg]
            elif kwarg == "to_date":
                to_date = kwargs[kwarg]
            elif kwarg == "output_format":
                output_format = kwargs[kwarg]
            elif kwarg == "filename":
                filename = kwargs[kwarg]
            elif kwarg == "verbose":
                verbose = kwargs[kwarg]
            # print current value
            print(kwarg, "=>", kwargs[kwarg])

        # Query Pattern
        # -----------------------------------
        initial = "REQUEST=doQuery&LANG=ADQL&FORMAT=" + str(output_format) + "&PHASE=RUN"
        query = "SELECT obs.observation_oid, obs.instrument_name, obs.observation_type, obs.begin_date, " \
                "obs.end_date, obs.processing_level, obs.science_objective, obs.wavelength_range, " \
                "obs.science_object_name, obs.file_name, obs.file_format, obs.file_size, obs.observatory_name, " \
                "obs.calibrated FROM p2sa.v_observation as obs "
        final = " ORDER BY obs.begin_date ASC"

        #  Check parameter values
        # -----------------------------------

        # Check if instrument list is null
        if instruments is not None:
            if len(instruments) > 0:
                array_index = 0
                for instrument in instruments:
                    instruments_query_string = instruments_query_string + instruments_query_pattern.replace(
                        instrument_pattern, instrument)
                    array_index = array_index + 1
                    if array_index < len(instruments):
                        instruments_query_string = instruments_query_string + " OR "
                    # __end_if
                # __end_for
            # __end_if
        # __end_if

        # Check fromDate parameter
        if from_date is not None:
            from_date_query_string = from_date_query_pattern.replace(date_pattern, from_date)
        # __end_if

        # Check toDate parameter
        if to_date is not None:
            to_date_query_string = to_date_query_pattern.replace(date_pattern, to_date)
        # __end_if

        # Check if we need a "WHERE" condition
        if instruments or from_date or to_date:
            query = query + where_condition

        # __end_if

        # Build instruments query string
        if instruments_query_string:
            where_instrument_condition = " (" + instruments_query_string + ")"
            query = query + where_instrument_condition
        # __end_if

        # check now date range conditions
        if to_date and from_date:
            where_date_condition = where_date_condition + from_date_query_string + " AND " + to_date_query_string
        elif to_date:
            where_date_condition = where_date_condition + to_date_query_string
        elif from_date:
            where_date_condition = where_date_condition + from_date_query_string

        # Add final where date condition
        if instruments_query_string:
            query = query + " AND " + where_date_condition
        else:
            query = query + where_date_condition

        # # build metadata search query
        # metadata_query = initial + "&QUERY=" + query + final
        #
        # # Encode metadata query
        # encoded_metadata_query = self.encode_string_if_needed(metadata_query)
        #
        # # Build final query
        # link = self.metadata_url + encoded_metadata_query

        link = query + final

        ########################################################
        # The following lines are only for debug purposes
        ########################################################
        log.info("Metadata Query: %s" % link)
        ########################################################

        try:
            # Launch the request to P2SA tap
            result = self.execute_query(link, filename)

            if result is not None:
                # if filename is None:
                #    filename = "p2sa_observations"
                # __end_if
                if verbose:
                    log.info("[get_p2sa_observation()] Wrote {0} to {1}".format(link, filename))
                # __end_if
                # return self.get_table(filename, response=result, output_format=output_format)
                return result
            else:
                log.error("Error occurred when downloading the requested observation")
            # __end_if
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        # log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # _end_of_query_p2sa_observations

    def query_p2sa_tap(self, query, output_file=None, output_format='votable', verbose=False, dump_to_file=False):

        """Launches a synchronous job to query the P2SA tap

        Parameters
        ----------
        query : str, mandatory
            query (adql) to be executed
        output_file : str, optional, default None
            file name where the results are saved if dumpToFile is True.
            If this parameter is not provided, the jobid is used instead
        output_format : str, optional, default 'votable'
            results format
        verbose : bool, optional, default 'False'
            flag to display information about the process
        dump_to_file: boolean, optional.

        Returns
        -------
        A table object
        """
        try:
            job = self.launch_job(query=query,
                                  output_file=output_file,
                                  output_format=output_format,
                                  verbose=verbose,
                                  dump_to_file=dump_to_file)
            table = job.get_results()
            return table
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        # except:
        # print("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # __end_queryP2SATap

    def get_p2sa_tables(self, only_names=True, verbose=False):
        """Get the available table in P2SA TAP service
        Parameters
        ----------
        only_names : bool, TAP+ only, optional, default 'False'
            True to load table names only
        verbose : bool, optional, default 'False'
            flag to display information about the process
        Returns
        -------
        A list of tables
        """

        tables = self.load_tables(only_names=only_names,
                                  include_shared_tables=False,
                                  verbose=verbose)
        if only_names is True:
            table_names = []
            for t in tables:
                table_names.append(t.name)
            return table_names
        else:
            return tables

    # __end_getTables

    def get_p2sa_columns(self, table_name, only_names=True, verbose=False):
        """Get the available columns for a table in P2SA TAP service
        Parameters
        ----------
        table_name : string, mandatory, default None
            table name of which, columns will be returned
        only_names : bool, TAP+ only, optional, default 'False'
            True to load table names only
        verbose : bool, optional, default 'False'
            flag to display information about the process
        Returns
        -------
        A list of columns
        """

        tables = self.load_tables(only_names=False,
                                  include_shared_tables=False,
                                  verbose=verbose)
        columns = None
        for t in tables:
            if str(t.name) == str(table_name):
                columns = t.columns
                break

        if columns is None:
            raise ValueError("table name specified is not found in "
                             "P2SA TAP service")

        if only_names is True:
            column_names = []
            for c in columns:
                column_names.append(c.name)
            return column_names
        else:
            return columns

    # __end_getColumns

    def get_file(self, filename, response):

        """
        This method parses the request response into a file.

        Parameters
        ----------
        filename: String
            name for the output file

        response: String
            output response from P2SA Tap server
        """

        try:
            with open(filename, 'wb') as fh:
                response_content = response.read()
                fh.write(response_content)

            if os.pathsep not in filename:
                log.info("File {0} downloaded to current "
                         "directory".format(filename))
            else:
                log.info("File {0} downloaded".format(filename))

        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        except:
            log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # end_of_get_file

    def get_table(self, filename, response, output_format='csv'):

        """
        This method parses the response into a formatted table.

        Parameters
        ----------

        filename: String
            name for the output file

        response: String
            output response from P2SA Tap server

        output_format:
            format in which the file will be written: votable_plain, ascii, csv...

        Returns
        -------
        table in the desired format
        """
        try:
            with open(filename, 'wb') as fh:
                response_content = response.read()
                fh.write(response_content)

            table = modelutils.read_results_table_from_file(filename,
                                                            str(output_format))
            return table
        except IOError:
            log.error('An error occurred trying to read the file.')
            log.error(IOError.get('message'))
        except ValueError:
            log.error('Error found in Value')
            log.error(ValueError.get('message'))
        except ImportError:
            log.error("NO module found")
            log.error(ImportError.get('message'))
        except EOFError:
            log.error('EOF found!!')
            log.error(EOFError.get('message'))
        except KeyboardInterrupt:
            log.error('Operation cancelled by User')
            log.error(KeyboardInterrupt.get('message'))
        except:
            log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # end_of_get_table

    # execute_query
    def execute_query(self, link, filename=None):
        # Check if the user is already logged. If not the prompt for the login will be shown.

        try:
            # self.check_user_access()
            # result = self._Tap__connHandler._TapConn__execute_get(link)
            job = self.launch_job(query=link, output_file=filename)
            result = job.results
            return result
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        except:
            a = str(sys.exc_info()[0])
            print(a)
            log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # __end_of_execute_query

    # execute_query
    def execute_download_query(self, link):

        try:
            # self.check_user_access()
            result = self._Tap__connHandler._TapConn__execute_get(link)
            return result
        except IOError as e:
            log.error('An error occurred trying to read the file.')
            log.error(e)
        except ValueError as e:
            log.error('Error found in Value')
            log.error(e)
        except ImportError as e:
            log.error("NO module found")
            log.error(e)
        except EOFError as e:
            log.error('EOF found!!')
            log.error(e)
        except KeyboardInterrupt as e:
            log.error('Operation cancelled by User')
            log.error(e)
        except:
            log.error("Error. Please review your request", str(sys.exc_info()[0]), "occurred.")

    # __end_of_execute_query

    def encode_string_if_needed(self, string_to_replace):
        """
        This method detects if there it is a search by prefix. In that case it will be necessary to encode the character

        Parameters
        ----------
        string_to_replace : string, mandatory, default None
            table name of which, columns will be returned
        Returns
        -------
        String with a special character encoded
        """
        character_asterisk = "*"
        minus_than_character = "<"
        major_than_character = ">"
        single_quote_character = "'"
        white_spaces = " "
        replaced_string = string_to_replace

        # Encode asterisks
        if character_asterisk in replaced_string:
            replaced_string = replaced_string.replace(
                character_asterisk, "%25")
        # _end_if

        # check for white spaces
        if white_spaces in replaced_string:
            replaced_string = replaced_string.replace(
                white_spaces, "%20")
        # _end_if

        # check for minus_than_character
        if minus_than_character in replaced_string:
            replaced_string = replaced_string.replace(
                minus_than_character, "%3C")
        # _end_if

        # check for major_than_character
        if major_than_character in replaced_string:
            replaced_string = replaced_string.replace(
                major_than_character, "%3E")
        # _end_if

        # check for single_quote_character
        if single_quote_character in replaced_string:
            replaced_string = replaced_string.replace(
                single_quote_character, "%27")
        # _end_if

        return replaced_string

    # end_of_encode_string_if_needed


# -------------------------------
# ------ End of Class -----------
# -------------------------------

ESAP2SA = ESAP2SAClass()
