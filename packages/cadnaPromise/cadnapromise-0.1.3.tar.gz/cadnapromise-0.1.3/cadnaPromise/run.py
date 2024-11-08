#!/usr/bin/env python3
# coding=utf-8

# This file is part of PROMISE.
#
# 	PROMISE is free software: you can redistribute it and/or modify it
# 	under the terms of the GNU Lesser General Public License as
# 	published by the Free Software Foundation, either version 3 of the
# 	License, or (at your option) any later version.
#
# 	PROMISE is distributed in the hope that it will be useful, but WITHOUT
# 	ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# 	or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General
# 	Public License for more details.
#
# 	You should have received a copy of the GNU Lesser General Public
# 	License along with PROMISE. If not, see
# 	<http://www.gnu.org/licenses/>.
#
# Promise v1 was written by Romain Picot
# Promise v2 has been written from v1 by Thibault Hilaire and Sara Hoseininasab
# 	Sorbonne Université
# 	LIP6 (Computing Science Laboratory)
# 	Paris, France
# Contact: thibault.hilaire@lip6.fr
#
#
# File: runPromise.py
# Date: April 2020
#
# 	contain the entry function, called to run Promise
#
# 	© Thibault HILAIRE, April 2020


__doc__= """
\U0001f918 CadnaPromise \U0001f918

Usage:
	runPromise -h | --help
	runPromise (hsd|hs|sd) [options]

Options:
  -h --help                     Show this screen.
  --conf CONF_FILE              get the configuration file [default: promise.yml]
  --output OUTPUT               set the path of the output (where the result files are put)
  --verbosity VERBOSITY         set the verbosity (betwen 0  and 4 for very low level debug) [default: 1]
  --log LOGFILE                 set the log file (no log file if this is not defined)
  --verbosityLog VERBOSITY      set the verbosity of the log file
  --debug                       put intermediate files into `debug/` (and `compileErrors/` for compilation errrors) and display the execution trace when an error comes
  --run RUN                     file to be run
  --compile COMMAND             command to compile the code
  --files FILES                 list of files to be examined by Promise (by default, all the .cc files)
  --nbDigits DIGITS             general required number of digits
  --path PATH                   set the path of the project (by default, the current path)
  --pause                       do pause between steps
  --noParsing                   do not parse the C file (__PROMISE__ are replaced and that's all)
  --alias ALIAS                 allow aliases (examples "g++=g++-14") [default:""]
  hsd                           Half/Single/Double mixed-precision
  hs                            Half/Single mixed-precision
  sd                            Single/Double mixed-precision

  
"""

import os
from os.path import join
import sys
from collections import Counter

from .promise import Promise
from .utils import parseOptions, PromiseError, getYMLOptions, Timing, pause, commaAnd
from .utils import customArgParser, __params__
from .logger import PrLogger
from .prfile import PrFile


def runPromise(argv=None):
	"""This function is registered (in setup.py) as an entry_point
	argv is used for the unit tests"""

	# reset the logger and get a new instance
	logger = PrLogger()
	displayTrace = False


	# types handle by Promise
	typeNames = {'h': 'Half', 's': 'Single', 'd': 'Double', 'q': 'Quad'}
	types = {'h': 'half_float::half', 's': 'float', 'd': 'double', 'q': 'float128'}


	try:
		# import docopt
		# get the options from command line and yml file

		args = customArgParser(sys.argv[1:] if argv is None else argv, __params__)      # parse the command line
		# args = docopt.docopt(__doc__, argv=sys.argv[1:] if argv is None else argv)      # parse the command line

		displayTrace = args['--debug']
		logger.configureLogger(args)                                                   # configure the logger
		options = getYMLOptions(args)                                           # get the options from the yml file
		logger.message("\U0001f918 CadnaPromise \U0001f918")
		method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias = parseOptions(options)    # parse the options

		compiler = 'g++'
		if alias == {}:
			curr_loc = os.path.dirname(os.path.realpath(__file__))

			cachePath = "/cache"
			if os.path.exists(curr_loc + cachePath):
				if os.path.isfile(curr_loc + cachePath + '/.CXX.txt'):
					with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
						compiler = file.read()
	
					if compiler != 'g++' and compiler is not None:
						alias = {'--alias':compiler}

		logger.message("Using the compiler: {}".format(compiler))
		PrFile.setCustom(typeCustom)
		compileErrorPath = join(path, 'compileErrors') if args['--debug'] else None
		tempPath = join(path, 'debug') if args['--debug'] else None

		# run with timing
		with Timing() as timing:
			# create Promise object
			pr = Promise(path, files, run, nbDigits, compileLines, parsing=not args['--noParsing'], alias=alias)

			# display general infos
			logger.info("We are working with %d file%s and %d different types" %
			            (pr.nbFiles, ('' if pr.nbFiles < 2 else 's'), pr.nbVariables))
			logger.info(pr.expectation())

			# debug the files
			if args['--debug']:
				pr.exportParsedFiles(tempPath)

			# get the cadna reference
			highest = types['q'] if 'q' in method else types['d']
			pr.changeSameType(highest)
			logger.step("Get a reference result with Cadna (%s)" % highest)
			pr.compileAndRun(tempPath, cadna=True)
			if args['--pause']:
				pause()

			# try with the highest precision
			logger.step("Check with highest format (%s)" % typeNames[method[-1]])
			pr.changeSameType(types[method[-1]])
			
			if not pr.compileAndRun(tempPath):
				pr.changeSameType(highest)
				raise PromiseError("You should lower your expectation, it doesn't work with " + typeNames[method[-1]])
			
			if args['--pause']:
				pause()

			# do the Delta-Debug passes ('s','d' and then 'h','s' when method is 'hsd' for example)
			for lo, hi in reversed(list(zip(method, method[1:]))):
				logger.step("Delta-Debug %s/%s" % (typeNames[lo], typeNames[hi]))
				res = pr.runDeltaDebug(types[lo], types[hi], tempPath, args['--pause'], compileErrorPath)
				# stop if the DeltaDebug is not successful
				if not res:
					break

		# export the output
		if argv is None:
			pr.exportFinalResult(outputPath)


	except PromiseError as e:
		logger.error(e, exc_info=displayTrace)

	else:
		if timing:
			# display the number of each type
			count = Counter(pr.typesDict.values())  # count the nb of each type (result is a dictionary type:nb)
			li = ["%dx %s" % (v, k) for k, v in count.items()]
			logger.message("The final result contains %s.", commaAnd(li))
			logger.debug("Final types:\n" + pr.strResult())

			# display the stats
			logger.message("It tooks %.2fs", timing.timing)
			logger.message("\U0001F449 %d compilations (%d failed) for %.2fs", *pr.compilations)
			logger.message("\U0001F449 %d executions   (%d failed) for %.2fs", *pr.executions)

			logger.reset()
			return pr.setPerType()

	# reset the handlers, in case of running runPromise several times (otherwise, the log files are still open)
	logger.reset()


