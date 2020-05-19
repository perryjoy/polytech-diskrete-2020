#include <fstream>
#include <iostream>
#include <iomanip>
#include <string>
#include <set>

using namespace std;

typedef unsigned long long int type;

unsigned int CountSetBits(type n)
{
  unsigned int count = 0;
  while (n != 0) 
  {
    n &= (n - 1);
    count++;
  }
  return count;
}

string PrintAsBinary(type x, int len)
{
  string res = (x>>(len-1))&1 ? "1" : "0";
  for (int i = len - 2; i >= 0; i--)
  {
    res += (x >> i) & 1 ? "1" : "0";
  }
  return res;
}

int Eul(int n) 
{
  int result = n;
  for (int i = 2; i*i <= n; ++i)
    if (n % i == 0) 
    {
      while (n % i == 0)
        n /= i;
      result -= result / i;
    }
  if (n > 1)
    result -= result / n;
  return result;
}

type Fact(unsigned int const &n)
{
  type res = 1;
  
  if (n == 0)
    return 1;

  for (unsigned int i = 1; i <= n; i++)
    res *= i;
  return res;
}

type Fact(unsigned int const &n1, unsigned int const &n2)
{
  type res = 1;

  if (n1 == n2)
    return 1;

  for (unsigned int i = n1 + 1; i <= n2; i++)
    res *= i;
  return res;
}

type C(unsigned int const &n, unsigned int const &k)
{
  type res = Fact(n - k, n);
  res /= Fact(k);
  return res;
}

int Pow(int const &a, int const &b)
{
  int res = 1;
  for (int i = 1; i <= b; i++)
    res *= a;
  return res;
}


void check(unsigned int const &N, unsigned int const &L, int &RoundC, int &SymmC, int &PairedC, int &SymmPairedC)
{
  RoundC = 0;
  SymmC = 0;
  PairedC = 0;
  SymmPairedC = 0;


  for (unsigned int i = 1; i <= N; i++)
  {
    if (N % i == 0 && L%i == 0)
    {
      RoundC += Eul(i) * (int)C(N/i, L/i);
    }
  }
  RoundC /= N;

  if (L == N / 2 && N % 2 == 0)
  {
    for (unsigned int i = 2; i <= N; i+=2)
    {
      if (N %  i == 0)
      {
        PairedC += Eul(i) * Pow(2, (N / i));
      }
    }
    PairedC /= N;
  }


  if (L == N / 2 && N % 2 == 0)
  {
    SymmPairedC = Pow(2, L-1);
  }


  
  SymmC = C(L / 2 + (N - L) / 2, L / 2);


}

