baseInName='\\base1.txt'
baseOutName='\\base2.txt'

bsOut=open(baseOutName, 'w')

print('чтение базы...', end='')

with open(baseInName, 'r') as bs:    
        for i in bs.readlines():
            key,val = i.strip().split('\t')    
            if key[0] in ["1","3"]:
                bsOut.write('{}\n'.format(key))
bsOut.close()
bs.close()
print("Ок")
