import subprocess

def call_cmd(CMD):
    conn = subprocess.Popen(
        CMD,
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return conn.stdout.readlines()


def get_or_else(l, i):
    try:
        return l[i]
    except:
        return None


def get_minutes(clock_time):
    hm, ampm = clock_time.split()
    h, m = [int(x) for x in hm.split(':')]
    t = m + (h + 12 if ampm == 'PM' else h) * 60
    return t