"""
Title: Python Lab Core Challenge
Author: Alan Polson
Object: To Sort Bike Records
and perform a small analysis on the data
File: 2014-07 - Citi Bike trip data.csv
Data: August 17th 2015 - Late :/

Steps:

*Read CSV File
*Take columns:  0  - trip duration
				1  - Start time
				12 - Customer/Subscriber
				14 - Gender
				
*Convert Start times to dates.
*Convert Trip duration to numbers

*Tally Customer/Subscriber Numbers
*Tally Gender Numbers

*=Try to do all these tasks in one pass, since it is a large file.

Output: 

Neglecting dates Plot Start-Stop time as a Histogram in 24 hour bins. Stacked with male and female

Display this plot, along with histograms of Subscriber vs Customer data and male vs female vs unknown data


UPDATE: was forced to make one pass to read the file and another to manipulate it, and yet another to plot it. 
I tried my best by working continuously for the last few days, and have learn loads in the process... but now I can't perfect it. I'm exhausted. Sorry
"""
import pandas as pd
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from datetime import datetime
from matplotlib import dates
#%matplotlib inline

#Reading the file and converting starttime to a date string
print 'Reading the file...'
#dt_parse=lambda x: datetime.strptime(x,'%m/%d/%Y %H:%M:%S')
dt_parse=lambda x: datetime.strptime(x,'%Y-%m-%d %H:%M:%S')

data_iter=pd.read_csv('2014-07 - Citi Bike trip data.csv', usecols=(0,1,12,14), parse_dates=['starttime'], date_parser=dt_parse, iterator=True, chunksize=1000)
jul=pd.concat(data_iter)

print 'Computing mean and tallying genders and customer type'
#finding the mean
m=np.mean(jul['tripduration'],dtype=np.float64)




#gleaning the hour of starttime, which we will distribute among our bins in the histogram
jul['starttime']=(pd.DatetimeIndex(jul['starttime'])).hour

#Tallying the gender and customer ratios
male= female= unknown= cust= subs=0
mst,fst,ust=[],[],[] #mst=male start time

for i in xrange(0,len(jul)):
	if jul['gender'].values[i]==1:
		male+=1
		mst.append(jul['starttime'].values[i])
	elif jul['gender'].values[i]==2:
		female+=1
		fst.append(jul['starttime'].values[i])
	else:
		unknown+=1
		ust.append(jul['starttime'].values[i])
	if jul['usertype'].values[i]=='Customer':
		cust+=1
	else:
		subs+=1

print 'Average Trip Duration = {0:.2f} seconds' .format(m)
print 'Total number of Customers = %d\nTotal Number of Subscribers = %d\nTotal number of Male Users = %d\nTotal\
number of Female users = %d\nTotal Number of Users whose Gender is unknown = %d' %(cust,subs,male,female,unknown)


num_bins1=range(0,25,1)
num_bins2=range(0,25,4)

print 'plotting the histogram'

fig=plt.figure(figsize=(13,7))
fig.gca()
plt.subplots_adjust(wspace=0.5, hspace=0.5)
plt.xticks([],[])
plt.yticks([],[])

#plt.sublots_adjust(wspace=0.5,hspace=0.3,left=0.2,right=0.5,top=0.5, bottom=0.5)
ax1=fig.add_subplot(211)
n1,bins1,arrays1=ax1.hist([mst,fst,ust],num_bins1,histtype='bar',alpha=0.75, stacked=True, color=['blue','pink','grey'], label=['Men','Women','Undeclared'])
#best fit line
x=np.linspace(0.5,23.5,24)
ax1.plot(x,n1[2],'r-')

ax1=fig.add_subplot(211)
n2,bins2=np.histogram(jul['starttime'],num_bins2)
barlist=ax1.bar([0,4,8,12,16,20],n2/4.0, width=4, alpha=0.5)
#had to use a bar, coz after 3 hours of trying, I couldn't figure out how to edit the histogram between bin sorting and publishing
jet=pl.get_cmap('jet',len(barlist))#colours!
for i in range(len(barlist)):
	barlist[i].set_color(jet(i))
for bar in barlist:
	height=bar.get_height()
	ax1.text(bar.get_x()+bar.get_width()/2., 1.05*height, '%d'%int(height),ha='center',va='bottom')

plt.xticks(np.arange(1,25))
plt.xlabel('Hour of the Day')
plt.ylabel('Number of People')
plt.title('Peak Hour for July 2014')
plt.legend(loc='upper right')
ax1.set_xlim(right=25)
ax1.set_ylim(top=max(n1[2]+10000))

ax2=fig.add_subplot(223)

#ax2.add_axes((0.1, 0.2, 0.8, 0.7))
barlist2=ax2.bar([-0.125, 1.0-0.125], [male, female], 0.25)
for bar in barlist2:
	height=bar.get_height()
	ax2.text(bar.get_x()+bar.get_width()/2., 1.05*height, '%d'%int(height),ha='center',va='bottom')
ax2.spines['right'].set_color('none')
ax2.spines['top'].set_color('none')
ax2.xaxis.set_ticks_position('bottom')
ax2.set_xticks([0, 1])
ax2.set_xlim([-0.5, 1.5])
ax2.set_ylim([0, max([male,female])+80000])
ax2.set_xticklabels(['Men', 'Women'])
plt.yticks(xrange(0,max([male,female])+80000,80000))

plt.title("Rides by Men vs Women")

ax3=fig.add_subplot(224)

barlist3=ax3.bar([-0.125, 1.0-0.125], [cust, subs], 0.25)
for bar in barlist3:
	height=bar.get_height()
	ax3.text(bar.get_x()+bar.get_width()/2., 1.05*height, '%d'%int(height),ha='center',va='bottom')
ax3.spines['right'].set_color('none')
ax3.spines['top'].set_color('none')
ax3.xaxis.set_ticks_position('bottom')
ax3.set_xticks([0, 1])
ax3.set_xlim([-0.5, 1.5])
ax3.set_ylim([0, max([cust,subs])+80000])
ax3.set_xticklabels(['Customers', 'Subscribers'])
plt.yticks(xrange(0,max([cust,subs])+80000,80000))

plt.title("Rides by Customers vs Subscribers")

plt.show()


