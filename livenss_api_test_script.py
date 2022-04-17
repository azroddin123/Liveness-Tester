from hashlib import new
from xmlrpc.client import boolean
import json
from nb_utils.file_dir_handling import list_files ## pip install nb_utils
import argparse 
import glob
import os 
from pathlib import Path
import requests
import httpx ## pip install httpx

from psutil import cpu_count
from tqdm.auto import tqdm
from tqdm.contrib.concurrent import process_map, thread_map  # requires tqdm>=4.42.0
from functools import partial

def call_Api(image_rel_filepath, dir_path, api_url, json_result_base_dir, verbose=False) :
    # url = "https://live.accurascan.com/upload.php"
    # api_url = "http://164.52.218.61/upload.php"

    image_abs_path = os.path.join(dir_path, image_rel_filepath) ## abasolute path

    payload={}
    files=[
        # ('photo',('file',open('/home/azhar/liveness_test/11.png','rb'),'image/png')),
      ('photo',(os.path.basename(image_abs_path),open(image_abs_path,'rb'),'image/png'))
    ]
    headers = {}
    # response = requests.request("POST", api_url, headers=headers, data=payload, files=files, verify=False)

    response = httpx.post(api_url, headers=headers, data=payload, files=files, verify=False)

    with open("result.json",'w') as f :
        f.write(json.dumps(response.json(), sort_keys=True, indent=4))
        
    response_text = json.loads(response.text)

    ###
    json_out_file_relpath = Path(image_rel_filepath).with_suffix(".json")
    json_outfile_abspath = os.path.join(
        dir_path, json_result_base_dir, json_out_file_relpath
    )
    os.makedirs(os.path.dirname(json_outfile_abspath), exist_ok=True)

    with open(json_outfile_abspath,'w') as f :
        f.write(json.dumps(response_text, sort_keys=True, indent=4))
        
    # if api_response["type"] == "success"  and api_response["label"] == "spoof" :
    #     spoof_result.append(api_response)
        
    # elif api_response["type"] == "success"  and api_response["label"] == "real" :
    #     real_result.append(api_response)
    
    # else :
    #     raw_result.append(api_response)

    if verbose:
        print(response_text)
    
    return response_text

def str2bool(v):
    import argparse
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    parser = argparse.ArgumentParser("Argument for passig folder")
    parser.add_argument(
        "--dir_path", type=str,
        help="pass image folder name to test images",
        default="/home/azhar/liveness_test/Liveness-Tester/sample"
    )
    parser.add_argument(
        "--json_result_base_dir", type=str, default="json_response",
        help="folder name to store json respose"
    )
    parser.add_argument(
        "--api_url", type=str, default="http://164.52.218.61/upload.php", 
        help="""API Url to check liveness: Example
        1) http://164.52.218.61/upload.php
        2) https://live.accurascan.com/upload.php
        3) http://127.0.0.1/upload.php -- useful if you have cpp api sdk on local
        """
    )
    parser.add_argument(
        "-w", "--max_workers", type=int, required=False, help="", default=1
    )
    parser.add_argument(
        "-v", "--verbose", type=str2bool, nargs='?', const=True, default=False, help="Message level to display. If verbose True all print messages will be displayed."
    )
    
    args = parser.parse_args()

    print(f"Using api Url: ", args.api_url)

    dir_path = args.dir_path 
    json_result_base_dir = args.json_result_base_dir
    verbose = args.verbose

    lst_image_files = list_files(
        dir_path, filter_ext=[".png", ".jpg", ".jpeg"], 
        return_relative_path=True
    )

    if args.max_workers <= 1:
        for image_rel_filepath in tqdm(lst_image_files) :
            if verbose:
                print(f"image_rel_filepath: ", image_rel_filepath)

            api_response  = call_Api(
                image_rel_filepath, dir_path, args.api_url, 
                json_result_base_dir, verbose
            )
            # print(f"api_response:", api_response)
    else:
        ## multiprocessing
        ## Commenting for now -- as request module is not thread safe
        ## getting null result many times

        # ## TODO : Add alternative modules to make parallel async calls
        # worker = call_Api  # function to map
        # kwargs = {
        #     'dir_path': dir_path,
        #     'api_url': args.api_url,
        # }
        # jobs = lst_image_files  # file_rel_paths

        # result = thread_map(
        #     partial(worker, **kwargs), jobs, 
        #     max_workers=args.max_workers
        # )
        # return result
        print(f"Multithreading not finalized yet... Please run script without --max_workers")

        pass
        
if __name__ == "__main__":
    main()