def runPromise_custom(argv=None):
	"""This function is registered (in setup.py) as an entry_point
	argv is used for the unit tests"""

	# reset the logger and get a new instance
	logger = PrLogger()
	displayTrace = False


	# types handle by Promise
	typeNames = {'h': 'Half', 's': 'Single', 'd': 'Double', 'q': 'Quad'}
	types = {'h': 'half_float::half', 's': 'float', 'd': 'double', 'q': 'float128'}


	try:
		# get the options from command line and yml file
		args = customArgParser(sys.argv[1:] if argv is None else argv, __params__)      # parse the command line
		displayTrace = args['--debug']
		logger.configureLogger(args)                                                   # configure the logger
		options = getYMLOptions(args)                                           # get the options from the yml file
		logger.message("\U0001f918 CadnaPromise \U0001f918")
		method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias = parseOptions(options)    # parse the options

		compiler = 'g++'
		if alias == {}:
			curr_loc = os.path.dirname(os.path.realpath(__file__))

			cachePath = "/cache"
			if os.path.exists(curr_loc + cachePath):
				if os.path.isfile(curr_loc + cachePath + '/.CXX.txt'):
					with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
						compiler = file.read()
	
					if compiler != 'g++' and compiler is not None:
						alias = {'--alias':compiler}

		logger.message("Using the compiler: {}".format(compiler))
		PrFile.setCustom(typeCustom)
		compileErrorPath = join(path, 'compileErrors') if args['--debug'] else None
		tempPath = join(path, 'debug') if args['--debug'] else None

		# run with timing
		with Timing() as timing:
			# create Promise object
			pr = Promise(path, files, run, nbDigits, compileLines, parsing=not args['--noParsing'], alias=alias)

			# display general infos
			logger.info("We are working with %d file%s and %d different types" %
			            (pr.nbFiles, ('' if pr.nbFiles < 2 else 's'), pr.nbVariables))
			logger.info(pr.expectation())

			# debug the files
			if args['--debug']:
				pr.exportParsedFiles(tempPath)

			# get the cadna reference
			highest = types['q'] if 'q' in method else types['d']
			pr.changeSameType(highest)
			logger.step("Get a reference result with Cadna (%s)" % highest)
			pr.compileAndRun(tempPath, cadna=True)
			
			if args['--pause']:
				pause()

			# try with the highest precision
			logger.step("Check with highest format (%s)" % typeNames[method[-1]])
			pr.changeSameType(types[method[-1]])
			
			if not pr.compileAndRun(tempPath):
				pr.changeSameType(highest)
				raise PromiseError("You should lower your expectation, it doesn't work with " + typeNames[method[-1]])
			
			if args['--pause']:
				pause()

			# do the Delta-Debug passes ('s','d' and then 'h','s' when method is 'hsd' for example)
			for lo, hi in reversed(list(zip(method, method[1:]))):
				logger.step("Delta-Debug %s/%s" % (typeNames[lo], typeNames[hi]))
				res = pr.runDeltaDebug(types[lo], types[hi], tempPath, args['--pause'], compileErrorPath)
				# stop if the DeltaDebug is not successful
				if not res:
					break

		# export the output
		if argv is None:
			pr.exportFinalResult(outputPath)


	except PromiseError as e:
		logger.error(e, exc_info=displayTrace)


	else:
		if timing:
			# display the number of each type
			count = Counter(pr.typesDict.values())  # count the nb of each type (result is a dictionary type:nb)
			li = ["%dx %s" % (v, k) for k, v in count.items()]
			logger.message("The final result contains %s.", commaAnd(li))
			logger.debug("Final types:\n" + pr.strResult())

			# display the stats
			logger.message("It tooks %.2fs", timing.timing)
			logger.message("\U0001F449 %d compilations (%d failed) for %.2fs", *pr.compilations)
			logger.message("\U0001F449 %d executions   (%d failed) for %.2fs", *pr.executions)

			logger.reset()
			return pr.setPerType()

	# reset the handlers, in case of running runPromise several times (otherwise, the log files are still open)
	logger.reset()




