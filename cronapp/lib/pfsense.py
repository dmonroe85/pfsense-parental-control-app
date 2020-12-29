import time

def create_filter_rule_patch(new_rules):
    return {
        'filter': {
            'rule': new_rules
        }
    }


def get_rules(api):
    config = api.config_get()
    rules = config['filter']['rule']
    return (
        [r for r in rules if not r['descr'].startswith('Default')],
        [r for r in rules if r['descr'].startswith('Default')]
    )

def create_block_rule(descr, ip):
    t = str(int(time.time()))
    return {
        "type": "block",
        "ipprotocol": "inet",
        "descr": descr,
        "interface": "lan",
        "source": { "address": ip },
        "destination": { "any": "" },
        'tracker': t,
    }

def build_descr(b):
    return ':'.join([
        b['User'].replace(' ', '-'),
        b['Description'].replace(' ', '-'),
        b['Reason']
    ])[:52]


def build_new_rules(blocked_ip, current_block_ip):
    new_rules = []
    for d, i in sorted(blocked_ip, key=lambda r: (r[0], r[1])):
        current_ip = current_block_ip.get(d)

        if current_ip is not None and current_ip != i:
            new_rules.append(create_block_rule(d, current_ip))

        if i is not None:
            new_rules.append(create_block_rule(d, i))

    return new_rules