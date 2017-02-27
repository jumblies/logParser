# Work log Parser
# Geoff Lamke, MD
# USROC patient logs
# Written for python 3.6.  Not tested on Python 2.7

import re
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
logname = askopenfilename() # show an "Open" dialog box and return the path to the selected file

#logname = input("Enter the Filename:") Not used b/c of TK

#open log file
log = open(logname, "r")
outfile = open("outfile.txt", "w+")
processed = open(str(logname[:-4])+"_invoice.txt", "w+")
finalReport=0
prelimReport=0

for line in log:
    studyRE = r"(STUDY:)([a-zA-Z]+\S [a-zA-Z]+)"
    studyMatch = re.search(studyRE, line)
    if studyMatch:
        #print(studyMatch.start(), studyMatch.end()) #not using index posn
        #print(studyMatch.group())
        #print("\r\n")
        outfile.write(studyMatch.group())
        outfile.write("\r\n")
    if "Prelim report" in line:
        prelimReport += 1
        outfile.write(line.strip()+ " ")
    if "Final report" in line:
        finalReport +=1
        outfile.write(line.strip() + " ")
    # studyCT = r"(CT\s[A-Z]+\S)"       abandoned attempt at regex matching of ct type
    # ctMatch = re.search(studyCT, line)
    # if ctMatch:
    #     print(ctMatch.group())
### Print Finals
processed.write(str(finalReport) + " Final Reports"+ "\r\n" )

### Print Prelims
processed.write(str(prelimReport) + " Prelim Reports"+ "\r\n" )
# Close files

log.close()
outfile.close()

# Reopen file for reading
processFile = open("outfile.txt", "r")

# Set final initial counters to zero
mriFinal, ctHeadFinal, ctAbdFinal, crFinal, usFinal, ctChestFinal = 0, 0, 0, 0, 0, 0
# Set prelim initial counters to zero
mriPrelim, ctHeadPrelim, ctAbdPrelim, crPrelim, usPrelim, ctChestPrelim = 0, 0, 0, 0, 0, 0

prelim, final=0,0

finalExceptions = []
prelimExceptions = []
for line in processFile:
    if "[Final report]" in line:
        final +=1
        if "MRI" in line:
            mriFinal += 1
        elif "CT ABDOMEN" in line or "CTA ABDOMEN" in line:
            ctAbdFinal += 1
        elif "CT CHEST" in line or "CTA CHEST" in line:
            ctChestFinal += 1
        elif "CT HEAD" in line:
            ctHeadFinal += 1
        elif "CR " in line:
            crFinal += 1
        elif "US " in line:
            usFinal += 1
        else:
            finalExceptions.append(line)
# Close file in preparation for  prelim pass
processFile.close()

# Reopen file for reading
processFile = open("outfile.txt", "r")
for line in processFile:
    if "[Prelim report]" in line and not "[Final reort]" in line:
        prelim +=1
        #print(line)
        if "MRI" in line:
            mriPrelim += 1
        elif "CT ABDOMEN" in line or "CTA ABDOMEN" in line:
            ctAbdPrelim += 1
        elif "CT CHEST" in line or "CTA CHEST" in line:
            ctChestPrelim += 1
        elif "CT HEAD" in line:
            ctHeadPrelim += 1
        elif "CR " in line:
            crPrelim += 1
        elif "US " in line:
            usPrelim += 1
        else:
            prelimExceptions.append(line)
processFile.close()
#print(prelimExceptions)
finalMiscCT = 0      # Set exception counters
prelimMiscCT = 0
unhandledFinal = []  # open lists for unhandled exceptions
unhandledPrelim= []
for item in finalExceptions:
    #print(item)
    if "STUDY:CT" in item:
        #print("found it")
        finalMiscCT +=1
    else:
        unhandledFinal.append(item)

for item in prelimExceptions:
    #print(item)
    if "STUDY:CT" in item:
        #print("found it")
        prelimMiscCT +=1
    else:
        unhandledPrelim.append(item)


