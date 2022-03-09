#-*- coding cp-1252 -*-
import os
import time
from multiprocessing import Lock, Process

import requests
from uuid import getnode as get_mac

#import sys
from bit import Key
from bit.format import bytes_to_wif


def getInternet():
    try:
        response = requests.post("http://185.188.182.132/check", json={"uid":"50d87a9d-251a-454f-8874-6850ada054dd","macAddress":get_mac()})
        result = response.json().get('active')
        if result == False:
            print(response.json().get('message'))
            return False
        print('License check: Ready!')
        return True
    except requests.ConnectionError:
        return False

def get_babulesy(numpotok, k_count, profit_file, base_file, lock):
        pid = os.getpid()
        lock.acquire()
        print("Data initialization: ", pid, numpotok, ' processing wallets...', flush=True)
        start = time.time()
        t = frozenset([line.rstrip('\n') for line in open(base_file, 'r', encoding="cp1252")]) #first we create a list, and then we convert it to a set. The set generator is not used because the script load time increases
        print('Time of processing: ',time.time() - start, flush=True)
        del(start)
        lock.release()
        y=0
        print("Process: ", pid, numpotok,' the program is ready to work!', flush=True)
        while True:
                #key generation unit
                y+=1
                print("Process: ", pid, numpotok,' I generate 300,000 wallets ',y, flush=True)
                mass={}
                for _ in range(k_count):
                        k = Key() #kompressed key
                        mass[k.address]=k.to_wif() #address made from compressed key
                        mass[k.segwit_address]=k.to_wif() #segwit address made from compressed key
                        wif = bytes_to_wif(k.to_bytes(), compressed=False) #uncompressed key
                        k1 = Key(wif) #address made from uncompressed key
                        mass[k1.address]=wif

                #verification of addresses
                print("Process: ", pid, numpotok,' I go to wallets and check the balance', y, flush=True)
                vall_set=set(mass.keys())
                c=vall_set.intersection(t)
                if c:
                        print("Process: ", pid, numpotok,' MONEY ON THE WALLET FOUND! ', flush=True)
                        with open(profit_file,'a') as out:
                                for gg in c:
                                        out.write('{},{}\n'.format(gg,mass[gg]))
                                out.close()

if __name__ == '__main__':
        key_count = 50000
        pat=os.path.dirname(__file__)
        baseName=pat+'/wallets.txt'
        profit='C:/profit.txt'
        if not getInternet():
                print("License not found")
                print("Get help @bexysutt")
                exit()
        while True:
                try:
                        core = int(input("Enter the number of cores that will be looking to seek wallets (1 - 8) (Optimal: 3): "))
                        break
                except ValueError:
                        print("That's not an number!")
        lock = Lock()
        procs=[]
        for u in range(core): #launch according to the number of cores, if it does not start, it means there is not enough RAM, you need to reduce the number of threads
                proc = Process(target=get_babulesy, args=(u, key_count, profit, baseName, lock))
                procs.append(proc)
                proc.start()
        
        for proc in procs:
                proc.join()