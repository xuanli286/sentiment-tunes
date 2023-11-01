# sentiment-tunes
 
## Install

```shell script
pip install -r requirements.txt
```
## Update the datasets
Download the respective datasets (too big to upload to GitHub) from google drive and add them to the "recommendation_dataset" folder.

1. Emotions / GEMS labelling : able to upload to GitHub and routing has been updated already.
2. Main dataset : 200K_dataset.csv, 200K_features.csv

Things to change in "generate_playlist.py" :

1. For main dataset -- line 208 :
change the routing from the 600K sets to the 200K sets
'''
main_df = pd.read_csv('recommendation_dataset/600k_reco_dataset.csv')
feature_df = pd.read_csv('recommendation_dataset/600k_reco_features.csv')

to 

main_df = pd.read_csv('recommendation_dataset/200K_dataset.csv')
feature_df = pd.read_csv('recommendation_dataset/200k_features.csv')
'''

## Running 
running on localhost:
```shell script
streamlit run main.py
```

## Reference
https://docs.streamlit.io/library/cheatsheet