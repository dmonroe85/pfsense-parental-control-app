from joblib import Parallel, delayed

from lib.util import call_cmd, get_or_else
from lib.config import SUBNET, ARP_EXE, IFCONFIG_EXE, BLACKLIST, prefix_octets

def ping(ip):
    call_cmd(['ping', '-c', '1', '-W', '5', ip])

def get_this_ip(subnet):
    CMD = [IFCONFIG_EXE]
    result = call_cmd(CMD)
    return [
        word for line in result
        for word in line.decode("utf-8").strip().split()
        if word.startswith(subnet)
    ]

def find_devices():
    print("Querying this IP")
    blacklist = \
        set(get_this_ip(SUBNET)).union(BLACKLIST)

    print('Blacklist: {}'.format(blacklist))

    suffixes = list(range(1, 255))

    ips = \
        set(['.'.join(prefix_octets + [str(s)]) for s in suffixes]) - \
        blacklist

    results = Parallel(
        n_jobs=len(ips), 
        prefer='threads'
    )(
        delayed(ping)(ip) for ip in ips
    )

    CMD=[
        ARP_EXE, '-a'
    ]

    results = call_cmd(CMD)

    mac_ip_lkup = {}
    for r in results:
        print(r)
        r_split = r.decode('utf-8').split()
        ip_paren = r_split[1]
        mac = r_split[3]
        ip = ip_paren.lstrip('(').rstrip(')')

        if ip not in blacklist and 'incomplete' not in mac:
            mac_ip_lkup[mac] = ip

    return mac_ip_lkup