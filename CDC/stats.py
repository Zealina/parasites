"""Count the number of parasites and parasitic diseases"""
#!/usr/bin/env python3

import json
from typing import List


class ParasiteScrapyStats:
    """Relevant Data about the Scraped file"""

    def __init__(self, filename) -> None:
        """Initialize the stats class"""
        self.filename = filename
        self.lib = []
        with open(filename, 'r') as f:
            self.lib = json.load(f)

    def organism_list(self) -> List:
        """Returns a list of organisms"""
        return [organism for organism in self.lib if organism['is_parasite']]

    def disease_list(self) -> List:
        """Return a list of diseases"""
        return [disease for disease in self.lib if not disease['is_parasite']]

    def unique_links(self) -> List:
        """return all the unique links"""
        links = [entry['link'] for entry in self.lib]
        unique_links = sorted(list(set(links)))
        related_to_link = []

        for link in unique_links:
            related = [entry['title'] for entry in self.lib if entry['link'] == link]
            related_to_link.append({link: related})
        return related_to_link

