from esa_p2sa.p2sa_core import ESAP2SAClass

instrument_list = []

parameters = {'input_instruments': instrument_list,
              'input_to_date': "2015-08-06 00:00:00",
              'input_from_date': "2015-08-04 00:00:00",
              'output_format': "votable",
              'filename': 'output',
              'verbose': False}

p2sa = ESAP2SAClass()

results_table = p2sa.query_p2sa_observations(instruments=parameters['input_instruments'],
                                             from_date=parameters['input_from_date'],
                                             to_date=parameters['input_to_date'],
                                             output_format=parameters['output_format'],
                                             filename=parameters['filename'],
                                             verbose=parameters['verbose'])

print(results_table)
