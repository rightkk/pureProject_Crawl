import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == '__main__':
    print(sys.path)
    process = CrawlerProcess(get_project_settings())
    process.crawl('zhihu.com')
    process.start()
