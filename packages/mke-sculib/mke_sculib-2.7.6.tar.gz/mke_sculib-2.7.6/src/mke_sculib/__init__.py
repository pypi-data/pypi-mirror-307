__version__ = '2.7.6'

import mke_sculib.scu 
from mke_sculib.scu import scu as scu_api
from mke_sculib.scu import plot_tt, print_color, colors, log
from mke_sculib.sim import scu_sim
from mke_sculib.stellarium_api import stellarium_api as stellar_api
from mke_sculib.sim import plot_motion_pyplot as plot_motion
from mke_sculib.helpers import get_utcnow, make_zulustr, parse_zulutime

def activate_logging_mattermost(whoami, url_qry = 'http://10.98.76.45:8990/logurl'):
    if not "requests" in locals():
        import requests
    url = requests.get(f'{url_qry}').json().get('url')
    mke_sculib.scu.activate_logging_mattermost(url, whoami)
    return True


def link_stellarium(antenna_id='', stellarium_address = 'http://localhost:8090', debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):

    if not 'use_socket' in kwargs:
        kwargs['use_socket'] = False
    if not 'wait_done_by_uuid' in kwargs:
        kwargs['wait_done_by_uuid'] = False
    if not 'start_streams_on_construct':
        kwargs['start_streams_on_construct'] = False

    dish = load(antenna_id=antenna_id, debug=debug, url_qry=url_qry, **kwargs)
    dish.link_stellarium(stellarium_address)


def load(antenna_id='', post_put_delay=0.0, debug=False, url_qry = 'http://10.98.76.45:8990/antennas', **kwargs):

    if not "requests" in locals():
        import requests
    if not "json" in locals():
        import json

    if isinstance(antenna_id, int):
        antenna_id = str(antenna_id)
    

    if antenna_id == 'test_antenna' or antenna_id == 'sim':
        return scu_sim(antenna_id, debug=debug, **kwargs)
    else:
        antennas = requests.get(f'{url_qry}').json()

        if not antenna_id:
            prompt = '\n   '.join([f'{i: 3.0f}: Dish "{dc.get("id")}" @{dc.get("address")}' for i, dc in enumerate(antennas)])
            prompt = f'Found the following dishes to choose from:\n   {prompt}\n\n Please select one (0...{len(antennas)-1}): '
            isel = None
            allowed = [str(i) for i in range(len(antennas))]

            while not isel in allowed:
                if not isel is None:
                    print(f'INPUT: "{isel}" incorrect please try again')
                isel = input(prompt)

            dc = antennas[int(isel)]
            antenna_id = dc.get('id')

        else:
            ids = [a.get('id') for a in antennas]
            dcs = [a for a in antennas if a.get('id') == antenna_id]

            if not dcs:
                import warnings
                warnings.warn(f'requested {antenna_id=} not found in available {ids=}, trying to resolve')
                dcs = [a for a in antennas if antenna_id in a.get('id')]
            
            assert dcs, f'could not find any antenna which matches the requested {antenna_id=} in available {ids=}'
            dc = next(iter(dcs))
        
        # dc = requests.get(f'{url_qry}/{antenna_id}').json()
        
        assert antenna_id, 'need to give an antenna id'

        try:
            params = json.loads(dc['params_json'])
            
        except Exception as err:
            print('could not load "params_json" from server')
            params = {}
        dish = scu_api(dc['address'], post_put_delay=post_put_delay, debug=debug, antenna_id=antenna_id, **kwargs)
        for k, v in params.items():
            if hasattr(dish, k):
                setattr(dish, k, v)

        try:
            assert dish.ping(), 'ping failed!'
            dish.determine_dish_type()

        except Exception as err:
            log(f'Error when trying to initialize connection to dish {dish}', colors.FAIL)
            
        log(f'loaded dish: {dish}', colors.OKBLUE)
        return dish
        
