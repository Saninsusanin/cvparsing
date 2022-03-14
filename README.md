
## Configure

Set up following evn variable to configure application
```
soon
```

Set up settings in src/settings.py file 

## Run

Convert single pdf file to html file

```
python3 manage.py --runcommand pdf_to_html
```

Convert single html file to ordered text

```
python3 manage.py --runcommand html_to_ordered_sentences
```

Convert all files in directory from pdf to ordered text

```
python3 manage.py --runcommand pdf_to_text_batch
```

Extract features from single pdf file and store them in the .json file line by line

```
python3 manage.py --runcommand get_features_from_pdf
```

Extract features from all pdf files that lays in the data/pdfs and store them in the .json files line by line

```
python3 manage.py --runcommand get_features_from_pdf_batch
```

Plot result of word clusterization algorithm: 

```
python3 manage.py --runcommand plot_words_by_point_grid
```