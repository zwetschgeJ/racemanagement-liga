import numpy as np
import pandas as pd

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
    data = [
        # 1 - Berlin
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
            1 RSN KYC(BW) MSC SVI BYC(BA) FSC
            2 MYC WYC NRV DYC SMCÜ SV03
            3 KYC(SH) ASVW JSC BYCÜ BYC(BE) VSaW
            4 KYC(SH) MSC JSC SV03 FSC DYC
            5 ASVW BYC(BE) BYC(BA) WYC NRV SVI
            6 VSaW RSN BYCÜ SMCÜ KYC(BW) MYC
            7 MSC RSN WYC BYC(BE) JSC MYC
            8 FSC BYC(BA) DYC ASVW VSaW SMCÜ
            9 BYCÜ SV03 SVI NRV KYC(SH) KYC(BW)
            10 DYC VSaW SVI RSN KYC(SH) WYC
            11 KYC(BW) NRV ASVW FSC MYC JSC
            12 SMCÜ BYCÜ BYC(BE) BYC(BA) SV03 MSC
            13 DYC BYCÜ MYC ASVW SVI MSC
            14 WYC JSC KYC(BW) VSaW SV03 BYC(BA)
            15 BYC(BE) KYC(SH) FSC SMCÜ RSN NRV
            16 BYC(BA) KYC(SH) VSaW MYC MSC NRV
            17 SV03 DYC RSN KYC(BW) ASVW BYC(BE)
            18 JSC SVI SMCÜ FSC WYC BYCÜ
            19 MSC ASVW SMCÜ KYC(BW) WYC KYC(SH)
            20 SVI FSC SV03 BYC(BE) MYC VSaW
            21 NRV DYC BYC(BA) JSC BYCÜ RSN
            22 NRV MSC ASVW SV03 VSaW RSN
            23 WYC BYC(BE) FSC BYCÜ DYC KYC(BW)
            24 BYC(BA) MYC KYC(SH) SVI SMCÜ JSC
            25 BYCÜ VSaW NRV MSC FSC WYC
            26 SMCÜ KYC(BW) BYC(BE) JSC DYC SVI
            27 SV03 BYC(BA) KYC(SH) MYC RSN ASVW
            28 SVI SMCÜ MSC VSaW JSC ASVW
            29 FSC SV03 RSN KYC(SH) BYCÜ WYC
            30 BYC(BE) NRV MYC BYC(BA) KYC(BW) DYC
            31 BYC(BE) SVI WYC BYC(BA) ASVW SV03
            32 JSC MYC DYC KYC(SH) MSC FSC
            33 KYC(BW) SMCÜ VSaW RSN NRV BYCÜ
            34 KYC(BW) DYC VSaW MSC BYC(BE) KYC(SH)
            35 MYC FSC BYCÜ WYC ASVW BYC(BA)
            36 RSN JSC SV03 NRV SVI SMCÜ
            37 BYCÜ JSC SV03 KYC(BW) BYC(BA) MSC
            38 VSaW SVI FSC RSN MYC BYC(BE)
            39 ASVW WYC NRV DYC KYC(SH) SMCÜ
            40 BYC(BA) WYC RSN DYC VSaW JSC
            41 SV03 MYC BYC(BE) SMCÜ BYCÜ KYC(SH)
            42 MSC ASVW KYC(BW) NRV SVI FSC
            43 SMCÜ SV03 DYC VSaW BYC(BA) FSC
            44 NRV BYC(BE) KYC(SH) ASVW JSC BYCÜ
            45 WYC RSN MSC MYC KYC(BW) SVI
            46 ASVW RSN MSC FSC SMCÜ BYC(BE)
            47 KYC(SH) KYC(BW) BYCÜ SVI DYC BYC(BA)
            48 JSC VSaW MYC SV03 WYC NRV
        """,
        # 2 - Warnemünde
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
            1 BYC(BA) SV03 WYC RSN SMCÜ ASVW
            2 NRV VSaW KYC(SH) KYC(BW) MYC FSC
            3 MSC BYC(BE) SVI JSC BYCÜ DYC
            4 MSC WYC SVI FSC ASVW KYC(BW)
            5 BYC(BE) BYCÜ SMCÜ VSaW KYC(SH) RSN
            6 DYC BYC(BA) JSC MYC SV03 NRV
            7 WYC BYC(BA) VSaW BYCÜ SVI NRV
            8 ASVW SMCÜ KYC(BW) BYC(BE) DYC MYC
            9 JSC FSC RSN KYC(SH) MSC SV03
            10 KYC(BW) DYC RSN BYC(BA) MSC VSaW
            11 SV03 KYC(SH) BYC(BE) ASVW NRV SVI
            12 MYC JSC BYCÜ SMCÜ FSC WYC
            13 KYC(BW) JSC NRV BYC(BE) RSN WYC
            14 VSaW SVI SV03 DYC FSC SMCÜ
            15 BYCÜ MSC ASVW MYC BYC(BA) KYC(SH)
            16 SMCÜ MSC DYC NRV WYC KYC(SH)
            17 FSC KYC(BW) BYC(BA) SV03 BYC(BE) BYCÜ
            18 SVI RSN MYC ASVW VSaW JSC
            19 WYC BYC(BE) MYC SV03 VSaW MSC
            20 RSN ASVW FSC BYCÜ NRV DYC
            21 KYC(SH) KYC(BW) SMCÜ SVI JSC BYC(BA)
            22 KYC(SH) WYC BYC(BE) FSC DYC BYC(BA)
            23 VSaW BYCÜ ASVW JSC KYC(BW) SV03
            24 SMCÜ NRV MSC RSN MYC SVI
            25 JSC DYC KYC(SH) WYC ASVW VSaW
            26 MYC SV03 BYCÜ SVI KYC(BW) RSN
            27 FSC SMCÜ MSC NRV BYC(BA) BYC(BE)
            28 RSN MYC WYC DYC SVI BYC(BE)
            29 ASVW FSC BYC(BA) MSC JSC VSaW
            30 BYCÜ KYC(SH) NRV SMCÜ SV03 KYC(BW)
            31 BYCÜ RSN VSaW SMCÜ BYC(BE) FSC
            32 SVI NRV KYC(BW) MSC WYC ASVW
            33 SV03 MYC DYC BYC(BA) KYC(SH) JSC
            34 SV03 KYC(BW) DYC WYC BYCÜ MSC
            35 NRV ASVW JSC VSaW BYC(BE) SMCÜ
            36 BYC(BA) SVI FSC KYC(SH) RSN MYC
            37 JSC SVI FSC SV03 SMCÜ WYC
            38 DYC RSN ASVW BYC(BA) NRV BYCÜ
            39 BYC(BE) VSaW KYC(SH) KYC(BW) MSC MYC
            40 SMCÜ VSaW BYC(BA) KYC(BW) DYC SVI
            41 FSC NRV BYCÜ MYC JSC MSC
            42 WYC BYC(BE) SV03 KYC(SH) RSN ASVW
            43 MYC FSC KYC(BW) DYC SMCÜ ASVW
            44 KYC(SH) BYCÜ MSC BYC(BE) SVI JSC
            45 VSaW BYC(BA) WYC NRV SV03 RSN
            46 BYC(BE) BYC(BA) WYC ASVW MYC BYCÜ
            47 MSC SV03 JSC RSN KYC(BW) SMCÜ
            48 SVI DYC NRV FSC VSaW KYC(SH)
        """,
        # 3 - Hotel Kieler Yacht Club
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
            1 MYC ASVW DYC SMCÜ NRV BYCÜ
            2 MSC KYC(BW) WYC FSC KYC(SH) BYC(BE)
            3 VSaW JSC BYC(BA) RSN SVI SV03
            4 VSaW DYC BYC(BA) BYC(BE) BYCÜ FSC
            5 JSC SVI NRV KYC(BW) WYC SMCÜ
            6 SV03 MYC RSN KYC(SH) ASVW MSC
            7 DYC MYC KYC(BW) SVI BYC(BA) MSC
            8 BYCÜ NRV FSC JSC SV03 KYC(SH)
            9 RSN BYC(BE) SMCÜ WYC VSaW ASVW
            10 FSC SV03 SMCÜ MYC VSaW KYC(BW)
            11 ASVW WYC JSC BYCÜ MSC BYC(BA)
            12 KYC(SH) RSN SVI NRV BYC(BE) DYC
            13 FSC RSN MSC JSC SMCÜ DYC
            14 KYC(BW) BYC(BA) ASVW SV03 BYC(BE) NRV
            15 SVI VSaW BYCÜ KYC(SH) MYC WYC
            16 NRV VSaW SV03 MSC DYC WYC
            17 BYC(BE) FSC MYC ASVW JSC SVI
            18 BYC(BA) SMCÜ KYC(SH) BYCÜ KYC(BW) RSN
            19 DYC JSC KYC(SH) ASVW KYC(BW) VSaW
            20 SMCÜ BYCÜ BYC(BE) SVI MSC SV03
            21 WYC FSC NRV BYC(BA) RSN MYC
            22 WYC DYC JSC BYC(BE) SV03 MYC
            23 KYC(BW) SVI BYCÜ RSN FSC ASVW
            24 NRV MSC VSaW SMCÜ KYC(SH) BYC(BA)
            25 RSN SV03 WYC DYC BYCÜ KYC(BW)
            26 KYC(SH) ASVW SVI BYC(BA) FSC SMCÜ
            27 BYC(BE) NRV VSaW MSC MYC JSC
            28 SMCÜ KYC(SH) DYC SV03 BYC(BA) JSC
            29 BYCÜ BYC(BE) MYC VSaW RSN KYC(BW)
            30 SVI WYC MSC NRV ASVW FSC
            31 SVI SMCÜ KYC(BW) NRV JSC BYC(BE)
            32 BYC(BA) MSC FSC VSaW DYC BYCÜ
            33 ASVW KYC(SH) SV03 MYC WYC RSN
            34 ASVW FSC SV03 DYC SVI VSaW
            35 MSC BYCÜ RSN KYC(BW) JSC NRV
            36 MYC BYC(BA) BYC(BE) WYC SMCÜ KYC(SH)
            37 RSN BYC(BA) BYC(BE) ASVW NRV DYC
            38 SV03 SMCÜ BYCÜ MYC MSC SVI
            39 JSC KYC(BW) WYC FSC VSaW KYC(SH)
            40 NRV KYC(BW) MYC FSC SV03 BYC(BA)
            41 BYC(BE) MSC SVI KYC(SH) RSN VSaW
            42 DYC JSC ASVW WYC SMCÜ BYCÜ
            43 KYC(SH) BYC(BE) FSC SV03 NRV BYCÜ
            44 WYC SVI VSaW JSC BYC(BA) RSN
            45 KYC(BW) MYC DYC MSC ASVW SMCÜ
            46 JSC MYC DYC BYCÜ KYC(SH) SVI
            47 VSaW ASVW RSN SMCÜ FSC NRV
            48 BYC(BA) SV03 MSC BYC(BE) KYC(BW) WYC
        """,
        # 4 - Camp 24/7
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
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
        """,
        # - 5 Münchner Yacht-Club
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
            1 NRV BYC(BE) KYC(BW) MYC KYC(SH) JSC
            2 WYC SV03 VSaW ASVW MSC BYCÜ
            3 DYC SVI SMCÜ BYC(BA) RSN FSC
            4 DYC KYC(BW) SMCÜ BYCÜ JSC ASVW
            5 SVI RSN KYC(SH) SV03 VSaW MYC2
            6 FSC NRV BYC(BA) MSC BYC(BE) WYC
            7 KYC(BW) NRV SV03 RSN SMCÜ WYC
            8 JSC KYC(SH) ASVW SVI FSC MSC3
            9 BYC(BA) BYCÜ MYC VSaW DYC BYC(BE)
            10 ASVW FSC MYC NRV DYC SV03
            11 BYC(BE) VSaW SVI JSC WYC SMCÜ4
            12 MSC BYC(BA) RSN KYC(SH) BYCÜ KYC(BW)
            13 ASVW BYC(BA) WYC SVI MYC KYC(BW)
            14 SV03 SMCÜ BYC(BE) FSC BYCÜ KYC(SH)5
            15 RSN DYC JSC MSC NRV VSaW
            16 KYC(SH) DYC FSC WYC KYC(BW) VSaW
            17 BYCÜ ASVW NRV BYC(BE) SVI RSN6
            18 SMCÜ MYC MSC JSC SV03 BYC(BA)
            19 KYC(BW) SVI MSC BYC(BE) SV03 DYC
            20 MYC JSC BYCÜ RSN WYC FSC7
            21 VSaW ASVW KYC(SH) SMCÜ BYC(BA) NRV
            22 VSaW KYC(BW) SVI BYCÜ FSC NRV
            23 SV03 RSN JSC BYC(BA) ASVW BYC(BE)8
            24 KYC(SH) WYC DYC MYC MSC SMCÜ
            25 BYC(BA) FSC VSaW KYC(BW) JSC SV03
            26 MSC BYC(BE) RSN SMCÜ ASVW MYC9
            27 BYCÜ KYC(SH) DYC WYC NRV SVI
            28 MYC MSC KYC(BW) FSC SMCÜ SVI
            29 JSC BYCÜ NRV DYC BYC(BA) SV0310
            30 RSN VSaW WYC KYC(SH) BYC(BE) ASVW
            31 RSN MYC SV03 KYC(SH) SVI BYCÜ
            32 SMCÜ WYC ASVW DYC KYC(BW) JSC11
            33 BYC(BE) MSC FSC NRV VSaW BYC(BA)
            34 BYC(BE) ASVW FSC KYC(BW) RSN DYC
            35 WYC JSC BYC(BA) SV03 SVI KYC(SH)12
            36 NRV SMCÜ BYCÜ VSaW MYC MSC
            37 BYC(BA) SMCÜ BYCÜ BYC(BE) KYC(SH) KYC(BW)
            38 FSC MYC JSC NRV WYC RSN13
            39 SVI SV03 VSaW ASVW DYC MSC
            40 KYC(SH) SV03 NRV ASVW FSC SMCÜ
            41 BYCÜ WYC RSN MSC BYC(BA) DYC14
            42 KYC(BW) SVI BYC(BE) VSaW MYC JSC
            43 MSC BYCÜ ASVW FSC KYC(SH) JSC
            44 VSaW RSN DYC SVI SMCÜ BYC(BA)15
            45 SV03 NRV KYC(BW) WYC BYC(BE) MYC
            46 SVI NRV KYC(BW) JSC MSC RSN
            47 DYC BYC(BE) BYC(BA) MYC ASVW KYC(SH)16
            48 SMCÜ FSC WYC BYCÜ SV03 VSaW
        """,
        # 6 - Bayerischer Yacht-Club
        """Flight Race Boat 1 Boat 2 Boat 3 Boat 4 Boat 5 Boat 6
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
    ]

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
