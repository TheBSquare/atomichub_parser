import asyncio
import binascii
import json
import time
from datetime import timedelta, datetime
import requests
import os
import eosiopy
from eosiopy import RawinputParams, EosioParams

from database import Db


if __name__ == '__main__':

    transaction = {
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
        "expiration": (datetime.now() - timedelta(hours=2, minutes=59)).strftime("%Y-%m-%dT%H:%M:%S.%f"),
        "ref_block_num": None,
        "ref_block_prefix": None
    }
    db = Db()
    token = db.create_connection()

    ti = time.time()

    data = requests.post('').json()
    ref_block_num = data['last_irreversible_block_num']
    chain_id = data['chain_id']
    print(chain_id, ref_block_num)
    data = requests.post('',
                         data=json.dumps({"block_num_or_id": ref_block_num})).json()
    ref_block_prefix = data['ref_block_prefix']
    print(data['block_num'])
    """
    print(time.time()-ti)
    ti = time.time()
    
    transaction['ref_block_num'] = ref_block_num
    transaction['ref_block_prefix'] = ref_block_prefix
    transaction['actions'][0]['data'] = get_action_data(24094889, token)

    transaction = str(transaction).replace("'", '"')

    os.system(f"cleos --url https://wax.greymass.com sign -k {private_key} -c {chain_id} -p '{transaction}'")
    print(time.time()-ti)"""
