import scrapy
from html2text import HTML2Text
import json
import os


# Crawl and extraction class
class PageSpider(scrapy.Spider):
    """Page Spider class"""
    name = "page"
    dict_lib = []
    
    # Read links from json file with unique links
    with open(os.getenv("UNIQUE_LINKS"), 'r') as f:
        dict_lib = json.load(f)
    
    start_urls = [f"https://www.cdc.gov{''.join(list(my_dict.keys()))}" for my_dict in dict_lib]

    print(start_urls)

    def parse(self, response):
        """Extract relevant parts of the page"""
        # Extract title
        title = response.css("#content ::text").getall()
        title = "".join(title).strip() if title else "No Title Found"

        # Extract species
        species_string = response.xpath("//div[@class='cdc-textblock']//text()").getall()
        species_string = "".join(species_string)
        species = []
        if species_string:
            # Split the string using closing square braces as delimiters
            species_parts = species_string.split("]")
            species = [s.replace("[", "").strip() for s in species_parts if s.strip()]

        # Extract content
        parasite_biology = response.css("#tabs-1-1").get()
        image_gallery = response.css("#tabs-1-2").get()
        lab_diagnosis = response.css("#tabs-1-3").get()
        resources = response.css("#tabs-1-4").get()
        last_reviewed = response.css("#last-reviewed-date::text").get()

        # convert to Markdown
        parser = HTML2Text()
        parser.ignore_links = False
        parasite_biology_md = parser.handle(parasite_biology) if parasite_biology != None else None
        image_gallery_md = parser.handle(image_gallery) if parasite_biology != None else None
        lab_diagnosis_md = parser.handle(lab_diagnosis) if lab_diagnosis != None else None
        resources_md = parser.handle(resources) if resources != None else None

        # Extract image links
        image_links = []
        for image in response.css(".content .img-fluid"):
            src = image.css("::attr(src)").get()
            if src:
                image_links.append(src)

	# Save to a JSON file, one file per link
        filename = f"{title.replace(' ', '_').replace('/', '_')}.json"
        directory = "scraped_data"
        os.makedirs(directory, exist_ok=True)  # Ensure the directory exists
        filepath = os.path.join(directory, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                    {
                        "url": response.url,
                        "title": title,
                        "species": species,
                        "parasite_biology": parasite_biology_md,
                        "image_gallery": image_gallery_md,
                        "lab_diagnosis": lab_diagnosis_md,
                        "resources": resources_md,
                        "image_links": image_links,
                        "last_reviewed": last_reviewed,
                    },
                f,
                ensure_ascii=False,
                indent=2,
            )

        self.log(f"Saved file {filepath}")
