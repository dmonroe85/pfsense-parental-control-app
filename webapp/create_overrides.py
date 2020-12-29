import sys
import json

_, userlist = sys.argv

ov_dict = dict((u, {}) for u in userlist.split(','))

with open('overrides.json', 'w') as outfile:
    json.dump(ov_dict, outfile)

print('Successfully created overrides file!')