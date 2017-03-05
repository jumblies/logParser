import re

log=open("2017-02-26.txt", "r")
out=open("outfile.txt", "w+")

#Define Regex patterns
finalStudyRE= ('^(.*)(\[Final report])')
prelimStudyRE= ('^(.*)(\[Prelim report])')
studyTypeRE = ('(STUDY:.*?\D+)')

for line in log:
    # Define regexes
    finalstudy = re.search(finalStudyRE, line)
    prelimstudy = re.search(prelimStudyRE, line)
    studyType = re.search(studyTypeRE, line)
    if finalstudy:
        out.write(str(finalstudy.group(2))+ " " + str(finalstudy.group(1)))
    if prelimstudy:
        out.write(str(prelimstudy.group(2))+ " " + str(prelimstudy.group(1)))
    if studyType:
        out.write(" " + str(studyType.group()) + "\n")
out.close()
log.close()
# Close files for phase 1
# Create empty lists for phase 2
listofcases =[]
finallist=[]
prelimlist=[]
exceptionlist=[]
# reprocess temp file to reorder pertinent data
out = open("outfile.txt", "r")
processed = open("2017-02-26_invoiceRE.txt", "w+")

def writeInvoiceRE(reportType, listName):    #function to write summary to file
    processed.write(str(reportType) +": " + str(len(listName)) + "\n")


for line in out:
    match = re.search('^(\[.+ report])\s(.*)\sSTUDY:(.*?\D+)', line)
    if match:
        #was writing out to file but now just storing in list
        # processed.write(str(match.group(1)) + str(match.group(3).strip()) + str(match.group(2)))
        listofcases.append((str(match.group(3).strip()) + " " + str(match.group(1).strip()) + " " + str(match.group(2).strip())))
listofcases.sort()

reportString=["Final Reports", "Prelim Reports", "Exceptions"]
listname=[finallist, prelimlist, exceptionlist]

for x in listofcases:
    if "Final report" in x:
        finallist.append(x)
    elif "Prelim report" in x:
        prelimlist.append(x)
    else:
        exceptionlist.append(x)

# These Statements can be replaced by iterable loop just below
# writeInvoiceRE("Final Reports", finallist)
# writeInvoiceRE("Prelim Reports", prelimlist)
# writeInvoiceRE("Exceptions", exceptionlist)

for a,b in zip(reportString,listname):
    writeInvoiceRE(a, b)

# cleanup
out.close()
processed.close()