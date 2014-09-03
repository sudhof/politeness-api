
import sys, os
import csv
import re


DIR = os.path.split(__file__)[0]


class StanfordDependencyParser:

	"""
	python interface to Stanford dependency parser
	basically a wrapper around a command-line call
	so it 'feels' like native python
	"""

	ROOT = DIR
	COMMAND = 'java -mx100m -cp ".:./*" CsvParser $INPUT $COLUMN $OUTPUT'
	DEPENDENCY_RE = re.compile(r"""([a-zA-Z0-9_]+[\(][0-9a-zA-Z\s,-]+[\)])[,\]]""")

	def parse(self, sentences):
		"""
		given list of sentences  ["sentence1", "sentence2"],
		returns a dictionary mapping {sentence: [list of dependencies]}
		"""

		if sentences.__class__.__name__ in ('str', 'unicode'):
			# tagging a single document
			sentences = [sentences]

		# In case we're tagging huge text blobs:
		csv.field_size_limit(sys.maxint)

		# Dummy tmp files:
		input = "tmpinput.csv"
		output = "tmpoutput.csv"
		full_input_path = os.path.join(self.ROOT, input)
		full_output_path = os.path.join(self.ROOT, output)
		input_length = len(sentences)		
		self.__write_csv(sentences, full_input_path)
		
		# Change working directory:
		current_working_dir = os.getcwd()
		os.chdir(self.ROOT)  # switch to jar-favorable directory
		
		# Prepare command:
		command = self.COMMAND
		command = command.replace("$INPUT", input)
		command = command.replace("$OUTPUT", output)
		command = command.replace("$COLUMN", "0")
		print command
		os.system(command)
		
		# Back to previous working dir:
		os.chdir(current_working_dir)
		
		# Read output:
		sentences = self.__read_csv(full_output_path)
		output_length = len(sentences)
		if input_length != output_length:
			print "#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"
			print "ERROR"
			print "\tParsing input length does not match output length. Something when wrong."
			print "\tInput: %d" % input_length
			print "\tOutput: %d" % output_length
			print "ERROR"
			print "#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"
			return False
		return sentences



	def __write_csv(self, documents, path):
		writer = csv.writer(open(path, 'w'))
		header = ["text"]
		writer.writerow(header)
		for doc in documents:
			writer.writerow([doc])


	def __read_csv(self, path):
		documents = {}
		reader = csv.DictReader(open(path, 'rb'))
		for row in reader:
			text = row['text']
			dependencies = row['dependencies']
			# Parse dependencies, from string to list:
			dependencies = self.DEPENDENCY_RE.findall(dependencies)
			documents[text] = dependencies
		return documents



if __name__ == "__main__":

	import time

	# self-contained demo

	sentences = [
		"I am really happy that sheep and cows exist.",
		"Goats are so much cooler than sheep."
	]

	s = time.time()
	parses = StanfordDependencyParser().parse(sentences)
	e = time.time()

	print "Total time: %f secs" % (e-s)



	for sentence in parses:
		print "----------------------------"
		print "> ", sentence
		print "Dependencies: ", parses[sentence]












