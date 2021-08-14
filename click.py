#-*- coding cp-1252 -*-
import os
import time
from multiprocessing import Lock, Process, cpu_count

#import sys
from bit import Key
from bit.format import bytes_to_wif


def get_babulesy(numpotok, k_count, profit_file, base_file, lock):
        pid = os.getpid()
        lock.acquire()
        print("process PID", pid, numpotok, ' read base...', flush=True)
        start = time.time()
        t = frozenset([line.rstrip('\n') for line in open(base_file, 'r', encoding="cp1252")]) #first we create a list, and then we convert it to a set. The set generator is not used because the script load time increases
        print('time read:',time.time() - start, flush=True)
        del(start)
        lock.release()
        y=0
        print("process PID", pid, numpotok,'start generation...', flush=True)
        while True:
                #key generation unit
                y+=1
                print("process PID", pid, numpotok,'generation ',y, flush=True)
                mass={}
                for _ in range(k_count):
                        k = Key() #kompressed key
                        mass[k.address]=k.to_wif() #address made from compressed key
                        mass[k.segwit_address]=k.to_wif() #segwit address made from compressed key
                        wif = bytes_to_wif(k.to_bytes(), compressed=False) #uncompressed key
                        k1 = Key(wif) #address made from uncompressed key
                        mass[k1.address]=wif

                #verification of addresses
                print("process PID", pid, numpotok,'verification ...', y, flush=True)
                vall_set=set(mass.keys())
                c=vall_set.intersection(t)
                if c:
                        print("process PID", pid, numpotok,'BINGO!!! ...', flush=True)
                        with open(profit_file,'a') as out:
                                for gg in c:
                                        out.write('{},{}\n'.format(gg,mass[gg]))
                                out.close()

if __name__ == '__main__':
        key_count = 50000
        pat=os.path.dirname(__file__)
        baseName=pat+'/base.txt'
        profit=pat+'/out.txt'
        
        lock=Lock()
        
        procs=[]
        for u in range(1): #launch according to the number of cores, if it does not start, it means there is not enough RAM, you need to reduce the number of threads
                proc = Process(target=get_babulesy, args=(u, key_count, profit, baseName, lock))
                procs.append(proc)
                proc.start()
        
        for proc in procs:
                proc.join()