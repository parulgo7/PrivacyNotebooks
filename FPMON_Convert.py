import pandas as pd

# Splitting our original manual dataset into two rows per website (one row for firefox data and another for chrome data)
df = pd.read_csv('FPMON_Dataset.csv')
company_df = df[['Company', "Industry", "url"]]
firefox_df = df[['% JS Attr. Tracked.1',
       '%' +' FP Features.1', '% Aggr. Features.1', 'Sensitive.1', 'Aggressive.1']]
firefox_df.rename(columns={'% JS Attr. Tracked.1': '% JS Attr. Tracked', '%' +' FP Features.1': '%' + ' FP Features', '% Aggr. Features.1': '% Aggr. Features', 'Sensitive.1': 'Sensitive', 'Aggressive.1': 'Aggressive'}, inplace=True)
firefox_full = pd.concat([company_df, firefox_df], axis=1, join='inner')
firefox_full['Browser']='Firefox'
chrome_full = df[['Company', 'Industry', 'url', '% JS Attr. Tracked', '%' + ' FP Features',
       '% Aggr. Features', 'Sensitive', 'Aggressive']]
chrome_full['Browser']='Chrome'
split_rows_df = pd.concat([chrome_full, firefox_full])
split_rows_df.index = list(range(0,100)) 

# Finding what features are present in the data we collected
features = []
for ind in split_rows_df.index:
       sen_features = (str(split_rows_df.loc[ind, "Sensitive"]).split('\n'))
       for word in sen_features:
              word = word.strip("\r")
              word = word.strip()
              if word not in features:
                    features.append(word)
       agg_features = (str(split_rows_df.loc[ind, "Aggressive"]).split('\n'))
       for word2 in agg_features:
              word2 = word2.strip("\r")
              word2 = word2.strip()
              if word2 not in features:
                   features.append(word2)

# remove empty values
features.remove('nan')
print(features)
print("Number of features: ", len(features))

# Setting up the final data frame
# We made a column for each feature and filled the default values with 0 to represent False
final_df = split_rows_df[['Browser', 'Company', 'Industry', 'url', '% JS Attr. Tracked', '%' + ' FP Features', '% Aggr. Features']]
for feature in features:
    feature_values = [0 for i in range(100)]
    final_df[feature] = feature_values

# Checked through the rows and if a website had a feature we would mark a 1 (True) in our Final_df
# correlating with the website and the broswer. This helps make the data easy to perform machine learning on.
index_counter = 0
for ind in split_rows_df.index:
    sen_features = (str(split_rows_df.loc[ind, "Sensitive"]).split('\n'))
    for word in sen_features:
        word = word.strip("\r")
        word = word.strip()
        final_df.at[index_counter, word]=1
    agg_features = (str(split_rows_df.loc[ind, "Aggressive"]).split('\n'))
    for word2 in agg_features:
        word2 = word2.strip("\r")
        word2 = word2.strip()
        final_df.at[index_counter, word2]=1
    index_counter += 1
# print(final_df)

# Exporting the final_df into a csv file
final_df.to_csv('cleaned_FPMON_Dataset.csv', index=False)




# //////////////////////////////////////////////////////////
# Some notes when we were cleaning **IGNORE-ALREADY FIXED**

# split:
# Build Id CPU class ---> build id and cpu class - done
# product vendor --> just product and just vendor - done
# mobile vendor ---> just mobile and just vendor - done
# mobile platform --> just mobile and just platform - done
# platform mobile ---> platform and mobile - done
# Timezone Platform Mobile Vendor --> split into 4 - done
# 'Mobile Platform Product --> 3 seperate - done
# Timezone product --> split - done
# product build ID --> split into product and build ID - done
# timezone platform -->split into 2 - done
# DoNot Track --> DoNotTrack - done
# Product mobile --. into 2 - done
# remove sensitive - done
# Online Status --> Online status - done
# Content Language --> Content language - no entries found?

# no split but keep note of:
# Device Memory
# browser vendor ---> browser lang and vendor
# Webdriver Geolocation --> split into 2 - done
# List of plugins Battery status --> split into List of plugins and Battery status - done
# Geolocation Connection --> split into 2 - done
# Permissions Connection --> split into 2 - done
# Webdriver Permissions --> split into 2 - done
# Geolocation Product sub --> split into Geolocation and Product sub - done
# Permissions App version --> split into Permissions and App version - done
# Connection Permissions --> split into 2 - done