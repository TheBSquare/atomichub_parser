
BOT_NAME = 'nfts'

SPIDER_MODULES = ['nfts.spiders']
NEWSPIDER_MODULE = 'nfts.spiders'

LOG_LEVEL = "ERROR"

ROBOTSTXT_OBEY = False

REACTOR_THREADPOOL_MAXSIZE = 128
CONCURRENT_REQUESTS = 256
CONCURRENT_REQUESTS_PER_DOMAIN = 256
CONCURRENT_REQUESTS_PER_IP = 256

DOWNLOADER_MIDDLEWARES = {
    'nfts.middlewares.NftsDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
}
"""
ROTATED_PROXY_ENABLED = False

HTTP_PROXIES = [
    'http://nothhing:80',
]"""
