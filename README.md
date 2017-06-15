sf-to-file
----------
Dump Salesforce CSV export to files.

I inherited a relatively small Salesforce account. Salesforce was more than I needed (especially for the cost), but I didn't want to lose the history in there--especially quotes and contracts stored as documents and/or attachments.

The Salesforce export utility gave me a zip file with all the data in CSV files and documents and attachments in directories names by their identifiers.

I wanted to archive this data in a more organized and readable format. This utility 

+ creates a directory for each account
+ puts each contact and note into a JSON file in the account directory
+ renames attachments back to the original file name and files under account

If some of the other objects are important to you, just follow the pattern to save those as well.

Unzip your export into a directory, then run:

```
python convert.py --source sourcedir --dest destdir
```