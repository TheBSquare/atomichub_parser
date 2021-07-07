import json

import scrapy

from database import Db

from sys import stdout


class AssetsSpider(scrapy.Spider):
    name = 'assets'
    db = Db()
    token = db.create_connection()

    def start_requests(self):
        yield scrapy.Request(
            url='https://wax.api.atomicassets.io/atomicassets/v1/assets?'
                f'template_id={self.template}&page=1&limit=1&order=asc&sort=asset_id',
            callback=self.ask_user,
            dont_filter=True
        )

    def ask_user(self, response, **kwargs):
        asset = json.loads(response.text)['data'][0]
        print(f'\n--------------------------\n'
              f'-Title: {asset["name"]}\n'
              f'-Template: {asset["template"]["template_id"]}\n'
              f'-Amount: {asset["template"]["issued_supply"]}\n'
              f'-Parsed_upper: {self.db.get_last_template_mint(self.template, self.token)[0]}\n'
              f'-Parsed_lower: {self.db.get_last_template_mint(self.template, self.token)[1]}\n'
              f'-Parsed_amount: {self.db.get_assets_length(self.template, self.token)}\n'
              f'--------------------------\n')
        if input('Do you really want to parse it?(y-Yes): ').lower() in 'yes':
            yield scrapy.Request(
                url=f'https://wax.api.atomicassets.io/atomicassets/v1/assets?template_id={self.template}'
                    f'&page=1&limit=1000&order=desc&sort=template_mint',
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response, **kwargs):
        data = json.loads(response.text)['data']
        for row in data:
            self.db.add_asset((int(row['asset_id']), self.template, int(row['template_mint']), self.price), self.token)
            stdout.write(f'\rAsset №{row["template_mint"]}')
        self.db.update_connection(self.token)
        if len(data) == 1000:
            yield scrapy.Request(
                url=f'https://wax.api.atomicassets.io/atomicassets/v1/assets?template_id={self.template}'
                    f'&page=1&limit=1000&order=desc&sort=template_mint&upper_bound={data[-1]["asset_id"]}',
                callback=self.parse,
                dont_filter=True
            )
        else:
            print('\nSuccessfully parsed all assets!')
            self.db.close_connection(self.token)