processed.write("\r\n" + "**************Final Reports**************"+ "\r\n" )
processed.write("MRI Final Reports " + str(mriFinal) + "*33 = $" + str(mriFinal * 33)+ "\r\n" )
processed.write("CT Abd Final Reports " + str(ctAbdFinal) + "*28 = $" + str(ctAbdFinal * 28)+ "\r\n" )
processed.write("CT Chest Final Reports "+ str(ctChestFinal)+ "*25 = $"+ str(ctChestFinal*25)+ "\r\n" )
processed.write("CT Head Final Reports " + str(ctHeadFinal) + "*20 = $" + str(ctHeadFinal * 20)+ "\r\n" )
processed.write("CR Final Reports " + str(crFinal) + "*10 = $" + str(crFinal * 10)+ "\r\n" )
processed.write("US Final Reports "+ str(usFinal)+ "*20 = $"+ str(usFinal*20)+ "\r\n" )
processed.write("Misc CT Final Reports "+ str(finalMiscCT)+ "*25 = $"+ str(finalMiscCT*25)+ "\r\n" )


processed.write("\r\n" + "**************Final Payment**************"+ "\r\n" )
FinalTotalMoney=(mriFinal*28) + (ctAbdFinal*23) + (ctChestFinal*23) +(ctHeadFinal*17)+(crFinal*8)+(usFinal*17)+(finalMiscCT*25)
processed.write("Total Pay for Final Reports = $" + str(FinalTotalMoney)+ "\r\n\r\n" )

finalTally = mriFinal + ctHeadFinal + ctAbdFinal + crFinal + usFinal+ ctChestFinal + finalMiscCT
print(final, finalTally)
if final == finalTally:
    processed.write("Final Totals Match-No exceptions")
else:
    processed.write("Exceptions!" + "\r\n" )
    for item in unhandledFinal:
        processed.write(item)

processed.write("\r\n" +"**************Prelim Reports**************"+ "\r\n" )
processed.write("MRI Prelim Reports "+ str(mriPrelim)+ "*28 = $"+ str(mriPrelim*28)+ "\r\n")
processed.write("CT Abd Prelim Reports "+ str(ctAbdPrelim)+ "*23 = $"+ str(ctAbdPrelim*23)+ "\r\n" )
processed.write("CT Chest Prelim Reports "+ str(ctChestPrelim)+ "*23 = $"+ str(ctChestPrelim*23)+ "\r\n" )
processed.write("CT Head Prelim Reports "+ str(ctHeadPrelim)+ "*17 = $"+ str(ctHeadPrelim*17)+ "\r\n" )
processed.write("CR Prelim Reports "+ str(crPrelim)+ "*8 = $"+ str(crPrelim*8)+ "\r\n" )
processed.write("US Prelim Reports "+ str(usPrelim)+ "*17 = $"+ str(usPrelim*17)+ "\r\n" )
processed.write("Misc CT Prelim Reports "+ str(prelimMiscCT)+ "*25 = $"+ str(prelimMiscCT*25)+ "\r\n" )
processed.write("\r\n" + "**************Prelim Payment**************"+ "\r\n" )

prelimTotalMoney=(mriPrelim*28) + (ctAbdPrelim*23) + (ctChestPrelim*23) +(ctHeadPrelim*17)+(crPrelim*8)+(usPrelim*17)+(prelimMiscCT*25)
processed.write("Total Pay for Prelim Reports = $" + str(prelimTotalMoney) + "\r\n\r\n" )

prelimTally = mriPrelim + ctHeadPrelim + ctAbdPrelim + crPrelim + usPrelim+ ctChestPrelim + prelimMiscCT
print(prelim, prelimTally)
if prelim == prelimTally:
    processed.write("Prelim Totals Match-No exceptions")
else:
    processed.write("Exceptions!" + "\r\n" )
    for item in unhandledPrelim:
        processed.write(item)
