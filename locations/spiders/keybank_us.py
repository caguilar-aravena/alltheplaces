from scrapy.spiders import SitemapSpider

from locations.structured_data_spider import StructuredDataSpider
from locations.user_agents import BROWSER_DEFAULT


class KeyBankUSSpider(SitemapSpider, StructuredDataSpider):
    name = "keybank_us"
    item_attributes = {"brand": "KeyBank", "brand_wikidata": "Q1740314"}
    sitemap_urls = ["https://www.key.com/about/seo.sitemap-locator.xml"]
    sitemap_rules = [(r"locations/.*/.*/.*/.*", "parse_sd")]
    time_format = "%H:%M:%S"
    user_agent = BROWSER_DEFAULT

    def post_process_item(self, item, response, ld_data, **kwargs):
        item["name"] = response.css("h1.address__title::text").get()
        item.pop("image")
        item.pop("twitter")
        yield item
