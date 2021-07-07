import os
import time
from datetime import datetime, timedelta

import scrapy
import json

from database import Db


class MainSpider(scrapy.Spider):
    name = 'main'

    table_url = 'https://wax.greymass.com/v1/chain/get_table_rows'
    info_url = "https://wax.greymass.com/v1/chain/get_info"
    block_url = "https://wax.greymass.com/v1/chain/get_block"

    schema_table = json.dumps({
        "json": True,
        "code": "atomicmarket",
        "scope": "atomicmarket",
        "table": "sales",
        "table_key": "",
        "lower_bound": None,
        "upper_bound": None,
        "index_position": 1,
        "key_type": "",
        "limit": "5",
        "reverse": True,
        "show_player": False
    })
    schema_buy = {
        "actions": [
            {
                "account": "atomicmarket",
                "data": None,
                "name": "purchasesale",
                "authorization": [
                    {
                        "actor": "ublacksquare",
                        "permission": "active"
                    }
                ]
            }
        ],
        "context_free_actions": [],
        "max_net_usage_words": 0,
        "max_cpu_usage_ms": 0,
        "delay_sec": 0,
        "signatures": [],
        "expiration": '',
        "ref_block_num": '',
        "ref_block_prefix": ''
    }

    private_key = "5HxtgwPugnnKDS8kHaxEJ6XutsEXgCFjBke7FX69XE8cP6zV4Su"
    chain_id = "1064487b3cd1a897ce03ae5b6a865651747e2e152090f99c1d19d44e01aea5a4"

    checked = set()
    db = Db()

    def start_requests(self):
        for x in range(15):
            token = self.db.create_connection()
            yield scrapy.Request(
                url=self.table_url,
                method="POST",
                callback=self.parse_tables,
                body=self.schema_table,
                dont_filter=True,
                meta={
                    'token': token
                }
            )
            time.sleep(.05)

        yield scrapy.Request(
            url=self.info_url,
            method="POST",
            callback=self.parse_ref_num,
            dont_filter=True
        )

    def parse_tables(self, response, **kwargs):
        yield scrapy.Request(
            url=self.table_url,
            method="POST",
            callback=self.parse_tables,
            body=self.schema_table,
            dont_filter=True,
            meta={
                'token': response.meta['token']
            }
        )

        data = json.loads(response.text)
        for row in data['rows']:
            if not row['sale_id'] in self.checked:
                self.checked.add(row['sale_id'])
                print(row['sale_id'])

                if 'USD' in row['listing_price'] or row['collection_name'] != 'alien.worlds' or \
                        row['seller'] != 'tmteo.wam':
                    continue

                price = self.db.get_price(row['asset_ids'][0], response.meta['token'])

                if not price is None:
                    print(time.time())
                    self.schema_buy['actions'][0]['data'] = self.get_action_data(row['sale_id'], response.meta['token'])
                    transaction = str(self.schema_buy).replace("'", '"')
                    os.system(f"cleos --url https://wax.greymass.com sign -p "
                              f"-k {self.private_key} "
                              f"-c {self.chain_id} "
                              f"'{transaction}'")
                    print(time.time())

    def parse_ref_num(self, response, **kwargs):
        yield scrapy.Request(
            url=self.block_url,
            method="POST",
            callback=self.parse_ref_prefix,
            body=json.dumps({"block_num_or_id": json.loads(response.text)['last_irreversible_block_num']}),
            dont_filter=True
        )

    def parse_ref_prefix(self, response, **kwargs):
        data = json.loads(response.text)
        self.schema_buy['expiration'] = self.get_transaction_expiration()
        self.schema_buy['ref_block_num'] = data['block_num']
        self.schema_buy['ref_block_prefix'] = data['ref_block_prefix']
        #print(f'Parsing time={self.schema_buy["expiration"]}, '
        #      f'head_block_num={self.schema_buy["ref_block_num"]}, '
        #      f'head_block_prefix={self.schema_buy["ref_block_prefix"]}')

        yield scrapy.Request(
            url=self.info_url,
            method="POST",
            callback=self.parse_ref_num,
            dont_filter=True
        )

    @staticmethod
    def get_transaction_expiration():
        return (datetime.now() - timedelta(hours=2, minutes=59)).strftime("%Y-%m-%dT%H:%M:%S.%f")

    def get_action_data(self, sale_id, token):
        action_part = "a0aed1164364e2d1"
        return ''.join((action_part, self.db.get_magic_num(sale_id, token)))
