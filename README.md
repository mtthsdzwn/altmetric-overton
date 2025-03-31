# altmetric-overton
This is a comparison of results from altmetric and overton

Use choosePublications.py to get random data from openAlex. 
this creates a doi.csv which can be used to get data from altmetric, 
and to do a search on overton.io. 
The Altmetric.csv file must be manually saved to csvFiles.

On overton.io, click discover -> search scholarly articles,
you can now enter doi's. 
click export -> generate API call,
copy the link from the browser as the starting point for overton.py

and yes, that url belongs in a config file, some later version will fix that.