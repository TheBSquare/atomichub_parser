import json

import scrapy

from database import Db


class SaleIdsSpider(scrapy.Spider):
    name = 'sale_ids'
    schema = {
        "code": "atomicmarket",
        "action": "purchasesale",
        "args": {
            "buyer": "ublacksquare",
            "sale_id": None,
            "intended_delphi_median": 0,
            "taker_marketplace": ""
        }
    }
    url = "https://wax.greymass.com/v1/chain/abi_json_to_bin"
    count = 0
    db = Db()

    def start_requests(self):
        for x in range(10):
            point = int(self.start_point) + x
            schema = self.schema
            schema['args']['sale_id'] = point

            token = self.db.create_connection()
            yield scrapy.Request(
                self.url,
                method="POST",
                callback=self.parse,
                body=json.dumps(schema),
                dont_filter=True,
                meta={
                    'point': point,
                    'token': token
                }
            )

    def parse(self, response, **kwargs):
        magic_num = json.loads(response.text)["binargs"][16:]
        num = response.meta['point']
        self.count += 1

        print(f'{self.count}. {num} - {magic_num}')
        self.db.add_magic_num(magic_num, num, response.meta['token'])

        schema = self.schema
        schema['args']['sale_id'] = response.meta['point'] + 10
        yield scrapy.Request(
            self.url,
            method="POST",
            callback=self.parse,
            body=json.dumps(schema),
            dont_filter=True,
            meta={
                'point': response.meta['point'] + 10,
                'token': response.meta['token']
            }
        )
