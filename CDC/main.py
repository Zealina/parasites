#!/usr/bin/env python3
"""Main file to test shit"""
from stats import ParasiteScrapyStats
import sys
import json

stats = ParasiteScrapyStats(sys.argv[1])
unique_links = stats.unique_links()

print(f"Total Number of Unique links = {len(unique_links)}:")
print(json.dumps(unique_links, indent=2))

with open("unique_links.json", 'w') as fp:
    json.dump(unique_links, fp, indent=2)
