from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import re

PI = 3.14159

def createFractionString(numerator,denominator):
    return f"[{numerator},{denominator}]"

def createPowerText(powerText):
    return f"^{powerText}#"

def notEmptyString(x):
    if(x == ""):
        return False
    else:
        return True

def startsWithStar(stringy):
    if(stringy[0] == "*"):
        return True
    else:
        return False


def writeFractionOrAndPowerString(canvasChosen,x,y,expression,font_size=12,power_font_size = 8,margin = 2, orientation="C"):
    # Assume [numerator,denominator]
    # Assume ^power text#
    # Step 1: Break it down to layer heights
    powerOrFractionKeyComponentPattern = r'(\[|\^|\#|\]|\,)'
    parts = re.split(powerOrFractionKeyComponentPattern, expression)
    parts = [realItem for realItem in filter(notEmptyString,parts)]
    fractionLetterCode = [""]
    fractionTextArray = []
    fractionValueArray = []
    fractionBracketNumbers = [""]
    fBValueBracketsImportant = []
    fB = 0
    for part in parts:
        if(part == "["):
            fractionLetterCode.append(fractionLetterCode[-1]+"U")
            fB += 1
            fractionBracketNumbers.append(fractionBracketNumbers[-1]+str(fB))
        elif(part == "]"):
            fractionLetterCode.append(fractionLetterCode[-1][0:-1])
            fractionBracketNumbers.append(fractionBracketNumbers[-1][0:-1])
        elif(part == "," and fractionLetterCode[-1] != ""):
            fractionLetterCode.append(fractionLetterCode[-1][0:-1] + "D")
        elif(part == "^"):
            fractionLetterCode.append("*" + fractionLetterCode[-1])
        elif(part == "#"):
            fractionLetterCode.append(fractionLetterCode[-1][1:])
        else:
            fractionLetterCode.append(fractionLetterCode[-1])
            fractionTextArray.append(fractionLetterCode[-1]) # This is important as this is when we are not switching to/from fraction/power
            fractionValueArray.append(part) # This is the actual text and should align with the code
            fBValueBracketsImportant.append(fractionBracketNumbers[-1])
    fractionLetterCode.pop(0)
    fractionBracketNumbers.pop(0)
    fBVBIArray = []
    fractionHeights = []
    combinedFractionValueArray = []
    previous = ""
    # Flip it so that power fractions will be first
    #print(fractionTextArray)
    """
    for i in range(1,len(fractionTextArray)):
        if(fractionTextArray[i-1] in fractionTextArray[i] and fractionTextArray[i][0]=="*" and len(fractionTextArray[i]) > len(fractionTextArray[i-1])+1):
            temp = fractionTextArray[i-1]
            fractionTextArray[i-1] = fractionTextArray[i]
            fractionTextArray[i] = temp
            temp2 = fractionValueArray[i-1]
            fractionValueArray[i-1] = fractionValueArray[i]
            fractionValueArray[i] = temp2
    """
    #print(fractionTextArray)
    j = 0
    for fTA in fractionTextArray: # Work out the height of each and at the same time create the combine value text Array
        if (fTA == previous or fTA == "*" + previous or "*" + fTA == previous or (fTA[0]=="*" and fTA == previous[:-1] + "D") or (fTA[:-1] == "*" + previous)):
            fractionHeights[-1] += "," + fTA
            previous = fTA
            combinedFractionValueArray[-1] += "," + fractionValueArray[j]
        else:
            fractionHeights.append(fTA)
            previous = fTA
            combinedFractionValueArray.append(fractionValueArray[j])
            fBVBIArray.append(fBValueBracketsImportant[j])
        j += 1
    #print(fractionHeights)
    fractionHeightIntegers = []
    for fH in fractionHeights:
        fHarraySet = [item for item in set(fH.split(","))]
        fHStarNumber = len([item for item in filter(startsWithStar , fHarraySet)])
        fHarraySetLength = len(fHarraySet)
        fractionHeightIntegers.append(fHStarNumber*power_font_size + (fHarraySetLength - (fHStarNumber) )*font_size + (fHarraySetLength+1)*margin)
    #Step 1 complete Remember the fractionHeightIntegers are my layer heights
    #Step 2 Now we should calculate the total height and create a centraal location
    totalHeight = sum(fractionHeightIntegers)
    centalY = totalHeight//2
    #Step 3: Draw the strings

    ###
    x_start=0
    total = 0
    max_line_length = 0
    for i in range(len(fractionHeightIntegers)):
        if(x_start > max_line_length):
            max_line_length = x_start
        x_start = 0
        fractionLineParts = combinedFractionValueArray[i].split(",")
        for j in range(len(fractionLineParts)):
            fLP = fractionLineParts[j]
            #print(fractionTextArray[total],fLP)
            if len(fractionLineParts) > 1:
                if(j>=1 and fractionTextArray[total][-1]!=fractionTextArray[total-1][-1] and fractionTextArray[total][0]=="*"):
                    canvasChosen.drawString(x+x_start,y + fractionTextArray[total].count("*")*power_font_size - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY,fLP)
                    x_start += len(fLP)*font_size/2.2
                elif(j<len(fractionLineParts)-1 and fractionTextArray[total][-1]!=fractionTextArray[total+1][-1] and fractionTextArray[total][0]=="*"):
                    canvasChosen.drawString(x+x_start,y + power_font_size + fractionTextArray[total].count("*")*power_font_size - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY,fLP)
                    canvasChosen.line(x+x_start,y + power_font_size + fractionTextArray[total].count("*")*power_font_size - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY,x+x_start+len(fractionTextArray[total])*font_size/2.2,y + power_font_size + fractionTextArray[total].count("*")*power_font_size - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY)
                else:
                    canvasChosen.drawString(x+x_start,y + fractionTextArray[total].count("*")*power_font_size - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY,fLP)
                    x_start += len(fLP)*font_size/2.2
            else:
                canvasChosen.drawString(x,y - fractionHeightIntegers[i] + margin + sum(fractionHeightIntegers[i:])-centalY,fLP)
                x_start += len(fLP)*font_size/2.2
            total += 1
        if(i>0):
            canvasChosen.line(x,y + sum(fractionHeightIntegers[i:])-centalY,x+100,y + sum(fractionHeightIntegers[i:])-centalY)

    #print(fBVBIArray)
    # Step 4: Brackets
    while(fB > 0):
        fBLayers = []
        for i in range(len(fBVBIArray)):
            if str(fB) in fBVBIArray[i]:
                fBLayers.append(i)
        fBHeight = 0
        for layer in fBLayers:
            fBHeight += fractionHeightIntegers[layer]
        if(len(fBLayers)==0):
            fBLowerHeightOffset = 0
        else:
            fBLowerHeightOffset = -15 -centalY + sum(fractionHeightIntegers[max(fBLayers):])
        canvasChosen.setFontSize(fBHeight)
        canvasChosen.drawString(x-13*len(fBLayers),y + fBLowerHeightOffset,"(")
        canvasChosen.drawString(x+max_line_length+7*len(fBLayers),y + fBLowerHeightOffset,")")
        canvasChosen.setFontSize(font_size)
        fB -= 1
    #Step 100: Return the key info [TOTAL HEIGHT, TOTAL WIDTH] 
    return [totalHeight,max_line_length+7*len(fBLayers)-(x-13*len(fBLayers))]


