"""Crawl the cdc index and return and return all entries"""
import scrapy


class ParasiteIndexSpider(scrapy.Spider):
    """The spider class to scrape the web."""
    name = "index"
    start_urls = [
        "https://www.cdc.gov/dpdx/az.html"
    ]

    def parse(self, response):
        """Parsing function of the Spider."""
        # Loop through all <ul class="bullet-list">
        for entry in response.css("div.row .bullet-list li"):
            text = "".join(entry.css("::text").getall()).strip()  # Get all text and clean up
            title = f"{text}"

            # Extract the link (if available)
            link = entry.css("a::attr(href)").get()

            # Check if it contains a parasite (based on <em>)
            is_parasite = bool(entry.css("em").get())

            yield {
                "title": title,
                "link": link,
                "is_parasite": is_parasite,
            }

