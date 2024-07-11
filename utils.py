import numpy as np
import pandas as pd

BOATS = 6
FLIGHTS = 16
TEAMS = ['ASVW', 'BYC(BA)', 'BYC(BE)', 'BYCÜ', 'DYC', 'FSC', 'JSC', 'KYC(BW)', 'KYC(SH)', 'MSC', 'MYC', 'NRV', 'RSN', 'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC']

BUCHSTABEN = {'OCS': BOATS+1,
              'DSQ': BOATS+1,
              'DNF': BOATS+1,
              'DNC': BOATS+1,}

def create_pairing_list():
    '''
    Temporary function to create (hard-coded) pairing list
    :return: Pairing list as a pandas DataFrame
    '''
    data = """
    Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
    1 KYC(SH) BYCÜ SV03 NRV MSC SVI
    2 VSaW FSC DYC BYC(BE) WYC JSC
    3 KYC(BW) RSN MYC SMCÜ BYC(BA) ASVW
    4 KYC(BW) SV03 MYC JSC SVI BYC(BE)
    5 RSN BYC(BA) MSC FSC DYC NRV
    6 ASVW KYC(SH) SMCÜ WYC BYCÜ VSaW
    7 SV03 KYC(SH) FSC BYC(BA) MYC VSaW
    8 SVI MSC BYC(BE) RSN ASVW WYC
    9 SMCÜ JSC NRV DYC KYC(BW) BYCÜ
    10 BYC(BE) ASVW NRV KYC(SH) KYC(BW) FSC
    11 BYCÜ DYC RSN SVI VSaW MYC
    12 WYC SMCÜ BYC(BA) MSC JSC SV03
    13 BYC(BE) SMCÜ VSaW RSN NRV SV03
    14 FSC MYC BYCÜ ASVW JSC MSC
    15 BYC(BA) KYC(BW) SVI WYC KYC(SH) DYC
    16 MSC KYC(BW) ASVW VSaW SV03 DYC
    17 JSC BYC(BE) KYC(SH) BYCÜ RSN BYC(BA)
    18 MYC NRV WYC SVI FSC SMCÜ
    19 SV03 RSN WYC BYCÜ FSC KYC(BW)
    20 NRV SVI JSC BYC(BA) VSaW ASVW
    21 DYC BYC(BE) MSC MYC SMCÜ KYC(SH)
    22 DYC SV03 RSN JSC ASVW KYC(SH)
    23 FSC BYC(BA) SVI SMCÜ BYC(BE) BYCÜ
    24 MSC VSaW KYC(BW) NRV WYC MYC
    25 SMCÜ ASVW DYC SV03 SVI FSC
    26 WYC BYCÜ BYC(BA) MYC BYC(BE) NRV
    27 JSC MSC KYC(BW) VSaW KYC(SH) RSN
    28 NRV WYC SV03 ASVW MYC RSN
    29 SVI JSC KYC(SH) KYC(BW) SMCÜ FSC
    30 BYC(BA) DYC VSaW MSC BYCÜ BYC(BE)
    31 BYC(BA) NRV FSC MSC RSN JSC
    32 MYC VSaW BYC(BE) KYC(BW) SV03 SVI
    33 BYCÜ WYC ASVW KYC(SH) DYC SMCÜ
    34 BYCÜ BYC(BE) ASVW SV03 BYC(BA) KYC(BW)
    35 VSaW SVI SMCÜ FSC RSN MSC
    36 KYC(SH) MYC JSC DYC NRV WYC
    37 SMCÜ MYC JSC BYCÜ MSC SV03
    38 ASVW NRV SVI KYC(SH) VSaW BYC(BA)
    39 RSN FSC DYC BYC(BE) KYC(BW) WYC
    40 MSC FSC KYC(SH) BYC(BE) ASVW MYC
    41 JSC VSaW BYC(BA) WYC SMCÜ KYC(BW)
    42 SV03 RSN BYCÜ DYC NRV SVI
    43 WYC JSC BYC(BE) ASVW MSC SVI
    44 DYC BYC(BA) KYC(BW) RSN MYC SMCÜ
    45 FSC KYC(SH) SV03 VSaW BYCÜ NRV
    46 RSN KYC(SH) SV03 SVI WYC BYC(BA)
    47 KYC(BW) BYCÜ SMCÜ NRV BYC(BE) MSC
    48 MYC ASVW VSaW JSC FSC DYC
    """

    # Parse the data
    lines = data.strip().split('\n')
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

    results_dict = {'Teams': TEAMS, 'SCP': [0]*len(TEAMS)}
    for flight in range(1,FLIGHTS+1):
        results_dict[f'Flight {flight}'] = [np.nan]*len(TEAMS)
    results_dict['Total'] = [0]*len(TEAMS)
    results = pd.DataFrame(results_dict)

    return df, results


def count_values(row):
    # You can adjust this list based on the values you're interested in
    values_of_interest = [i for i in range(1, 6+2)]
    # TODO look only in Race{}.format() columns
    counts = {value: (row == value).sum() for value in values_of_interest}
    return pd.Series(counts)


def sort_results(result_df):
    result_df_copy = result_df.copy()

    result_df_copy.replace(BUCHSTABEN, inplace=True)

    columns_to_sum = ['SCP']
    columns_to_sum.extend([f'Flight {i}' for i in range(1, FLIGHTS+1)])
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
    return int(np.ceil(race / (len(TEAMS)/BOATS)))


def add_results(result_df):

    return result_df