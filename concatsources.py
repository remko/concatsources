#!/usr/bin/env python

B64CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

def vlqEncode(value):
	if value < 0:
		value = (-value << 1) | 1
	else:
		value = value << 1
	result = ""
	while True:
		digit = value & 31
		value = value >> 5
		if value > 0:
			digit = digit | 32
		result += B64CHARS[digit]
		if value <= 0:
			break
	return result

def relative(new, old):
	if old == None:
		return new
	return new - old
	
if __name__ == "__main__":
	import sys
	import json
	from optparse import OptionParser
	import base64

	parser = OptionParser()
	parser.add_option("-o", "--output", 
			dest="output", 
			help="write output to FILE", metavar="FILE")
	parser.add_option("--source-map-include-sources", 
			action="store_true", dest="includeSources", default=False,
			help="include sources in source map")

	(options, args) = parser.parse_args()
	
	result = {
		"version" : 3,
		"file": options.output,
		"sourceRoot": "",
		"sources": [],
		"sourcesContent": [],
		"names": [],
		"mappings": ""
	}
	mappings = []
	with open(options.output, "w") as out:
		previousSourceIndex = None
		previousSourceLine = None
		for filename in args:
			result["sources"].append(filename)
			sourceIndex = len(result["sources"]) - 1

			sourceContent = []
			with open(filename) as f:
				sourceLine = 0
				for line in f.readlines():
					sourceContent.append(line)
					out.write(line)
					mappings.append("".join([
						"A", 
						vlqEncode(relative(sourceIndex, previousSourceIndex)),
						vlqEncode(relative(sourceLine, previousSourceLine)),
						"A"
					]))
					previousSourceIndex = sourceIndex
					previousSourceLine = sourceLine
					sourceLine += 1

			if options.includeSources:
				result["sourcesContent"].append("".join(sourceContent))
			else:
				result["sourcesContent"].append(None)
		result["mappings"] = ";".join(mappings)

		sourceMappingURL = "data:application/json;base64," + base64.b64encode(json.dumps(result))
		if options.output.endswith(".js"):
			out.write("//# sourceMappingURL=%s\n" % sourceMappingURL)
		elif options.output.endswith(".css"):
			out.write("/*# sourceMappingURL=%s */\n" % sourceMappingURL)
