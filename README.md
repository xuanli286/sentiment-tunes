# sentiment-tunes
 
## Install

```shell script
pip install -r requirements.txt
```
## Update the datasets
Download the respective datasets (too big to upload to GitHub) from google drive and add them to the "recommendation_dataset" folder.

1. Emotions / GEMS labelling : @Jess @Steph
2. Main dataset : 200K_dataset.csv, 200K_features.csv

Things to change in "generate_playlist.py" :

1. For emotions -- line 205 :
'''
change the routing to the emotions dataset @Jess @Steph
'''
2. For main dataset -- line 208 :
'''
change the routing from the 600K sets to the 200K sets
'''

## Running 
running on localhost:
```shell script
streamlit run main.py
```

## Reference
https://docs.streamlit.io/library/cheatsheet