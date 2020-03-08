import numeral_system.positional as nsp
import numpy as np
import msvcrt
import csv

systemBase = 0
symbolsCount = 0

class CustomBreak(Exception):
    pass

def enc(num):
    symbols = nsp.encode(num,systemBase)
    symbols = ''.join(['0' for i in range(symbolsCount - symbols.__len__())]) + symbols
    return symbols

def next(num):
    symbols = nsp.encode(num,systemBase)
    symbols += ''.join(['0' for i in range(symbolsCount - symbols.__len__())])
    return nsp.decode(''.join(sorted(symbols, reverse = True)), systemBase) - nsp.decode(''.join(sorted(symbols)), systemBase)

systemBaseFirst = 4
systemBaseLast = 36 + 1
symbolsCountFirst = 2
symbolsCountLast = 20 + 1



def makeres():
    try:
        for j in range (systemBaseFirst, systemBaseLast):
            for i in range (symbolsCountFirst, symbolsCountLast):
                global systemBase
                global symbolsCount
                systemBase = j
                symbolsCount = i
                lngth = j**i
                currNumber = 0
                loopList = []
                print(systemBase, symbolsCount, lngth, 'to go (', lngth / (j-1), ')', sep = ' ')
                if lngth >= 100000000: #* (j-1):
                    print ("\t\t\t skipping...")
                    continue
    
                if msvcrt.kbhit():
                    raise CustomBreak
    
                step = j-1
                while currNumber < lngth:
                    if next(currNumber) == currNumber:
                        loopList += [currNumber]
                    currNumber += step
            
                with open('Base=%i, Count=%i.txt' %(systemBase, symbolsCount), 'w') as f:
                    for loopNumbers in loopList:
                        f.write(enc(loopNumbers) + '\n')
    except CustomBreak:
        loadres()

def loadres():
    with open('Total.txt', 'w') as fBig:
        systemBaseFirst = 2
        symbolsCountFirst = 2
    
        for j in range (systemBaseFirst-1, systemBaseLast):
            for i in range (symbolsCountFirst-1, symbolsCountLast):
                counter = 0
                systemBase = j
                symbolsCount = i
                try:
                    with open('Base=%i, Count=%i.txt' %(systemBase, symbolsCount), 'r') as f:
                        for line in f:
                            counter += 1
                except IOError:
                    counter = -1
    
                if i == symbolsCountFirst-1 and j >= systemBaseFirst:
                    fBig.write("%i" %j)
                if j == systemBaseFirst-1 and i >= symbolsCountFirst:
                    fBig.write("%i" %i)
                if i >= symbolsCountFirst and j >= systemBaseFirst:
                    if counter == -1: #or counter == 1: #changable
                        fBig.write(" ") 
                        counter = 0
                    else:    
                        fBig.write("%i" %counter)
                if i != symbolsCountLast-1:
                 fBig.write('\t')
            if j != systemBaseLast-1:
                fBig.write('\n')

def initcustomres():
    with open('results.txt', "w") as res:
        
        systemBaseFirst = 2
        symbolsCountFirst = 2
    
        for j in range (2, 11):
            for i in range (2, 7):
                #counter = 0
                systemBase = j
                symbolsCount = i
                res.write('Base=%i, Count=%i\t' %(j, i))
                try:
                    with open('Base=%i, Count=%i.txt' %(j, i), 'r') as f:
                        for line in f:
                            res.write('\t' + line[:-1])

                except IOError:
                    res.write('\t' + 'None')
                res.write("\n")
        

#makeres()
#loadres()
initcustomres()




                    ######################################
                    # Older version with sequence storing#
                    ######################################

#import numeral_system.positional as nsp
#import numpy as np
#import msvcrt

#systemBase = 0
#symbolsCount = 0

#def enc(num):
#	base = systemBase
#	count = sybmolsCount
#	s = nsp.encode(num,base)
#	ss = ''.join(['0' for i in range(count - s.__len__())])
#	return ss+s

#def dcd(str):
#	base = systemBase
#	s = nsp.decode(str, base)
#	return s

#def min(num):
#	return dcd(''.join(sorted(enc(num))))

#def max(num):
#	return dcd(''.join(sorted(enc(num), reverse = True)))

#def next(num):
#	return max(num) - min(num)

#systemBaseFirst = 2
#systemBaseLast = 20 + 1
#symbolsCountFirst = 2
#symbolsCountLast = 20 + 1


#def loadres_older():
#    a = symbolsCountFirst
#    b = symbolsCountLast
#    c = systemBaseFirst
#    d = systemBaseLast
#    fBig = open('Total.txt', 'w')
#    for j in range (systemBaseFirst-1, systemBaseLast):
#    	for i in range (symbolsCountFirst-1, symbolsCountLast):
#    		counter = 0
#    		systemBase = j
#    		sybmolsCount = i
#    		try:
#    			f = open('Base=%i, Count=%i.txt' %(systemBase, sybmolsCount), 'r')
#    			for line in f:
#    				counter += 1
#    			f.close()
#    		except IOError:
#    			print('ohohoh')
#    		if i == a-1 and j >= c:
#    			fBig.write("%i" %j)
#    		if j == c-1 and i >= a:
#    			fBig.write("%i" %i)
#    		if i >= a and j>= c:
#    			fBig.write("%i" %counter)
#    		if i!=b-1:
#    			fBig.write('\t')
    	
#    	if j!=d-1:
#    		fBig.write('\n')
    
#    fBig.close()

#def makeres_older():
#    global systemBase
#    global symbolsCount
#    for j in range (systemBaseFirst, systemBaseLast):
#        for i in range (symbolsCountFirst, symbolsCountLast):
#            systemBase = j
#            sybmolsCount = i
#            loopList = []	
#            if systemBase ** sybmolsCount < 200000:
#                unknownNumbersList = [x for x in range(systemBase ** sybmolsCount)]
#                sequenceList = [[] for x in range(systemBase ** sybmolsCount)]
    
#            curr = unknownNumbersList[0]

#            while len(unknownNumbersList) != 0:
#                unknownNumbersList.remove(curr)
#                afterCurr = next(curr)
    
#                if afterCurr == curr:
#                    loopList += [curr]
#                else:
#                    sequenceList[curr] += [afterCurr]
    
#                if afterCurr in unknownNumbersList:
#                    curr = afterCurr
#                elif len(unknownNumbersList) != 0:
#                    curr = unknownNumbersList[0]

#                f = open('Base=%i, Count=%i.txt' %(systemBase, sybmolsCount), 'w')
#                for tmp in loopList:
#                    f.write(enc(tmp) + '\n')
#                f.close()
