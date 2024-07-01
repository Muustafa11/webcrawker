import scrapy
from urllib.parse import urljoin

class AmazonSpider(scrapy.Spider):
    name = "amazonspider"
    counter = 0  # Initialize a counter for ID

    def start_requests(self):
        keyword = "Men polo shirts"
        amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
        yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': 1})

    def parse_search_results(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword']

        search_products = response.css("div.s-result-item")
        for product in search_products:
            relative_url = product.css(".puis-card-container .s-product-image-container a.a-link-normal.s-no-outline::attr(href)").get()
            if relative_url:
                brand_name = product.css('h2.a-size-mini.s-line-clamp-1 span.a-size-base-plus.a-color-base::text').get()
                brief = product.css('h2.a-size-mini.a-spacing-none.a-color-base.s-line-clamp-2 span.a-size-base-plus.a-color-base.a-text-normal::text').get()
                product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
                price = product.css('.a-price > .a-offscreen::text').get()
                image_url = product.css('div.s-product-image-container img.s-image::attr(src)').get()

                if all([brand_name, brief, price, product_url, image_url]):
                    self.counter += 1  # Increment counter
                    item_data = {
                        'id': self.counter,
                        'brand_name': brand_name,
                        'brief': brief,
                        'price': price,
                        'product_url': product_url,
                        'image_url': image_url
                    }
                    yield item_data

        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item") and not(contains(@class, "s-pagination-separator"))]/text()'
            ).getall()
            if available_pages:
                last_page = int(available_pages[-1])
                for page_num in range(2, last_page + 1):
                    amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                    yield scrapy.Request(url=amazon_search_url, callback=self.parse_search_results, meta={'keyword': keyword, 'page': page_num})

        next_page_url = response.css('a.s-pagination-item.s-pagination-next::attr(href)').get()
        if next_page_url:
            next_page_url = urljoin('https://www.amazon.com/', next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_search_results, meta=response.meta)
