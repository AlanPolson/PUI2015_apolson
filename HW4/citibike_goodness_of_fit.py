import pylab as pl
import pandas as pd
import numpy as np
%pylab inline

import os

#this makes my plots pretty! but it is totally not mandatory to do it
#import json
#s = json.load( open(os.getenv ('PUI2015')+"/fbb_matplotlibrc.json") )
#pl.rcParams.update(s)

#I used seaborn for my graphs 
import seaborn as sns

#i know i will use scipy for the tests
import scipy.stats



df_W=pd.read_csv('201401.csv')
print df_W.columns
df_S=pd.read_csv('201406.csv')
df_S.head()




#df is the dataframe where the content of the csv file is stored
df_W['birth year'] = df_W['birth year'].convert_objects(convert_numeric=True)
df_S['birth year'] = df_S['birth year'].convert_objects(convert_numeric=True)
df_W['age'] = 2014 - df_W['birth year'][(df_W['usertype'] == 'Subscriber')]
df_S['age'] = 2014 - df_S['birth year'][(df_S['usertype'] == 'Subscriber')]






bins = np.arange(10, 99, 10)
df_W.age.groupby(pd.cut(df_W.age, bins)).agg([count_nonzero]).plot(kind='bar', title="Winter")
W_age_dist = df_W.age.groupby(pd.cut(df_W.age, bins)).agg([count_nonzero])
df_S.age.groupby(pd.cut(df_S.age, bins)).agg([count_nonzero]).plot(kind='bar', title="Summer")
S_age_dist = df_S.age.groupby(pd.cut(df_S.age, bins)).agg([count_nonzero])







#compare to normal

ksW=scipy.stats.kstest(W_age_dist, 'norm')
ksS=scipy.stats.kstest(S_age_dist, 'norm')
print "winter, normal fit", ksW
print "summer, normal fit", ksS

#compare to poisson 

ksW=scipy.stats.kstest(W_age_dist, 'cauchy')
ksS=scipy.stats.kstest(S_age_dist, 'cauchy')
print "winter, normal fit", ksW
print "summer, normal fit", ksS







ksW=scipy.stats.kstest(W_age_dist, 'gamma', args=(35,))
ksS=scipy.stats.kstest(S_age_dist, 'gamma', args=(35,))

print "winter, normal fit", ksW
print "summer, normal fit", ksS





def mydistribution(size, m0, m1):
    #this is a crazy dumb function, but i am trying to make a point here...
    return (np.empty_like(size)+1) * m0 **2



ksW=scipy.stats.kstest(W_age_dist, mydistribution, args=(35,38))
ksS=scipy.stats.kstest(S_age_dist, mydistribution, args=(35,38))

print "winter, normal fit", ksW
print "summer, normal fit", ksS





#Anderson Test
print W_age_dist.values.transpose()




#Performing 

age_sum = S_age_dist.as_matrix()[:,0]
age_win = W_age_dist.as_matrix()[:,0]

ADS = scipy.stats.anderson(age_sum, dist='norm')
ADW = scipy.stats.anderson(age_win, dist='norm')

print "winter, normal fit", ADW
print "summer, normal fit", ADS





#Pearson Test
dist1 = df_W.age.groupby(pd.cut(df_W.age, bins)).agg([count_nonzero])
dist2 = df_S.age.groupby(pd.cut(df_S.age, bins)).agg([count_nonzero])
W1 = dist1.mean()
S2 = dist2.mean()
std1 = dist1.std()
std2 = dist2.std()
norm1 = (dist1 - W1)/std1
norm2 = (dist2 - S2)/std2
r, pv = scipy.stats.pearsonr(norm1, norm2)
print r, pv