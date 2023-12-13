import csv
def loadCsvFile (fileNam):
    ''' Reads a csv file specified as the only argument.
        Uses the reader method from Python csv module.
        Returns two lists:
         1. A list containing the elements of the first row.
            These are assumed to be the headers.
         2. A list containing each remaining row in the csv file.
            Each row is given as a list of all the elements
        This version does not do any error checking'''
    
    fieldNames=[]       # list to hold column headers
    rowData=[]          # List to hold all the data rows in the file
    with open(fileNam, newline='') as csvfile:
        reader = csv.reader(csvfile)
        fieldNames=next(reader)     # first row contains headers
    
        for row in reader:          # remaining rows contain table data
            if row[0]:              # some rows may only contain empty strings.
                                    # Here we only check first field.
                rowData.append(row) # Append the row to rowData
    return fieldNames, rowData

def getColumnOffset (targetHeader, sourceHeader):
    ''' Returns a list of column offsets (starting at zero) of fields
        in the source table to match those required in the target table'''
    
    columnOffsets = []
    for outFldOff in range (len(targetHeader)):     # work through each fieldname in target header
        inFldOff = sourceHeader.index(targetHeader [outFldOff])  # for the name in the target header
                                                                 # find the column offset and apppend
                                                                 # to the colunmOffsets list.
        columnOffsets.append(inFldOff)

    return (columnOffsets)      # return the list of source colunms offsets to be used in target

def buildOutputRow (targetColumns, sourceRow):
    ''' Builds a list with the columns specified in targetColumns using field specified in sourceRow'''
    outRow = []
    for elem in range (len(targetColumns)):
        outRow.append (sourceRow[targetColumns[elem]]) # TargetColumns[elem] contains the field number
                                                    # in the source row of the required data
    return (outRow)

def writeFile (filePath, arrayName):
    # writing the file - don't need csv writer as the array is in the right format

    ''' One of the files contains a list of lists.  The file writing
        utility expects a string.  It's quite tricky to determine whether you
        have a list or a string, because a string is a type of list.  I will
        use a try - except to attempt to append an element to an element of
        the array.  If successful, it is a list and each row will need to be
        unpacked into a string before writing'''
    
    try:
        lstFlg = True
        tst = arrayName[1] + [6]
    except TypeError:
        lstFlg = False
    
    with open(filePath, 'w') as f:
        for i in range(len(arrayName)):
            if lstFlg == False:                         # Wasn't a list, assume it's a string
                arrayLine = arrayName[i]
            else:
                arrayLine = unpackList (arrayName[i])   # It's a list.  Unpack the elements
            f.writelines(arrayLine)
            f.write('\n')       # need newline or you get one long record
        f.close        # meed this to flush the buffer if it's last action in program. (Not sure if needed).

def unpackList (arrayLine):
    '''Converts a list of elements into a string of elements enclosed in apostrophes and comma delinited'''
    mystr= "'{}'".format(arrayLine[0])
    for el in range(1, len(arrayLine)):
        mystr+= " ,'{}'".format(arrayLine[el])
    return mystr
   

'''Start of main section'''
myPath = "/Users/dmytro/projects/wc/Lecture10/"

''' ElementNames is a file containing the atomic number, name and symbol.
    The data is to be accepted as correct and used to fix any errors in the remaining files'''
elementFields, elementName=loadCsvFile(myPath + "ElementNames.csv")

''' Used for diagnostic purposes during development
numElementName = len(elementName)           # Number of data rows in the list
print ('Number of rows: ', numElementName)
print(elementFields)                        # Show the Field names
    
for i in range(10):                         # Show the first 10 rows
    print(elementName[i])
for i in range(numElementName-10, numElementName):  # Show the last 10 rows
    print(elementName[i])
'''

''' Now load the File containing detailed record for first 40 elements'''
El1to40Fields, El1to40Name=loadCsvFile (myPath + "periodicTable1to40.csv")

''' Used for diagnostic purposes during development
numEl1to40Name = len(El1to40Name)
print (El1to40Fields)
print ('Number of rows: ', numEl1to40Name)
for i in range(10):
    print(El1to40Name[i])
for i in range(numEl1to40Name-10,numEl1to40Name ):
    print(El1to40Name[i])
'''

''' Load the File containing detailed record for elements 41 to 88'''
El41to88Fields, El41to88Name=loadCsvFile (myPath + "periodicTable41to88.csv")

