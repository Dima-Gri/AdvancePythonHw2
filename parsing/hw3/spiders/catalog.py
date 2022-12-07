import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com']

    categories = ['minecraft', 'brawl', 'tank']
    # лучше запускать по очереди, а то отсматривать будет тяжко

    # проходимся по страницам
    def start_requests(self):
        for cat in CatalogSpider.categories:
            for content in range(3): # решил вывесть на трех страницах
                url = f"https://store.steampowered.com/search/?term={cat}&force_infinite=1&&start={content * 50}&count=50"
                yield scrapy.Request(url, callback=self.parse_pages)

    # проходимся по товарам на текущей страницы
    def parse_pages(self, response, **kwargs):
        platforms, prices = [], []
        prices = response.xpath('//div[@class="col search_price_discount_combined responsive_secondrow"]').xpath('@data-price-final').getall()
        prices = list(map(lambda item: int(item)//100, prices))
        for resp in response.xpath('//div[@class="col search_name ellipsis"]').getall():
            string = ''
            if 'platform_img win' in resp:
                string += 'Windows '
            if 'platform_img mac' in resp:
                string += 'MacOs '
            if 'platform_img linux' in resp:
                string += 'linux'
            platforms.append(string.strip())

        for index, href in enumerate(response.xpath('//div[@id="search_resultsRows"]/a').xpath('@href').getall()):
            if index == 100:
                break
            request = scrapy.Request(href, callback=self.parse)

            request.cb_kwargs['value'] = platforms[index]
            request.cb_kwargs['price'] = prices[index]
            yield request

    def parse(self, response, value, price):
        ls = list(map(lambda item: item.strip('\t\r\n '), response.xpath('//div[@class="glance_tags popular_tags"]/a/text()').getall()))
        item = {
            'name': response.xpath('//div[@id="appHubAppName_responsive"]/\text()').get(),
            'path': '->'.join(response.css('div.blockbg a::text').getall()[1::]),
            # 'views': response.css('div.user_reviews_filter_score visible div span b::text').get()
            'date': response.xpath('//div[@class="release_date"]//div[@class="date"]/text()').get(),
            'developer': response.xpath('//div[@id="developers_list"]//a/text()').get(),
            'publisher': response.xpath('//div[@class="dev_row"]//div[@class="summary column"]//a/text()').getall()[1],
            'tags': ls,
            'platform': value,
            'price': price
        }
        if int(response.xpath('//div[@class="release_date"]//div[@class="date"]/text()').get()[-4:]) <= 2000:
            item = None
        yield item

