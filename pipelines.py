from itemadapter import ItemAdapter

class AmazonPipeline:
    def process_item(self, item, spider):
        return item

class RemoveEmptyFieldsPipeline:
    def process_item(self, item, spider):
        if not all(item.values()):
            return None  # Drop item if any field is empty
        else:
            return item

class PriceProcessingPipeline:
    def process_item(self, item, spider):
        if 'price' in item:
            price_string = item['price']
            try:
                price_float = float(price_string.replace('$', '').replace(',', ''))
            except ValueError:
                return None  # Drop item if price conversion fails
            item['price'] = price_float
        return item

class PandasExportPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        if not all(item.values()):
            return None  # Drop item if any field is empty

        if len(item['product_url']) < 50:
            return None  # Drop item if product_url length is less than 50

        item['id'] = len(self.items) + 1
        self.items.append(item)
        return item

    def close_spider(self, spider):
        # No need to save to CSV here, as Scrapy will handle this
        pass
