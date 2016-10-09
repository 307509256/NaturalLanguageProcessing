#coding:utf-8

productions = {'S':{('A', 'B'),('B', 'C')},'A':{('B', 'A')},'B':{('C','C')},'C':{('A','B')}}
string = ['a','b','a','b','a', 'a']
l = len(string)
table = [[{'-'} for i in range(l)] for i in range(l)]
table[0][0] = {'A','C'}
table[1][1] = {'B'}
table[2][2] = {'A','C'}
table[3][3] = {'B'}
table[4][4] = {'A','C'}
table[5][5] = {'A', 'C'}
def get_entry(i, j):
    global table
    if(table[i][j]!={'-'}):
        return table[i][j]
    table[i][j] = set()
    for k in range(j-i):
        concate = {(p1,p2) for p1 in get_entry(i, i+k) for p2 in get_entry(i+k+1, j)}
        for c in concate:
            for (s1, s2) in productions.iteritems():
                if(c in s2):
                    table[i][j] |= {s1}
    return table[i][j]; 
get_entry(0,l-1)
for i in range(l):
    for j in range(i+1):
        print table[j][l-i+j-1],
    print