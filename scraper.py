import glassdoor_scraper as gs 
import pandas as pd

df=gs.get_jobs('data scientist',15,False)