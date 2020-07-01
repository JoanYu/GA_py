#imports
import numpy as np
import random
from scipy.stats import norm
dim=5
def initpop(n_pop,x_range_l,x_range_r):
    pop=np.zeros((dim,n_pop))
    for i in range(dim):
        for j in range(n_pop):
            pop[i][j]=random.uniform(x_range_l, x_range_r)
    return pop

def fitness(pop):
    fit=np.zeros((pop.shape[1],1))
    for n in range(pop.shape[1]):
        fit[n]=1/(1+func(pop[:,n]))
    return fit

def func(x):
    y=sum(x*x-10*np.cos(2*np.pi*x)+10)
    return y

def select(fit,pop,selectrate):
    sumfit=sum(fit)
    accp=np.zeros((pop.shape[1],1))
    accp[0]=fit[0]/sumfit
    for i in range(1,pop.shape[1]):
        accp[i]=accp[i-1]+fit[i]/sumfit
    matrix=np.zeros_like(accp)
    n_select=round(selectrate*pop.shape[1])
    parent_pop=np.zeros((pop.shape[0],n_select))
    for n in range(round(n_select)):
        parent_pop[:,n]=pop[:,np.where(accp>random.random())[0][0]]
    return parent_pop

def coding(pop,poplength,x_range_l):
    pop=np.around((pop-x_range_l)*10000)
    pop=pop.astype(int)
    merged_pop=[]
    for n in range(pop.shape[1]):
        merge=''
        for k in range(pop.shape[0]):
            addpop=dec2bin(pop[k][n])
            plength=len(addpop)
            addpop='0'*(poplength-plength)+addpop
            merge=merge+addpop
        merged_pop.append(merge)
    return merged_pop

def dec2bin(num):
    binlist=[]
    while(num>0):
        rem=num % 2
        binlist.append(str(rem))
        num=num//2
    binlist=binlist[::-1]
    bin=''.join(binlist)
    return bin

def crossover(merged_pop,n_pop,crossrate):
    sort=[x for x in range(n_pop)]
    random.shuffle(sort)
    kidspop=[]
    for i in range(int(round(n_pop/2))):
        father=merged_pop[sort[i]]
        mother=merged_pop[sort[i+1]]
        if crossrate > random.random():
            crosslocation=int(np.ceil((len(father)-1)*random.random())+1)
            new_mother=mother[crosslocation:]+father[:crosslocation]
            new_father=father[crosslocation:]+mother[:crosslocation]
            kidspop.append(new_father)
            kidspop.append(new_mother)
        else:
            kidspop.append(father)
            kidspop.append(mother)
        i=i+i
    # print(len(kidspop))
    return kidspop

def variation(kidspop,variationrate):
    for n in range(len(kidspop)):
        if variationrate > random.random():
            temp=kidspop[n]
            varlocation=int(np.ceil(len(temp)*random.random()))-1
            temp=temp[:varlocation]+rev(temp[varlocation])+temp[varlocation+1:]
            kidspop[n]=temp
    return kidspop


def rev(str):
    if str=='0':
        revstr='1'
    elif str=='1':
        revstr='0'
    return revstr

def encoding(kidspop,poplength,x_range_l):
    splited_pop=np.zeros((dim,len(kidspop)))
    for n in range(len(kidspop)):
        splited=kidspop[n]
        for k in range(dim):
            bin=str(splited[poplength*k:poplength*(k+1)])
            dec=bin2dec(bin)
            dec=dec/10000.
            # print(dec)
            splited_pop[k,n]=dec
    return splited_pop

def bin2dec(bin):
    return int(bin,2)

def merge(pop,n_pop):
    fit=fitness(pop)
    rank=np.argsort(-fit,axis=0)
    save=np.where(rank>=n_pop)[0]
    newpop=np.delete(pop,save,axis=1)
    return newpop
    


if __name__=="__main__":
    pop=initpop(100,-1,1)
    fit=fitness(pop)
    pop=select(fit,pop,0.5)
    merged_pop=coding(pop,15,-1)
    print(merged_pop)
    kidspop=crossover(merged_pop,50,0.5)
    print(kidspop)
    kidspop=crossover(kidspop,50,0.5)
    print(kidspop)
    kidspop=crossover(kidspop,50,0.5)
    print(kidspop)
    # kidspop=variation(kidspop,0.1)
    # kidspop=encoding(kidspop,15,-1)
    # pop=np.append(pop,kidspop,axis=1)
    # pop=merge(pop,50)