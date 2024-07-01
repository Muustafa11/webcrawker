# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class AmazonPipeline:
    def process_item(self, item, spider):
        return item

class RemoveEmptyFieldsPipeline:
    def process_item(self, item, spider):
        # Check if any field is empty
        if not all(item.values()):
            # If any field is empty, return None to indicate that this item should be dropped
            return None
        else:
            return item
class PriceProcessingPipeline:
    def process_item(self, item, spider):
        if 'price' in item:
            price_string = item['price']
            # Remove the "$" symbol and convert to float
            price_float = float(price_string.replace('$', ''))
            # Update the item with the modified price
            item['price'] = price_float
        return item

class PandasExportPipeline:
    def __init__(self):
        self.df = pd.DataFrame(columns=['brand_name', 'brief', 'price', 'product_url', 'image_url'])

    def process_item(self, item, spider):
        # Check if any field is empty
        if not all(item.values()):
            return None

        # Check the length of the product_url
        if len(item['product_url']) < 50:
            return None

        # Concatenate item to DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([item])], ignore_index=True)
        return item

    def close_spider(self, spider):
        # Drop rows with any empty fields
        self.df_cleaned = self.df.dropna()

        # Convert back to list of dictionaries
        cleaned_data = self.df_cleaned.to_dict('records')

        # Save cleaned data to CSV file
        self.df_cleaned.to_csv('x.csv', index=False)