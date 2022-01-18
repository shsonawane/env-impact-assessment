
import pandas as pd
import csv
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import pickle
import seaborn as sns
sns.set()


# In[12]:


features = ['O3','PM10','PM25','NO2','T2M']
train = pd.read_csv('train.csv', parse_dates = ['date'])
train = train.dropna(axis = 0, how = 'any') 
X_train = train[features]
y = train['mortality_rate'].copy()
# In[13]:

model = RandomForestRegressor(n_estimators = 200)
model.fit(X_train, y)

test = pd.read_csv('train.csv', parse_dates = ['date'])
test = test.dropna(axis = 0, how = 'any') 
X_test = train[features]
y_test = train['mortality_rate'].copy()

# In[15]:
pred = model.predict(X_test)
accuracy = model.score(X_test, y_test)
print(accuracy)

filename = 'finalized_model.sav'
pickle.dump(model, open(filename, 'wb'))



# In[16]:


filename = 'finalized_model2.sav'
model = pickle.load(open(filename, 'rb'))

#print(sys.argv(1),sys.argv(2),sys.argv(3),sys.argv(4),sys.argv(5),sys.argv(6))
data = [[22.833,9.614,4.078,7.882,273.262]]
print(round(float(model.predict(data)),3))

# In[21]:


plt.plot(data['mortality_rate']*1000,data['O3'],'ro')
plt.xlabel('Mortality Rate')
plt.ylabel('O3')
plt.show()


plt.plot(data['mortality_rate']*1000,data['NO2'],'bo')
plt.xlabel('Mortality Rate')
plt.ylabel('NO2')
plt.show()

plt.plot(data['mortality_rate']*1000,data['PM10'],'yo')
plt.xlabel('Mortality Rate')
plt.ylabel('PM10')
plt.show()

plt.plot(data['mortality_rate']*1000,data['PM10'],'go')
plt.xlabel('Mortality Rate')
plt.ylabel('PM25')
plt.show()

plt.plot(data['mortality_rate']*1000,data['PM10'],'ko')
plt.xlabel('Mortality Rate')
plt.ylabel('T2M')
plt.show()


# In[26]:


regions = dict((r['Code'],r['Region'])     for r in csv.DictReader(open('regions.csv')))
data['region'].replace(regions, inplace = True)


# In[28]:


def plotbyregion(var):
    byregion = data[['date', 'region', var]] 
    byregion = byregion.pivot(index='date', columns='region', values=var) 
    byregion.plot(figsize=(12,8), alpha=0.6)
    plt.title(var, fontsize=18)
    plt.legend(loc='upper right')
    plt.show()

plotbyregion('mortality_rate')
plotbyregion('O3')
plotbyregion('PM10')
plotbyregion('PM25')
plotbyregion('T2M')
plotbyregion('NO2')

