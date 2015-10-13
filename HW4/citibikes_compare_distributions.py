#Because jupyter doesn't install in Bertin Computers and I'm running out of time
#___author___=Alan
import pylab as pl
import pandas as pd
import numpy as np
#%pylab inline

import os

#this makes my plots pretty! but it is totally not mandatory to do it
import seaborn as sns


# Load September 2014 data in Pandas dataframe
import requests, zipfile, StringIO
r = requests.get('https://s3.amazonaws.com/tripdata/201409-citibike-tripdata.zip')
z = zipfile.ZipFile(StringIO.StringIO(r.content))
df = pd.read_csv(z.open('201409-citibike-tripdata.csv'))

print df.columns


#df is the dataframe where the content of the csv file is stored
df['birth year'] = df['birth year'].convert_objects(convert_numeric=True)
df['ageM'] = 2015 - df['birth year'][(df['usertype'] == 'Subscriber') & (df['gender'] == 1)]
df['ageF'] = 2015 - df['birth year'][(df['usertype'] == 'Subscriber') & (df['gender'] == 2)]
df.head()


bins = np.arange(10, 99, 10)
df.ageM.groupby(pd.cut(df.ageM, bins)).agg([count_nonzero]).plot(kind='bar')
df.ageF.groupby(pd.cut(df.ageF, bins)).agg([count_nonzero]).plot(kind='bar')



#print df.ageS, df.ageS.cumsum()

csM=df.ageM.groupby(pd.cut(df.ageM, bins)).agg([count_nonzero]).cumsum()

csF=df.ageF.groupby(pd.cut(df.ageF, bins)).agg([count_nonzero]).cumsum()

print np.abs(csM / csM.max()-csF / csF.max())

pl.plot(bins[:-1] + 5, csM / csM.max(), label = "M")
pl.plot(bins[:-1] + 5, csF / csF.max(), label = "F")
pl.legend()


import scipy.stats
ks=scipy.stats.ks_2samp(df.ageM[~np.isnan(df.ageM)], df.ageF[~np.isnan(df.ageF)])
print ks


#here is the critical values tablel. Have you chosen your significance level yet?? you should do it first thing!
#from IPython.display import Image
#Image(filename="ksample.png")

#Sigificance level was chosen at 0.05 and the p-value (0.0) < 0.05. 
#Therefore, I can reject the null hypothesis that the two samples are pulled 
#from the same underlying distribution.


# Find the max absolute value distance between the two CDFs
diffs = np.abs(csM / csM.max()-csF / csF.max())

# Calculate critical value for sig. level 0.05
# http://www.real-statistics.com/statistics-tables/kolmogorov-smirnov-table/
nM = np.count_nonzero(~np.isnan(df.ageM))
nF = np.count_nonzero(~np.isnan(df.ageF))

crit_val = 1.36*sqrt((nM+nF)/(nM*nF))

print 'statistic ', round(nanmax(diffs),4) , ' > critical value', crit_val
print 'Women and men do not appear to be drawn from the same distribution'
# Note: it seems very easy to reject the null hypothesis with this this test
#    given large sample sizes



#please perform the Pearson's test and tell me what you find

# Set NaNs to 0 for ages not represented in each partition of the data set
csM[np.isnan(csM)] = 0
csF[np.isnan(csF)] = 0

pear = scipy.stats.pearsonr(csM, csF)
print 'Pearson\'s correlation coefficient: ', pear[0]
print 'p-value: ', pear[1]
print
print 'We can reject the null hypothesis that there is no correlation between the two samples.\n'
print 'The very low p-value represents the small probability that uncorrelated systems produced this correlation coeff.'




#please perform the Spearman's test and tell me what you find
# This test does NOT assume that the two samples are normally distributed

spear = scipy.stats.spearmanr(csM, csF)
print 'Spearmman\'s correlation coefficient: ', spear[0]
print 'p-value: ', spear[1]
print
print 'We can reject the null hypothesis that there is no correlation between the two samples.\n'
print 'The very low p-value represents the small probability that uncorrelated systems produced this correlation coeff.'

##NIGHT n DAY

#KS Test

# Convert starttime to datetime data type, then get hour only
df['starttime2'] = pd.to_datetime(df['starttime'])
df['starthour'] = [start.hour for start in df['starttime2']]
print df['starthour'].head()
#print df['starthour'].describe(



# Split the data by morning (5am-11am) and night (5pm-12am) riders, keeping same restrictions on Subscribers only
df['ageAM'] = 2015-df['birth year'][(df['usertype'] == 'Subscriber') & ( df['starthour'] >= 5) & (df['starthour'] <= 11)]
df['agePM'] = 2015-df['birth year'][(df['usertype'] == 'Subscriber') & (df['starthour'] >= 17) ]





# Plot histograms
bins = np.arange(0, 99, 5)
df.ageAM.groupby(pd.cut(df.ageAM, bins)).agg([count_nonzero]).plot(kind='bar')
df.agePM.groupby(pd.cut(df.agePM, bins)).agg([count_nonzero]).plot(kind='bar')




# Calculate CDFs and plot
csAM=df.ageAM.groupby(pd.cut(df.ageAM, bins)).agg([count_nonzero]).cumsum()
csPM=df.agePM.groupby(pd.cut(df.agePM, bins)).agg([count_nonzero]).cumsum()

pl.plot(bins[:-1] + 5, csAM / csAM.max(), label = "AM")
pl.plot(bins[:-1] + 5, csPM / csPM.max(), label = "PM")
pl.legend()




# Perform KS test
ks=scipy.stats.ks_2samp(df.ageAM[~np.isnan(df.ageAM)], df.agePM[~np.isnan(df.agePM)])
print ks

print 'AM riders and PM riders do not appear to be drawn from the same distribution'




#Pearson's Test of Correlation

# Set NaNs to 0 for ages not represented in each partition of the data set
csAM[np.isnan(csAM)] = 0
csPM[np.isnan(csPM)] = 0


pear = scipy.stats.pearsonr(csAM, csPM)
print 'Pearson\'s correlation coefficient: ', pear[0]
print 'p-value: ', pear[1]
print
print 'We can reject the null hypothesis that there is no correlation between the two samples.\n'
print 'The very low p-value represents the small probability that uncorrelated systems produced this correlation coeff.'




#Spearman's Test of correlation:


# This test does NOT assume that the two samples are normally distributed

spear = scipy.stats.spearmanr(csAM, csPM)
print 'Spearmman\'s correlation coefficient: ', spear[0]
print 'p-value: ', spear[1]
print
print 'We can reject the null hypothesis that there is no correlation between the two samples.\n'
print 'The very low p-value represents the small probability that uncorrelated systems produced this correlation coeff.'


