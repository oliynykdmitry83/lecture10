''' This program loads the csv file of the table of elements which
    was created in the first part of this assignment and uses it
    to plot the atomic radius and number of shells for each element
    '''
import csv
import matplotlib.pyplot as plt
import numpy as np

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
        reader = csv.reader(csvfile, quotechar="'")
        fieldNames=next(reader)     # first row contains headers
    
        for row in reader:          # remaining rows contain table data
            if row[0]:              # some rows only contain empty strings.
                                    # Here we only check first field.
                rowData.append(row) # Append the row to rowData
    return fieldNames, rowData

def columnToList (array, column, varType):  # converts a column of array to a list
                                            # varType can be 'int' or 'float'
    list=[]
    for i in range (len(array)):
        if varType == 'int':
            list.append (int(array[i][column]))
        elif varType == 'float':
            list.append (float(array[i][column]))
        else:
            list.append (array[i][column])
    return list

'''Start of main section'''
myPath = "/Users/dmytro/projects/wc/Lecture10/"

''' Load the cleaned up file into elements array, headers into elementFields'''
elementFields, elements=loadCsvFile(myPath + "elementsRevised.csv")
numElements = len(elements)           # Number of data rows in the list
print ('Number of rows: ', numElements)
print(elementFields)                        # Show the Field names
for i in range(10):                         # Show the first 10 rows
    print(elements[i])
for i in range(numElements-10, numElements):  # Show the last 10 rows
    print(elements[i])

''' Now plot the Atomic Radius and number of shells for each element'''

fig, ax1 = plt.subplots()
                                                # right hand scale from being clipped
#   Create a list from a column of the elements array
xdata = columnToList(elements, 0, 'int')               # column 0 is atomic number
print(xdata)
yRadius = columnToList (elements, 4, 'float')              # column 4 is atomic radius
print (yRadius)
yShell = columnToList (elements, 8, 'float')              # column 8 is number of shells
print (yShell)
color = 'tab:red'
ax1.set_xlabel(elementFields[0])
ax1.set_ylabel(elementFields[4], color=color)
ax1.set_title('Atomic Radius and Shell Number versus Atomic Number')

plot1 = ax1.plot(xdata, yRadius, label=elementFields[4], color = color)    

ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel(elementFields[8], color=color)  # we already handled the x-label with ax1
plot2 = ax2.plot(xdata, yShell, label=elementFields[8], color=color)
ax2.tick_params(axis='y', labelcolor=color)

# Add legends

lns = plot1 + plot2 
# Note: usually the ax.plot does not need a variable to receive the handle of the
# object, but when using two y-axes, only the second one would appear in the legend
# so in this case, we store the legends plot1 and plot 2.  These are used in the 
# labels  command to invoke the get_labels get the labels handles into list labels
# which is then used in the plt.legend command.

labels = [l.get_label() for l in lns]
plt.legend(lns, labels, loc=0)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
