import pandas as pd
import matplotlib.pyplot as plt
import pygal
import country_converter as coco

# Pre-process data, clean up data for typos / whitespace
df1 = pd.read_csv('data/articleInfo.csv')
df1.fillna(0, inplace=True)
df2 = pd.read_csv('data/authorInfo.csv')
df2.fillna(0, inplace=True)
df2.replace("Denamrk", "Denmark", inplace=True)
df2.replace("Denmark ", "Denmark", inplace=True)
df2.replace("Chian", "China ", inplace=True)
df2.replace("China ", "China", inplace=True)
df2.replace("Chile ", "Chile", inplace=True)
df2.replace("Spain ", "Spain", inplace=True)
df2.replace("Israel ", "Israel", inplace=True)
df2.replace("Bristol", "United Kingdom", inplace=True)

output1 = pd.merge(df1, df2, 
                   on='Article No.', 
                   how='inner')
output1.to_csv('data/output1.csv')

    # 1.1 _______________________________________________
# Get unique list of years aritcles were published
year = output1.iloc[ :, 2]
year = [*set(year)]

yearVsArt = pd.DataFrame(year, columns=['Year'])
numArt = []
for x in year:
    # extract all elements from aritcleInfo = x, get and store size of this array
    numArt.append(len(df1.loc[df1['Year'] == x, ].index))

yearVsArt['NumArticles'] = numArt
yearVsArt.plot(x='Year', y='NumArticles', kind='scatter', title='yearly_publication')
plt.show()

    # 1.2 _______________________________________________
# Creat DF for each year and number of citations per year
yearVsCit = pd.DataFrame(year, columns=['Year'])
numCit = []
for x in year:
    # extract all elements from df1 = x, get size of this array
    numCit.append((df1.loc[df1['Year'] == x, 'Citation']).sum())

yearVsCit['NumCitations'] = numCit
yearVsCit.plot(x='Year', y='NumCitations', kind='scatter', title='yearly_citation')
plt.show()

    # 1.3 _______________________________________________
# Get df of countries and art no, 81 rows
temp = df2.iloc[ : , 2:4]
# temp = temp.drop_duplicates()
# ??????????????????

# Get list of unique countries
countries = df2.iloc[ : , 2]
countries = [*set(countries)]
countries.remove(0) # missing values
countries.remove(' ')
countryPubs = []
for x in countries:
    countryPubs.append(len(temp.loc[temp['Country'] == x, ].index))

pubPerCntry = pd.DataFrame(countries, columns=['Countries'])
pubPerCntry['NumPublications'] = countryPubs

# Convert country names to iso2 code / abrv.
cc = coco.CountryConverter()
pubPerCntry['Countries'] = cc.convert(names=pubPerCntry['Countries'], to = 'ISO2')
pubPerCntry['Countries'] = pubPerCntry['Countries'].str.lower()
wm = pygal.maps.world.World()
wm.title = 'Number of Publications per Country'
i = 0
for x in pubPerCntry['Countries']:
    wm.add(x, {x : pubPerCntry.iloc[i,1]})
    i = i + 1
wm.render_to_file('data/map.svg')

    # 1.4 _______________________________________________
# Get DF of Instituitons their published Aritcles
temp2 = df2[["Author Affiliation", "Article No."]]
# temp2 = temp2.drop_duplicates() -> commented out to fix 3 authors of same aritcle from same country should count 3 times

# Get list of Unique Institutions
institutions = df2["Author Affiliation"]
institutions = [*set(institutions)]
institutions.remove(0)

# Iterate through list of institutions, get list of # of appearences in auhtorinfo, get size of that list
instArti = []
for x in institutions:
    instArti.append(len(temp2.loc[temp2['Author Affiliation'] == x, ].index))

# Create/Organize top 5 institutions dataframe
top5inst = pd.DataFrame(institutions, columns=['Institutions'])
top5inst['NumPublications'] = instArti
top5inst = top5inst.sort_values(by='NumPublications', ascending=False).head(5)
print(top5inst)

    # 1.5 _______________________________________________
# Get DF of Names and H-ind, sort descending, extract top 5
top5hind = df2[["Author Name", "h-index"]]
top5hind = top5hind.sort_values(by="h-index", ascending=False).head(5)
print(top5hind)
