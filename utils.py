import numpy as np
import pandas as pd
import utils_pairing_list

BOATS = 6
FLIGHTS = 16
EVENTS = 6
TEAMS = ['ASVW', 'BYC(BA)', 'BYC(BE)', 'BYCÜ', 'DYC', 'FSC', 'JSC', 'KYC(BW)', 'KYC(SH)', 'MSC', 'MYC', 'NRV', 'RSN',
         'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC']

BUCHSTABEN = {'OCS': BOATS + 1,
              'DSQ': BOATS + 1,
              'DNF': BOATS + 1,
              'DNC': BOATS + 1,
              'OSC' : BOATS + 1,
              'RDG' : 1000,
              'No result': np.nan, }


def create_pairing_list(event):
    '''
    Temporary function to create (hard-coded) pairing list
    :return: Pairing list as a pandas DataFrame
    '''
    data = utils_pairing_list.data

    # Parse the data
    lines = data[event].strip().split('\n')
    parsed_data = []

    for line in lines[1:]:
        split_line = line.split()
        race = split_line[0].strip()
        boats = split_line[1:]
        temp_list = [int(race)]
        for boat_number, team in enumerate(boats, start=1):
            temp_list.append(team)
        parsed_data.append(temp_list)

    columns = ['Race']
    columns.extend(['Boat{}'.format(i) for i in range(1, 7)])
    df = pd.DataFrame(parsed_data, columns=columns)
    df['flight'] = [number for number in range(1, 17) for _ in range(3)]

    results_dict = {'Teams': TEAMS, 'SCP': [0] * len(TEAMS)}
    for flight in range(1, FLIGHTS + 1):
        results_dict[f'Flight {flight}'] = [np.nan] * len(TEAMS)
    results_dict['Total'] = [0] * len(TEAMS)
    results = pd.DataFrame(results_dict)

    return df, results


def count_values(row):
    # You can adjust this list based on the values you're interested in
    values_of_interest = [i for i in range(1, 6 + 2)]
    # TODO look only in Race{}.format() columns
    counts = {value: (row == value).sum() for value in values_of_interest}
    return pd.Series(counts)


def sort_results(result_df):
    result_df_copy = result_df.copy()

    result_df_copy.replace(BUCHSTABEN, inplace=True)
    result_df_copy.replace('-', np.nan, inplace=True)

    columns_to_sum = ['SCP']
    columns_to_sum.extend([f'Flight {i}' for i in range(1, FLIGHTS + 1)])
    for col in columns_to_sum:
        result_df_copy[col] = result_df_copy[col].astype(float)
    result_df_copy['Total'] = result_df_copy[columns_to_sum].sum(axis=1)
    counts_df = result_df_copy.apply(count_values, axis=1)
    result_df_copy = pd.concat([result_df_copy, counts_df], axis=1, )

    sort_column_list = ['Total']
    sort_column_list.extend([i for i in range(1, BOATS + 2)])
    sort_column_list.extend(['Flight {}'.format(i) for i in range(FLIGHTS, 1, -1)])

    sort_column_order_list = [True]
    sort_column_order_list.extend([False for i in range(1, BOATS + 2)])
    sort_column_order_list.extend([True for i in range(FLIGHTS, 1, -1)])

    result_df_copy.sort_values(by=sort_column_list, ascending=sort_column_order_list, inplace=True)

    index = result_df_copy.index
    result_df = result_df.reindex(index)
    result_df['Total'] = result_df_copy['Total']

    return result_df


def get_flight(race):
    return int(np.ceil(race / (len(TEAMS) / BOATS)))


def add_results(result_df):
    return result_df
