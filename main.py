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

"""
00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 16  
10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f 32
20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f 48
30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 64
40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f 80
50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f 96 
60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 112
70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f 128
80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f 144
90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f 160
a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af 176
b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf 192
c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf 208
d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df 224
f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff 240
0001 0101 0201 0301 0401 0501 0601 0701 0801 0901 0a01 0b01 0c01 0d01 0e01 0f01 256
1001 1101 1201 1301 1401 1501 1601 1701 1801 1901 1a01 1b01 1c01 1d01 1e01 1f01 272
2001 2101 2201 2301 2401 2501 2601 2701 2801 2901 2a01 2b01 2c01 2d01 2e01 2f01 288
3001 3101 3201 3301 3401 3501 3601 3701 3801 3901 3a01 3b01 3c01 3d01 3e01 3f01 304
4001 4101 4201 4301 4401 4501 4601 4701 4801 4901 4a01 4b01 4c01 4d01 4e01 4f01 320
5001 5101 5201 5301 5401 5501 5601 5701 5801 5901 5a01 5b01 5c01 5d01 5e01 5f01 336
6001 6101 6201 6301 6401 6501 6601 6701 6801 6901 6a01 6b01 6c01 6d01 6e01 6f01 352
7001 7101 7201 7301 7401 7501 7601 7701 7801 7901 7a01 7b01 7c01 7d01 7e01 7f01 368
8001 8101 8201 8301 8401 8501 8601 8701 8801 8901 8a01 8b01 8c01 8d01 8e01 8f01 384
9001 9101 9201 9301 9401 9501 9601 9701 9801 9901 9a01 9b01 9c01 9d01 9e01 9f01 400
a001 a101 a201 a301 a401 a501 a601 a701 a801 a901 aa01 ab01 ac01 ad01 ae01 af01 416
b001 b101 b201 b301 b401 b501 b601 b701 b801 b901 ba01 bb01 bc01 bd01 be01 bf01 432
c001 c101 c201 c301 c401 c501 c601 c701 c801 c901 ca01 cb01 cc01 cd01 ce01 cf01 448
d001 d101 d201 d301 d401 d501 d601 d701 d801 d901 da01 db01 dc01 dd01 de01 df01 464
f001 f101 f201 f301 f401 f501 f601 f701 f801 f901 fa01 fb01 fc01 fd01 fe01 ff01 480
0002 0102 0202 0302 0402 0502 0602 0702 0802 0902 0a02 0b02 0c02 0d02 0e02 0f02 496
"""





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
