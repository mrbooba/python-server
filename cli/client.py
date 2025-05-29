#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def add_event(args):
    payload = {"start": args.start, "stop": args.stop, "tags": args.tags}
    r = requests.post(f"{API_URL}/add_event", json=payload)
    print(r.json())
    
def list_events(args):
    r = requests.get(f"{API_URL}/list_events")
    for event in r.json():
        print(event)

def remove_events(args):
    r = requests.delete(f"{API_URL}/remove_events", params={"tags": args.tags})
    print(r.json())

def main():
    parser = argparse.ArgumentParser(description="Manage events")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add")
    add.add_argument("--start", type=int, required=True)
    add.add_argument("--stop", type=int)
    add.add_argument("--tags", nargs="+", required=True)
    add.set_defaults(func=add_event)
    
    listp = subparsers.add_parser("list")
    listp.set_defaults(func=list_events)

    remove = subparsers.add_parser("remove")
    remove.add_argument("--tags", nargs="+", required=True)
    remove.set_defaults(func=remove_events)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
