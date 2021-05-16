#!/usr/bin/env python3

from datetime import datetime
from pathlib import Path
import json
import sys
import sys

import httpx


class TMPrinter():
    def __init__(self):
        self.max_len = 0

    def out(self, text):
        if len(text) > self.max_len:
            self.max_len = len(text)
        else:
            text += (" " * (self.max_len - len(text)))
        print(text, end='\r')
    def clear(self):
    	print(" " * self.max_len, end="\r")

def doc_hunt(doc_link, tmprinter):

    doc_id = ''.join([x for x in doc_link.split("?")[0].split("/") if len(x) in (33, 44)])
    if doc_id:
        print(f"\nDocument ID : {doc_id}\n")
    else:
        exit("\nDocument ID not found.\nPlease make sure you have something that looks like this in your link :\1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")


    headers = {"X-Origin": "https://drive.google.com"}
    client = httpx.Client(headers=headers)

    url = f"https://clients6.google.com/drive/v2beta/files/{doc_id}?fields=alternateLink%2CcopyRequiresWriterPermission%2CcreatedDate%2Cdescription%2CdriveId%2CfileSize%2CiconLink%2Cid%2Clabels(starred%2C%20trashed)%2ClastViewedByMeDate%2CmodifiedDate%2Cshared%2CteamDriveId%2CuserPermission(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cpermissions(id%2Cname%2CemailAddress%2Cdomain%2Crole%2CadditionalRoles%2CphotoLink%2Ctype%2CwithLink)%2Cparents(id)%2Ccapabilities(canMoveItemWithinDrive%2CcanMoveItemOutOfDrive%2CcanMoveItemOutOfTeamDrive%2CcanAddChildren%2CcanEdit%2CcanDownload%2CcanComment%2CcanMoveChildrenWithinDrive%2CcanRename%2CcanRemoveChildren%2CcanMoveItemIntoTeamDrive)%2Ckind&supportsTeamDrives=true&enforceSingleParent=true&key=AIzaSyC1eQ1xj69IdTMeii5r7brs3R90eck-m7k"

    retries = 100
    for retry in range(retries):
        req = client.get(url)
        if "File not found" in req.text:
            exit("[-] This file does not exist or is not public")
        elif "rateLimitExceeded" in req.text:
            tmprinter.out(f"[-] Rate-limit detected, retrying... {retry+1}/{retries}")
            continue
        else:
            break
    else:
        tmprinter.clear()
        exit("[-] Rate-limit exceeded. Try again later.")

    tmprinter.clear()

    data = json.loads(req.text)
    # Extracting informations

    # Dates

    created_date = datetime.strptime(data["createdDate"], '%Y-%m-%dT%H:%M:%S.%fz')
    modified_date = datetime.strptime(data["modifiedDate"], '%Y-%m-%dT%H:%M:%S.%fz')

    print(f"[+] Creation date : {created_date.strftime('%Y/%m/%d %H:%M:%S')} (UTC)")
    print(f"[+] Last edit date : {modified_date.strftime('%Y/%m/%d %H:%M:%S')} (UTC)")

    # Permissions

    user_permissions = []
    if data["userPermission"]:
        if data["userPermission"]["id"] == "me":
            user_permissions.append(data["userPermission"]["role"])
            if "additionalRoles" in data["userPermission"]:
                user_permissions += data["userPermission"]["additionalRoles"]

    public_permissions = []
    owner = None
    for permission in data["permissions"]:
        if permission["id"] in ["anyoneWithLink", "anyone"]:
            public_permissions.append(permission["role"])
            if "additionalRoles" in data["permissions"]:
                public_permissions += permission["additionalRoles"]
        elif permission["role"] == "owner":
            owner = permission

    print("\nPublic permissions :")
    for permission in public_permissions:
        print(f"- {permission}")

    if public_permissions != user_permissions:
        print("[+] You have special permissions :")
        for permission in user_permissions:
            print(f"- {permission}")

    if owner:
        print("\n[+] Owner found !\n")
        print(f"Name : {owner['name']}")
        print(f"Email : {owner['emailAddress']}")
        print(f"Google ID : {owner['id']}")

def main():

    print('Twitter : @MalfratsInd')
    print('Github : https://github.com/Malfrats/xeuledoc')

    if len(sys.argv)>1:
        tmprinter = TMPrinter()
        doc_hunt(sys.argv[1], tmprinter)
    else:
        exit("Please give the link to a Google resource.\nExample : xeuledoc https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")

if __name__ == '__main__':
    main()