int calc(int LENGTH, int ONES)
{
  set <type> uniqueOnes;
  set <type> symmetricOnes;
  set <type> selfPairedOnes;
  set <type> symmetriclyPairedOnes;

  int RoundC, SymmC, PairedC, SymmPairedC;

  int *shiftL, *shiftR;

  unsigned long long int code = 0;
  int len = LENGTH;
  int ones_count = ONES;

  string fName = "len = " + to_string(LENGTH) + ", ones = " + to_string(ONES) + ".txt";
  ofstream fout;
  fout.open(fName);
  

  shiftL = new int[len];  // to be shifted left: e.g.      0000 0000 0000 0000 1010 1100 1010 0101 1111 0000
  shiftR = new int[len]; //                                                    ________shR________ ___shL___
                          //                      shR:     0000 0000 0000 0000 1111 1111 1111 1111 0000 0000
                           //                     shL:     0000 0000 0000 0000 0000 0000 0000 0000 1111 1111
  shiftL[0] = 0;
  shiftR[0] = 0xffffffffffffffff >> (64-len);
  for (int i = 1; i < len; i++)
  {
    shiftL[i] = (shiftL[i - 1] << 1) | 1;
    shiftR[i] = shiftR[0] & (~shiftL[i]);
  }

  while (code < ((type)1 << len))
  {
    if (CountSetBits(code) == ones_count)
    {
      for (int shift = 0; shift < len; shift++)
      {
        type testVal = ((code&shiftR[shift]) >> shift) + ((code&shiftL[shift]) << (len - shift));

        if (uniqueOnes.find(testVal) != uniqueOnes.end())
          goto next1;
      }

      uniqueOnes.insert(code);

    next1:
      ;
    }

    code++;
  }


  for (type candidate:uniqueOnes)
  {
    int fittingFlag = 0;
    code = 0;
    for (int i = 0; i < len; i++)
    {
      code += ((candidate & ((type)1 << i)) >> i) << (len - i - 1);
    }
    for (int shift = 0; shift < len; shift++)
    {
      type testVal = ((code&shiftR[shift]) >> shift) + ((code&shiftL[shift]) << (len - shift));

      if (symmetricOnes.find(testVal) != symmetricOnes.end())
        goto next3;

      if (testVal == candidate)
        fittingFlag = 1;
    }
    if (fittingFlag == 1)
      symmetricOnes.insert(code);
  next3:
    ;

    code = ~code;
    fittingFlag = 0;
    for (int shift = 0; shift < len; shift++)
    {
      type testVal = ((code&shiftR[shift]) >> shift) + ((code&shiftL[shift]) << (len - shift));

      if (symmetriclyPairedOnes.find(testVal) != symmetriclyPairedOnes.end())
        goto next4;

      if (testVal == candidate)
        fittingFlag = 1;
    }
    if (fittingFlag == 1)
      symmetriclyPairedOnes.insert(code);
  next4:
    ;


    code = ~candidate;
    fittingFlag = 0;
    for (int shift = 0; shift < len; shift++)
    {
      type testVal = ((code&shiftR[shift]) >> shift) + ((code&shiftL[shift]) << (len - shift));
      
      if (selfPairedOnes.find(testVal) != selfPairedOnes.end())
        goto next2;

      if (testVal == candidate)
        fittingFlag = 1;
    }
    if (fittingFlag == 1)
      selfPairedOnes.insert(code);
  next2:
    ;
  }

  check(LENGTH, ONES, RoundC, SymmC, PairedC, SymmPairedC);

  delete[] shiftL, shiftR;
  fout << "length = " << len << ", ones count = " << ones_count << endl;
  
  fout << endl << "All unique structures:" << endl;
  int k = 1;
  if (RoundC != -1 && RoundC != uniqueOnes.size())
    cout << "!";
  for (auto x : uniqueOnes)
  {
    fout << setw(3) << k << ". " << PrintAsBinary(x, len) << endl;
    k++;
  }

  fout << endl << "All symmetrical structures:" << endl;
  k = 1;
  if (SymmC != -1 && SymmC != symmetricOnes.size())
    cout << "!";
  for (auto x : symmetricOnes)
  {
    fout << setw(3) << k << ". " << PrintAsBinary(x, len) << endl;
    k++;
  }

  fout << endl << "All self-paired structures:" << endl;
  k = 1;
  if (PairedC != -1 && PairedC != selfPairedOnes.size())
    cout << "!";
  for (auto x : selfPairedOnes)
  {
    fout << setw(3) << k << ". " << PrintAsBinary(x, len) << endl;
    k++;
  }
  
  fout << endl << "All self-symmetricly-paired structures:" << endl;
  k = 1;
  if (SymmPairedC != -1 && SymmPairedC != symmetriclyPairedOnes.size())
    cout << "!";
  for (auto x : symmetriclyPairedOnes)
  {
    fout << setw(3) << k << ". " << PrintAsBinary(x, len) << endl;
    k++;
  }

  //cin >> code;
  fout.close();

  return 0;
}

int main(void)
{
  int R, PR, S, PS;
  ofstream f1, f2, f3, f4;
  f1.open("N1.txt");
  f2.open("N2.txt");
  f3.open("N3.txt");
  f4.open("N4.txt");
  
  for (int i = 1; i < 21; i++)
    for (int j = 0; j <= 20/*i*/; j++)
    {
      if (j <= i)
      {
        check(i, j, R, S, PR, PS);
        f1 << R ;
        f2 << S ;
        f3 << PR ;
        f4 << PS ;
        //calc(i, j);
      }
      
      f1 << (j == 20 ? '\n' : '\t');
      f2 << (j == 20 ? '\n' : '\t');
      f3 << (j == 20 ? '\n' : '\t');
      f4 << (j == 20 ? '\n' : '\t');
      
      
    }

  f1.close();
  f2.close();
  f3.close();
  f4.close();
  return 0;
}