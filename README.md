# LinkedIn Data Retriever

### Why
I was building a personal site and wanted to include my LinkedIn
data on the website. LinkedIn allows you to download your personal data but once I
initiated a download I was forced to wait 24 hours to actually receive the data. I
decided to just scrape it myself

#### What this is:
An easy way for you to download **your own** profile data

#### What this is not:
A way for you to download **others'** profile data. Please do not misuse this

### How
In a chrome tab open the developer console `(ctrl+opt+j)`. 
In the Elements tab right click the topmost html element and select
`Edit as HTML`. Copy and paste in a file named `linkedin_profile.html`.

To run the script

```shell script
conda create -n linkedinscrape python=3.6 -f requirements.txt
conda activate linkedinscrape
python scrape_linkedin.py # will output to linkedin_profile.json in the same directory
```