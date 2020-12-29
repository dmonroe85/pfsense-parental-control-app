import os, sys, json

_, conf_file = sys.argv

with open(conf_file, 'r') as infile:
	conf = json.load(infile)

PFSENSE_HOST = conf['PFSENSE_HOST']
G_SHEET_KEY = conf['G_SHEET_KEY']
apikey = conf['FAUXAPI_APIKEY']
apisecret = conf['FAUXAPI_APISECRET']
ARP_EXE = conf['ARP_EXE']
IFCONFIG_EXE = conf['IFCONFIG_EXE']
SUBNET = conf['SUBNET']
BLACKLIST_STRING = conf['BLACKLIST']
LAMBDA_GET_FUNCTION = conf['LAMBDA_GET_FUNCTION_NAME']

prefix_octets = [x for x in SUBNET.split('.') if x]
BLACKLIST = set([PFSENSE_HOST] + BLACKLIST_STRING.split(','))