def runPromise_custom_test(argv=None):
	"""This function is registered (in setup.py) as an entry_point
	argv is used for the unit tests"""

	print("**** start")
	# reset the logger and get a new instance
	logger = PrLogger()
	displayTrace = False

	print("****1. argv:", argv)
	
	# types handle by Promise
	typeNames = {'h': 'Half', 's': 'Single', 'd': 'Double', 'q': 'Quad'}
	types = {'h': 'half_float::half', 's': 'float', 'd': 'double', 'q': 'float128'}

	print("*****sys.argv:", sys.argv)
	try:
		# get the options from command line and yml file
		args = customArgParser(sys.argv[1:] if argv is None else argv, __params__)      # parse the command line
		# print("****2. args:", args)

		displayTrace = args['--debug']
		# print("****3. displayTrace:", displayTrace)

		logger.configureLogger(args)                                                   # configure the logger
		options = getYMLOptions(args)                                           # get the options from the yml file

		# print("****4. options:", options)
		logger.message(r"\U0001f918 CadnaPromise \U0001f918")
		method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias = parseOptions(options)    # parse the options

		# print("****5. method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias:")
		# print(method, path, files, run, nbDigits, compileLines, outputPath, typeCustom, alias)

		PrFile.setCustom(typeCustom)
		compileErrorPath = join(path, 'compileErrors') if args['--debug'] else None
		tempPath = join(path, 'debug') if args['--debug'] else None


		
		# run with timing
		with Timing() as timing:
			# create Promise object
			pr = Promise(path, files, run, nbDigits, compileLines, parsing=not args['--noParsing'], alias=alias)

			# display general infos
			logger.info("We are working with %d file%s and %d different types" %
			            (pr.nbFiles, ('' if pr.nbFiles < 2 else 's'), pr.nbVariables))
			
			logger.info(pr.expectation())

			# debug the files
			if args['--debug']:
				pr.exportParsedFiles(tempPath)


			# print("**** test - tempPath ", tempPath)
			# get the cadna reference
			highest = types['q'] if 'q' in method else types['d']

			# print("***5. highest:", highest)
			pr.changeSameType(highest)
			logger.step("Get a reference result with Cadna (%s)" % highest)

			pr.compileAndRun(tempPath, cadna=True)
			if args['--pause']:
				pause()

			# try with the highest precision
			logger.step("Check with highest format (%s)" % typeNames[method[-1]])
			pr.changeSameType(types[method[-1]])
			
			if not pr.compileAndRun(tempPath):
				pr.changeSameType(highest)
				raise PromiseError("You should lower your expectation, it doesn't work with " + typeNames[method[-1]])
			
			if args['--pause']:
				pause()

			# do the Delta-Debug passes ('s','d' and then 'h','s' when method is 'hsd' for example)
			for lo, hi in reversed(list(zip(method, method[1:]))):
				logger.step("Delta-Debug %s/%s" % (typeNames[lo], typeNames[hi]))
				res = pr.runDeltaDebug(types[lo], types[hi], tempPath, args['--pause'], compileErrorPath)
				# stop if the DeltaDebug is not successful
				if not res:
					break

		# export the output
		if argv is None:
			pr.exportFinalResult(outputPath)


	except PromiseError as e:
		logger.error(e, exc_info=displayTrace)


	else:
		if timing:
			# display the number of each type
			count = Counter(pr.typesDict.values())  # count the nb of each type (result is a dictionary type:nb)
			li = ["%dx %s" % (v, k) for k, v in count.items()]
			logger.message(r"The final result contains %s.", commaAnd(li))
			logger.debug(r"Final types:\n" + pr.strResult())

			# display the stats
			logger.message(r"It tooks %.2fs", timing.timing)
			logger.message(r"\U0001F449 %d compilations (%d failed) for %.2fs", *pr.compilations)
			logger.message(r"\U0001F449 %d executions   (%d failed) for %.2fs", *pr.executions)

			logger.reset()
			return pr.setPerType()

	# reset the handlers, in case of running runPromise several times (otherwise, the log files are still open)
	logger.reset()




if __name__ == "__main__":
	runPromise()



