# imports
import ga
import numpy as np
import matplotlib.pyplot as plt
# 
n_pop=100
x_range_l=-5.12
x_range_r=5.12
poplength=15
iteration=10000
crossrate=0.1
selectrate=0.25
variationrate=0.001

# 
pop=ga.initpop(n_pop,x_range_l,x_range_r)
pop_first=pop

x=np.arange(0,iteration)
mxfit=[]
mnfit=[]
mefit=[]
mfit=[]
# print(x)

for t in range(iteration):
    fit=ga.fitness(pop)
    selected_pop=ga.select(fit,pop,selectrate)
    binpop=ga.coding(selected_pop,poplength,x_range_l)
    kidspop=ga.crossover(binpop,len(pop),crossrate)
    kidspop=ga.variation(kidspop,variationrate)
    splited_pop=ga.encoding(kidspop,poplength,x_range_l)
    newpop=np.append(pop,splited_pop,axis=1)
    pop=ga.merge(newpop,n_pop)
    maxfit=np.max(fit)
    minfit=np.min(fit)
    meanfit=np.average(fit)
    mxfit.append(maxfit)
    mnfit.append(minfit)
    mefit.append(meanfit)
    mfit.append(max(mxfit))
    # print(maxfit,minfit,meanfit)

plt.plot(x,mxfit,'r-',x,mnfit,'g-',x,mefit,'b-',mfit,'k-')
plt.show()
# print(pop)