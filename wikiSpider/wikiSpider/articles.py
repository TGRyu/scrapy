from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wikiSpider.items import Article

class ArticleSpider(CrawlSpider):
    name = 'articles'
    allowed_domains = ['wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Benevolent_dictator_for_life']
    rules = [Rule(LinkExtractor(allow='en.wikipedia.org/wiki/((?!:).)*$'), callback='parse_items', follow=True)
             ]
    # rules = [Rule(LinkExtractor(allow=r'.*'), callback='parse_items', follow=True)]

    def parse_items(self, response):
        article = Article();
        article['url'] = response.url
        article['title'] = response.css('h1::text').extract_first()

        text_rule = '//div[@id="mw-content-text"]//text()'
        article['text'] = text = response.xpath(text_rule).extract()

        update_rule = 'li#footer-info-lastmod::text'
        update_delete = 'This page was last edited on '
        lastUpdated = response.css(update_rule).extract_first()
        article['lastUpdated'] = lastUpdated.replace(update_delete, '')

        return article

    # def parse_items(self, response, is_article):
    #     print(response.url)
    #     title = response.css('h1::text').extract_first()
    #     if is_article:
    #         text = response.xpath('//div[@id="mw-content-text"]//text()').extract()
    #         lastUpdated = response.css('li#footer-info-lastmod::text').extract_first()
    #         lastUpdated = lastUpdated.replace('This page was last edited on ', '')
    #         print(f'title is: {title}')
    #         print(f'text is: {text}')
    #         print(f'Last updated: {lastUpdated}')
    #     else:
    #         print(f'This is not an article: {title}')
    #
    #
    # def parse_items(self, response, is_article):
    #     print(response.url)
    #     title = response.css('h1::text').extract_first()
    #     if is_article:
    #         text_rule = '//div[@id="mw-content-text"]//text()'
    #         text = response.xpath(text_rule).extract()
    #
    #         update_rule = 'li#footer-info-lastmod::text'
    #         update_delete = 'This page was last edited on '
    #         lastUpdated = response.css(update_rule).extract_first()
    #         lastUpdated = lastUpdated.replace(update_delete, '')
    #
    #         print(f'title is: {title}')
    #         print(f'text is: {text}')
    #         print(f'Last updated: {lastUpdated}')
    #     else:
    #         print(f'This is not an article: {title}')



