import requests
import io
import os
import configparser
import json
import pandas as pd
from src.logger import logging



class NSRDBDataDownloader():
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.sections()
        self.config.read('config.ini')
        self.config["API"]["API_KEY"]
        pass

    def read_json_test(self, file_path):
        logging.info(f"read_json")
        return 1
        # with open(file_path, "r") as f:
        #     return json.load(f)

    def get_nsrdb_data(self, years, locations):
        try:
            # location_years = self.read_json(file_path="location.json")
            print(f"TRY")
            for year in years:
                for location in locations['locations']:
                    querystring = {"wkt": location['long_lat'], "names": year, "utc": self.config["API"]["UTC"], "interval": self.config["API"]["INTERVAL"], "email": self.config["API"]["EMAIL"], "api_key": self.config["API"]["API_KEY"]}
                    # Make API request and get response content as bytes
                    response = requests.get(self.config["API"]["URL"], params=querystring)
                    df = pd.read_csv(io.StringIO(response.text))

                    path = f"{year}_{location['region']}.csv"
                    updated_path = self.config["PATHS"]["UPDATED_PATH"] # read_ini_extra(file_path="config.ini",key = 'UPDATED_PATH')
                    upload_path = self.config["PATHS"]["PATH"] # read_ini_extra(file_path="config.ini",key = 'PATH')
                    upload_path = f"{upload_path}/{location['region']}"
                    # Check whether the specified path exists or not
                    isExist = os.path.exists(upload_path)
                    if not isExist:
                        # Create a new directory because it does not exist
                        os.makedirs(upload_path)
                        upload_path = f"{upload_path}/{path}" 
                        df.to_csv(upload_path, index=False)
                        logging.info(f"The New directory is created! & The file is Uploaded on  {upload_path}")
                    else:
                        upload_path = f"{upload_path}/{path}" 
                        df.to_csv(upload_path, index=False)
                        logging.info(f"The file is uploaded {upload_path}")
            
            return upload_path
        except:
            print(f"EXCEPTION")
            pass


    def update_location_json(years, location):
        pass
        # a = []
        # if not os.path.isfile(fname):
        #     a.append(entry)
        #     with open(fname, mode='w') as f:
        #         f.write(json.dumps(a, indent=2))
        # else:
        #     with open(fname) as feedsjson:
        #         feeds = json.load(feedsjson)

        #     feeds.append(entry)
        #     with open(fname, mode='w') as f:
        #         f.write(json.dumps(feeds, indent=2))