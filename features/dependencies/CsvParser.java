import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Collection;
import java.util.List;
import java.io.StringReader;

import edu.stanford.nlp.objectbank.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;

import java.io.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import au.com.bytecode.opencsv.CSVWriter;
import au.com.bytecode.opencsv.CSVReader;

/*

javac -cp "./*" CsvParser.java
java -mx3000m -cp ".:./*" CsvParser srcFilename colIndexStartingAtZero outputFilename

*/

class CsvParser {
    
    public static void main(String[] args) throws Exception {

		@SuppressWarnings("unchecked")	
		
		final String INPUT_FILENAME = args[0];
		final int TEXT_COLUMN_INDEX = Integer.parseInt(args[1]);
		final String OUTPUT_FILENAME = args[2];

		CSVReader csvreader = new CSVReader(new FileReader(INPUT_FILENAME), ',');
		CSVWriter csvwriter = new CSVWriter(new FileWriter(OUTPUT_FILENAME), ',');
		
		LexicalizedParser lp = LexicalizedParser.loadModel("edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz");
		TreebankLanguagePack tlp = new PennTreebankLanguagePack();
		GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();


		boolean headerRow = true;
		System.out.println("beginning parsing");
		
		String [] srcRow;
		while ((srcRow = csvreader.readNext()) != null) {

			// Output row length:
			int rowLength = srcRow.length;

			// Output final index:
			int rowFinalIndex = rowLength - 1;

			// Header row:	    
			if (headerRow == true) {
				String[] header = new String[rowLength+1];
				for (int i=0; i < rowLength; i++) {
					header[i] = srcRow[i];
				} 
				header[rowLength] = "dependencies";		
				csvwriter.writeNext(header);
				headerRow = false;	 
			}
			else {
				// Start building the row:
				String[] row = new String[rowLength+1];
				// Add all the old values:
				for (int i=0; i < rowLength; i++) {
					row[i] = srcRow[i];
				}
				// Get the text to parse:
				String text = srcRow[TEXT_COLUMN_INDEX];	    		    
				
				// Parse the text:
				Tree parse = lp.apply(text);
				GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
				Collection tdl = gs.typedDependenciesCCprocessed(true);

				// Add the dependencies:
				row[rowLength] = tdl.toString();
				// Write the new row:
				csvwriter.writeNext(row);
			}
		}
		csvwriter.close();
	}

}

