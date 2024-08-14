import numpy as np

BOATS = 6
FLIGHTS = 16
EVENTS = 4
TEAMS = ['ASVW', 'BYC (BA)', 'BYC (BE)', 'BYCÜ', 'DYC', 'FSC', 'JSC', 'KYC (BW)', 'KYC (SH)', 'MSC', 'MYC', 'NRV', 'RSN',
         'SMCÜ', 'SV03', 'SVI', 'VSaW', 'WYC']

BUCHSTABEN = {'OCS': BOATS + 1,
              'DSQ': BOATS + 1,
              'DNF': BOATS + 1,
              'DNC': BOATS + 1,
              'No result': np.nan, 
              'OSC': BOATS + 1, # Well
              }

max_race_columns = 16
race_columns = ['Flight {}'.format(i) for i in range(1,max_race_columns+1)]

link_event_01 = "19xaFNpplaFOW7dS-Efir9EMsDPV8oy4w6X6fTzO1uXo"
link_event_02 = "1rtMz8LQRaLdPvqoNXrbG30_DvkcmnQx7x_dJQijoJyY"
link_event_03 = "1LeFExyFaH101326yN82BKjLaPmX0uKKTK4g0lQvBquY"

link_test = "1fC3hQSpiOPVZW4lJp5cSr_t-8UER_1KzXmCi-9JbO3Y"


DISPLAY_COLORCODING = False
REFRESH_TIME = 60 # in seconds 