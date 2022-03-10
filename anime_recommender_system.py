# pip install the necessary libraries
# import file using pandas
import pandas as pd
import numpy as np

df =pd.read_csv('anime_dataset.csv')

# display first 30 rows
if not df.empty:
    print (df.head(30))

s = df["Genres"]
columnVectorS = len(s)

# Getting each Genre
genre_labels = set()
for s in df['Genres'].str.split(',').values:
    genre_labels = genre_labels.union(set(s))

# Converting Set to Dictionary Key
temptD = dict.fromkeys(genre_labels,0)
temptDkeys = temptD.keys()

def getGenreList(genreDictString):
    rtnList = []
    for j in temptDkeys: #only take the key from the key-value pair
        rtnList.append(j)
    return rtnList

genreD = {} #create a dictionary
for i in s:
    for j in getGenreList(i):
        genreD[j] = 0 #use the genre as a key and assign value 0

# We now want to subsitute the Genres column with our standard genreD values. 
# The relevant genres should be set to 1, and the others 0. 

# Add Zero Array as the Value for Every Key in the Dictionary of Genres
zeroArr = np.zeros(columnVectorS).astype(int)

for i in genreD.keys():
    genreD[i] = np.array(zeroArr)

# Create a new Genre Dataframe from the Dictionary of Genres
df2 = pd.DataFrame(genreD)
df2.shape

# Get the Genre Dataframe Columns and Initial Dataframe Columns
colsGenre = df2.columns.tolist()
colsInitial = df.columns.tolist()

# Merge Initial Dataframe with Genre Dataframe
dfMerged = df.join(df2, how='outer')

# Set the Relevant Cells in the Genre Columns to 1
def stringToDictionary(genreString):
    li = list(genreString.split(","))
    return li

for i in range(len(dfMerged)):
    dictStr = dfMerged.loc[i,'Genres']
    for j in stringToDictionary(dictStr):
        dfMerged.loc[i,j] = 1

spaceSize = len(dfMerged)
npArray = np.arange(spaceSize)
numList = npArray.tolist()

# List Similar Titles
# We can define a function that lists twenty similar titles, using the cosine similarity function:

def getSimilarTitles(rowNo,df):
    #gnL = getGenreList( dfMerged.loc[rowNo, ['Genres']].values[0] )
    #print (gnL)
    csIndexL = []
    csResultL = []
    
    # rowNoVec = df.loc[rowNo, 'Fantasy':].values
    rowNoVec = df.iloc[rowNo, 11:]

    for i in range(spaceSize):
        # iVec = df.loc[i, 'Fantasy':].values
        iVec = df.iloc[i, 11:]
        # cosine similarity calculation
        csResultL.append(np.dot(rowNoVec, iVec) / (np.linalg.norm(rowNoVec) * np.linalg.norm(iVec)))
        csIndexL.append(i)
        
    dfResult = pd.DataFrame({"Cosine Similarity": csResultL})
    dfResult = dfResult.sort_values("Cosine Similarity", ascending=False).head(21)
    return dfResult

# Prompt user for ID of Anime
animeID = input('Enter Anime ID:')

dfResult = getSimilarTitles(int(animeID), dfMerged)
indexList = dfResult.index.tolist()

print ("The following are the results - first row is the original title:")
pd.set_option('display.max_colwidth', None)
dfDisplay = dfMerged.loc[indexList, ['Name', 'Score', 'Sypnosis', 'Genres', 'Rating']]
print(dfDisplay)