''' Used for diagnostic purposes during development
numEl41to88Name = len(El41to88Name)
print(El41to88Fields)

print ('Number of rows: ', numEl41to88Name)
for i in range(10):
    print(El41to88Name[i])
for i in range(numEl41to88Name-10,numEl41to88Name ):
    print(El41to88Name[i])
'''

''' We have to create a csv file of the first 80 elements from the two partial files.  The list of fields
    required (in the order specified) is as follows:
        Atomic Number, Name, Chemical Symbol, Atomic Mass, Atomic Radius,
        Number of Protons, Number of Neutrons, Period, Number of Shells,
        Valence, Metal, Nonmetal, Metalloid.

     The field names for both  input files are the same, but one column has been omitted from the second file.
     The specified field names are not exactly the same as those in the table, so manually match the 
     specified field names to those in the header of the first file.'''

for i in range(len(El1to40Fields)):                     # Printing the list of column names for manually 
    print (f'column: {i}  Name: {El1to40Fields[i]}')    # coding the outputFieldCols.

'''Use this to manually create a list of field names for the required output'''
outputFieldCols = [0, 1, 2, 3, 16, 5, 4, 7, 26, 27, 12, 13, 14]     # If you change this, you should get different output columns
outputFieldNames = []           # Will contain field names for output file
for i in outputFieldCols:       # Now build up the output column header list
    outputFieldNames.append (El1to40Fields[i])
print (outputFieldNames)        # Show the corresponding field names from the input files - check this.

''' Next, build a list of columns required from first file.  This is circular logic.  We went from
    coding the output column numbers manually to generating the column names and now converting 
    them back to numbers. I left it in as a way of checking that I got everything right, but it
    could be left out, using outputFieldCols in place of columnOffsets.  The only thing is that
    you would have to manually code a separate version of outputField columns for the second input file.
'''
columnOffsets = getColumnOffset (outputFieldNames, El1to40Fields)

'''Construct list of rows of data from first input table'''
outData = [outputFieldNames]
for i in range(len(El1to40Name)):
    outputRow = buildOutputRow(columnOffsets, El1to40Name[i])
    outData.append(outputRow)

    '''Build a list of columns required from second file'''
columnOffsets = getColumnOffset (outputFieldNames, El41to88Fields)
#   print (columnOffsets)
'''Append rows of data from second input table'''

for i in range(80 - len(El1to40Name)):  # Only want 80 elements in output
    outputRow = buildOutputRow(columnOffsets, El41to88Name[i])
    outData.append(outputRow)
print (len(outData), ' Records in output file (including the column headers)')

# print (outData)       # For diagnostic purposes only

''' Now correct any names and chemical symbols in outData by matching with 
     rows from elementName.
     if either field is wrong, I report the error and replace both fields - easier than doing them separately
     Produce a CSV file noting all corrections from this operation'''

badNames = ["'AtomicNumber', 'Name', 'Symbol', 'WasName', 'WasSymbol'"]

for elem in range (1,len(outData)): # elementName has number, symbol, name,
                                    # but outData has number, name, symbol
                                    # Note: outData has a header, but elementName does not.
    
    if (outData[elem][1] != elementName[elem-1][2]) | (outData[elem][2] != elementName[elem-1][1]):
      
        namesErr = "'{}', '{}', '{}', '{}', '{}'".format(
            outData[elem][0], elementName[elem-1][2], elementName[elem-1][1], outData[elem][1], outData[elem][2])
        outData[elem][2] = elementName[elem-1][1]
        outData[elem][1] = elementName[elem-1][2]
        badNames.append(namesErr)

''' For diagnostic purposes only, print parts of the file
for i in range(len(badNames)):
    print (badNames[i])
for i in range(len (El1to40Name)):
    print (El1to40Name[i][0], El1to40Name[i][1], El1to40Name[i][2])
for i in range(len (El41to88Name)):
    print (El41to88Name[i][0], El41to88Name[i][1], El41to88Name[i][2])
for i in range(len (outData)):
    print (outData[i][0], outData[i][1], outData[i][2])
'''


'''Now write out the files'''

# write the revised element file 
fileName = myPath + "elementsRevised.csv"
    
writeFile(fileName, outData) 

# Write the file of corrected element names or symbols

fileName = myPath + "correctedNames.csv"
writeFile(fileName, badNames)


print ('End of job')