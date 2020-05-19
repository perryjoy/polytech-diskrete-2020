import numpy as np
import math

def eil(a):
    res = a
    i = 2
    while i*i <= a:
        if a % i == 0:
            while a % i == 0:
                a /= i
            res -= res // i
        i += 1
    if a > 1:
        res -= res//a
    return int(res)

def C(n, k):
    return int(math.factorial(n)/math.factorial(n-k)/math.factorial(k))

#for i in range (1, 20):
#    x = eil (i)
x = math.factorial(0)

len_start = 8
len_end = 11

ones_start = 4

final = np.zeros((len_end+1, len_end+1))
final_sym = np.zeros((len_end+1, len_end+1))


final_t = np.zeros((len_end+1, len_end+1))
final_sym_t = np.zeros((len_end+1, len_end+1))

for chain_len in range(len_start, len_end + 1):
    for ones in range (ones_start, chain_len + 1):

        a = [["0", "1"]]
        for i in range (1,chain_len):
            a += [[]]
        
        for i in range(0, chain_len-1):
            for b in a[i]:
                a[i+1]+=[b+"0"]
                a[i+1]+=[b+"1"]
        
        res = []
        
        
        def onescount(s):
            val = int(s)
            sum = 0
            while val != 0:
                sum += val % 10
                val = val // 10
            return sum
        q = []
        for c in a[chain_len-1]:
            q+=[c]
        for c in q:
            flag = 1
            for i in range (0, chain_len):
                if (c[chain_len-i:]+c[:chain_len-i] in a[chain_len-1]):
                    if flag == 1:
                      res += [c]
                      flag = 0
                    a[chain_len-1].remove(c[chain_len-i:]+c[:chain_len-i])
                  
        
        
        b = []
        for c in res:
            if onescount(c) == ones:
                b+=[c]
        
        bb = []        
        for t in b:
            flag = 0
            for i in range (0, chain_len):
                if flag == 1:
                    continue
                flag = 1
                tt = t[chain_len-i:]+t[:chain_len-i]

                for j in range (1, chain_len // 2 + 1):
                    if tt[j] != tt[-j]:
                        flag = 0
                if flag == 1:
                    bb += [tt]
                    j = chain_len//2
                else:
                    if chain_len % 2 == 0:
                        flag = 1
                        for j in range (1, chain_len // 2 + 1):
                            if tt[j-1] != tt[-j]:
                                flag = 0
                        if flag == 1:
                            bb += [tt]
                            j = chain_len//2

        final[chain_len, ones] = len(b)
        final_sym[chain_len, ones] = len(bb)
        
        for der in range(1, ones + 1):
            if ones % der == 0 and (chain_len-ones) % der == 0:# and der <= chain_len - ones:
                s = eil(der)*(math.factorial(chain_len/der))/(math.factorial(ones/der) * math.factorial((chain_len - ones)/der))
                #testtt += s
                final_t[chain_len, ones] += eil(der)*(math.factorial(chain_len/der))/(math.factorial(ones/der) * math.factorial((chain_len - ones)/der))
        final_t[chain_len, ones] /= chain_len
        
        
        if (chain_len % 2 == 1):
            vert = ones if (ones % 2 == 1) else (chain_len - ones)
            others = (chain_len-vert) / 2
            vert =  (vert-1)/2
            final_sym_t[chain_len, ones] = final_t[chain_len, ones]/2 + C(vert+others, vert)/2
        else:
            if ones % 2 == 0:
                a1 = ones
                b1 = chain_len - ones
                a1 = a1/2 - 1
                b1 = b1/2
                a2 = a1 + 1
                b2 = b1 - 1
                a3 = a1 + 1
                b3 = b1
                final_sym_t[chain_len, ones] = final_t[chain_len, ones]/2 + (C(a1+b1, a1) + C(a3+b3, a3))/4 + (C(a2+b2, a2)/4 if b1 > 0 else 0)
            else:
                final_sym_t[chain_len, ones] = final_t[chain_len, ones]/2 + C((chain_len-2)/2, (ones-1)/2)/2 # not 2chain_len on purpose


for i in range(len_start, len_end + 1):
        final[i,0] = final[i,i]
        final_t[i,0] = final_t[i,i]
        final_sym[i,0] = final_sym[i,i]
        final_sym_t[i,0] = final_sym_t[i,i]
final[0,0] = 1
final_t[0,0] = 1
final_sym[0,0] = 1
final_sym_t[0,0] = 1

#print(final_t[chain_len, ones])
#print(final[chain_len, ones], end = '\n\n\n')
#print (final_t - final, end = '\n\n\n')
print (final_t, end = '\n\n\n')
print (final_sym_t, end = '\n\n\n')
print (final_sym, end = '\n\n\n')
print(2*final_sym_t - final_t, end = '\n\n\n')
print (2*final_sym_t - final_t - final_sym)


#print(b)
#print(bb)
#print(len(b))
#print(len(bb))

#chain_len = 8
#ones = 2
#testtt = 0
#for der in range(1, ones + 1):
#            if ones % der == 0 and (chain_len-ones) % der == 0 and der <= chain_len - ones:
#                s = eil(der)*(math.factorial(chain_len/der))/(math.factorial(ones/der) * math.factorial((chain_len - ones)/der))
#                testtt += s
#                final_t[chain_len, ones] += s
