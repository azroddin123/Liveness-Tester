from hashlib import new
from matplotlib.font_manager import json_dump
import requests
import json
from nb_utils.file_dir_handling import list_files ## pip install nb_utils
import argparse 
import glob
import os 

parser = argparse.ArgumentParser("Argument for passig folder")
parser.add_argument("--dir_path",type=str,help="pass image folder name to test images",default="/home/azhar/liveness_test/Liveness-Tester/sample")
args = parser.parse_args()

new_path = args.dir_path 
ext_list = ["*.jpg","*.png","*.jpeg"]

image_data = [] 
spoof_result = [] 
real_result  = []
raw_result = [] 

image_data = list_files(new_path, filter_ext=[".png", ".jpg", ".jpeg"])

def call_Api(image) :
    url = "https://live.accurascan.com/upload.php"
    payload={}
    files=[
        # ('photo',('file',open('/home/azhar/liveness_test/11.png','rb'),'image/png')),
      ('photo',(os.path.basename(image),open(image,'rb'),'image/jpg'))
    ]
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload, files=files, verify=False)
    return json.loads(response.text)

for image in image_data :
    api_response  = call_Api(image)
    print(api_response)
    with open("response.json",'a') as f :
        f.write(f"{json.dumps(api_response, sort_keys=True, indent=4)},")
        
    # if api_response["type"] == "success"  and api_response["label"] == "spoof" :
    #     spoof_result.append(api_response)
        
    # elif api_response["type"] == "success"  and api_response["label"] == "real" :
    #     real_result.append(api_response)
    
    # else :
    #     raw_result.append(api_response)
        