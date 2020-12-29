import time

import pprint

from PfsenseFauxapi.PfsenseFauxapi import PfsenseFauxapi

from lib.block_rules import find_blocked
from lib.network import find_devices
from lib.pfsense import build_descr, \
                        get_rules, \
                        build_new_rules, \
                        create_filter_rule_patch
from lib.config import PFSENSE_HOST, apikey, apisecret
from lib.ov import get_overrides


def main():
    print('Starting PfSense Parental Control App')

    print('Finding LAN devices')
    devices = find_devices()

    print('Finding Rule Overides')
    overrides = get_overrides()

    print('Finding blocked users')
    blocked = find_blocked(devices, overrides)
    
    print('Resolving IP addresses')
    blocked_ip = [
        [build_descr(b), devices.get(b['MAC'])]
        for b in blocked
    ]

    print("Configuring Faux API")
    api = PfsenseFauxapi(PFSENSE_HOST, apikey, apisecret)
    api.proto = 'http'

    print("Requesting config")
    current_block_rules, default_rules = get_rules(api)
    current_block_ip = dict(
        (r['descr'], r['source']['address'])
        for r in current_block_rules
    )

    new_rules = build_new_rules(blocked_ip, current_block_ip)
    new_patch = create_filter_rule_patch(new_rules + default_rules)

    pprint.pprint(new_patch)
    print("patching")
    api.config_patch(new_patch)
    api.function_call({
        'function': 'filter_configure_sync',
        'args': [False],
        'includes': ['shaper.inc'],
    })

if __name__ == '__main__':
    t = time.time()
    main()

    print('Ran in {} seconds'.format(time.time() - t))
