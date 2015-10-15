# test to see how a command line argument can be used to define a filename

import sys, json

null_list = [1, 3, 5, 7, 7, 2]

outName = sys.argv[1] + '.json'

def json_out(outlist, filename):	
	with open(filename, 'w') as outfile:
		outfile.write("{}\n".format(json.dumps(outlist, indent = 4)))
		print ('Output written to file -> %s') % filename

json_out(null_list, outName)