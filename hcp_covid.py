#!/usr/bin/env python3

# Wrapper that uploads files.
# Uploads the files to selected bucket on the HCP.
# Lists files in covid-wgs diretory.

import glob
import argparse
import os
import json
import sys
from NGPinterface.hcp import HCPManager

##############################################
# List files that will be uploaded on the HCP.
def files(args):
    file_lst = glob.glob(args.path)
    return file_lst


# Upload files and json to selected bucket on HCP.
def upload_fastq(args, files_pg, hcpm):
    # List and upload files provided by path flag.
    if args.path:
        for file_pg in files_pg:
            hcpm.upload_file(file_pg, "covid-wgs/"+os.path.basename(file_pg))
            print(f"uploading: {file_pg}")

    if args.filepath:
        # Uploads single file.
        hcpm.upload_file(f"{args.filepath}",
                            "covid-wgs/"+os.path.basename(args.filepath))


def search(args,hcpm):
    lst = hcpm.search_objects(args.query)
    for i in lst:
        if args.query and args.download:
            return lst
        if args.query and not args.download:
            print(i.key)
    

def download_fastq(args,hcpm,file_lst):
    if args.key and args.download:
        # Downloads file.
        obj = hcpm.get_object(f"{args.key}")
        hcpm.download_file(obj, f"{args.output}/"+os.path.basename(args.key))

    if args.query and args.download:
        # Downloads several files specified by query.
        for i in file_lst:
            obj = hcpm.get_object(i.key)
            hcpm.download_file(obj, f"{args.output}/"+os.path.basename(i.key))


def listfiles(hcpm):
    lst = hcpm.search_objects("covid-wgs")
    for i in lst:
        print(i.key)


def arg():
    parser = argparse.ArgumentParser(prog="hci_covid.py")
    requiredNamed = parser.add_argument_group('required arguments')
    requiredUpload = parser.add_argument_group('additional required arguments for upload or download')

    requiredNamed.add_argument("-ep", "--endpoint",
                            help="endpoint url")
    requiredNamed.add_argument("-aki", "--aws_access_key_id",
                            help="aws access key id")
    requiredNamed.add_argument("-sak", "--aws_secret_access_key",
                            help="aws secret access key")
    requiredNamed.add_argument("-b", "--bucket",
                            help="bucket name")
    requiredUpload.add_argument("-p", "--path",
                            action='store',
                            help="path to directory with files for upload")
    requiredUpload.add_argument("-f", "--filepath",
                            help="path to single file")
    requiredUpload.add_argument("-l", "--listfiles",
                            action="store_true",
                            help="list existing files")
    requiredUpload.add_argument("-d", "--download",
                            action="store_true",
                            help="Download files, -k for single file, -q for files found using query")
    requiredUpload.add_argument("-q", "--query",
                            help="search for files on HCP")
    requiredUpload.add_argument("-o", "--output",
                            help="outputpath for downloaded file")
    requiredUpload.add_argument("-k", "--key",
                            help="filepath on HCP (key) for file to download")

    args = parser.parse_args()

    return args


def main():
    args = arg()

    # Connect to HCP
    hcpm = HCPManager(args.endpoint, args.aws_access_key_id, args.aws_secret_access_key)
    hcpm.attach_bucket(args.bucket)

    if args.query:
        file_lst = search(args,hcpm)

    if args.listfiles:
        listfiles(hcpm)

    if args.path:
        files_pg = files(args)
        upload_fastq(args, files_pg, hcpm)

    if args.filepath:
        files_pg = []
        upload_fastq(args, files_pg,hcpm)
    
    if args.download:
        download_fastq(args, hcpm, file_lst)


if __name__ == "__main__":
    main()
