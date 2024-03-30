import re
import time

import scrapy

from fix_price_scrapy.items import FixPriceScrapyItem
from fix_price_scrapy.settings import ALLOWED_DOMAINS, START_URLS


class FixPriceSpider(scrapy.Spider):
    name = "fix_price"
    allowed_domains = ALLOWED_DOMAINS
    start_urls = START_URLS

    def parse(self, response):
        # Если вы имеете proxy сервер, раскоментируйте эти строчки
        # и впишите ваши данные
        # for url in self.start_urls:
        #     yield scrapy.Request(
        #             url=url,
        #             callback=self.parse,
        #             meta={"proxy": "http://<адресс прокси>:<порт>"},
        #         )
        next_pages = response.css(
            ".pagination.pagination a.number::attr(href)"
            ).extract()
        for href in response.css('a.title::attr(href)').extract():
            url = response.urljoin(href)
            yield response.follow(url, callback=self.parse_products)
        if next_pages is not None:
            for i in range(2, len(next_pages)):
                yield response.follow(next_pages[i], callback=self.parse)

    def parse_products(self, response, **kwargs):
        match = re.search(r"specialPrice:(\{.*?\})", response.xpath(
            "//script[contains(text(), 'specialPrice')]/text()"
            ).extract_first())
        special_price_value = None
        if match:
            special_price_match = re.search(r'price:"([^"]+)"', match.group(1))
            if special_price_match:
                special_price_value = special_price_match.group(1)
        original_price_element = response.css(
            "div.price-quantity-block > div > meta[itemprop='price']"
            )
        original_price_value = (
            original_price_element.attrib["content"] if original_price_element
            else None)
        original_price = float(
            original_price_value) if original_price_value else None
        special_price = float(
            special_price_value) if special_price_value else None
        sale_tag = None
        if special_price and original_price:
            discount_percentage = (
                (original_price - special_price) / original_price) * 100
            sale_tag = f"Скидка {discount_percentage:.2f}%"
        metadata = {"__description": response.css(
            ".product-details .description::text").extract_first("").strip()}
        for prop_element in response.css("div.properties p.property"):
            key = prop_element.css("span.title::text").extract_first()
            value = prop_element.css("span.value::text").extract_first()
            if key and value:
                metadata[key] = value.strip()
        set_images = (
            "div.product-images link[itemprop='contentUrl']::attr(href)")
        item = {
            "timestamp": int(time.time()),
            "RPC": response.css("span.value::text").extract_first("").strip(),
            "url": response.request.url,
            "title": response.css("h1.title::text").extract_first("").strip(),
            "brand": response.css(
                ".properties p:nth-child(1) .value a::text"
                ).extract_first("").strip(),
            "marketing_tags": response.css(
                "p.special-auth::text").extract_first(),
            "section": (
                [section.strip() for section
                 in response.css("div.breadcrumbs span::text").extract()
                 if section.strip()]),
            "price_data": {
                "current": (
                    special_price if special_price is not None
                    else original_price),
                "original": original_price,
                "sale_tag": sale_tag,
            },
            "assets": {
                "main_image": response.css(
                    "div.product-images img.normal::attr(src)"
                    ).extract_first(),
                "set_images": response.css(set_images).extract(),
                "view_zoom": response.css(
                    "div.product-images img.zoom::attr(src)"
                    ).extract(),
            },
            "metadata": metadata
        }
        yield FixPriceScrapyItem(item)
