
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
    'http://NkKB4DpF:fSP1ApTz@91.199.112.79:53543',
    'http://NkKB4DpF:fSP1ApTz@45.152.116.248:60257',
    'http://NkKB4DpF:fSP1ApTz@109.196.172.62:55955',
    'http://NkKB4DpF:fSP1ApTz@94.154.189.231:45349',
    'http://NkKB4DpF:fSP1ApTz@45.95.28.100:6279',
]"""
