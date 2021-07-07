import os


db_settings = {
    'name': "nfts",
    'host': 'localhost',
    'nfts_table': 'nfts',
    'username': 'black',
    'password': 'dfsdqe1WF2#'
}

collections = [
    {
        'link': 'https://wax.atomichub.io/market?collection_name=alien.worlds&order=desc&sort=created&symbol=WAX',
        'threads': 2
    },
    {
        'link': 'https://wax.atomichub.io/market?collection_name=novarallywax&order=desc&sort=created&symbol=WAX',
        'threads': 2
    }
]

filters = {
    'wax': {
        'min': 0,
        'max': 10000,
    },
    'usd': {
        'min': 0,
        'max': 10000
    },
    'profit': 5
}

work_path = os.getcwd()

show_browser = True     # True - показывать екран скупщика, False - не показывать

