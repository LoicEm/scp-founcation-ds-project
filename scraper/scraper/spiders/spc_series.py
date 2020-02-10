# -*- coding: utf-8 -*-
import scrapy


class ScpSeriesSpider(scrapy.Spider):
    name = 'scp-series'
    allowed_domains = ['scp-wiki.net']
    start_urls = ['http://scp-wiki.net/scp-series',
                  'http://scp-wiki.net/scp-series-2',
                  'http://scp-wiki.net/scp-series-3',
                  'http://scp-wiki.net/scp-series-4',
                  'http://scp-wiki.net/scp-series-5',
                  'http://scp-wiki.net/scp-series-6',
                  ]

    def parse(self, response):
        for ref in response.\
            xpath('.//div[@class="content-panel standalone series"]/ul')[1:-2].\
            xpath('.//li'):
            name = ref.xpath('./text()').get()
            href = ref.xpath(".//@href").get()
            number = href[5:]
            meta = {
                'name': name,
                'scp_number': number}
            yield response.follow(href, self.parse_article, meta=meta)

    def parse_article(self, response):
        """Parse an SCP page into compnents that will be exploitable from a data standpoint.
        """
        # Structured data
        rating = response.xpath('//span[@class="number prw54353"]//text()').get()
        if rating is not None:
            rating = int(rating)
        scp_class = response.xpath('//strong[starts-with(text(), "Object Class")]').xpath('../text()').get('').strip()
        tags = response.xpath('//div[@class="page-tags"]/span/a/text()').getall()
        # Sections present everywhere
        containment_procedures = response.xpath('//strong[starts-with(text(), "Special Containment Procedures")]').\
            xpath('..//text()').getall()

        # Full text
        full_description = response.xpath('//div[@id="page-content"]//p//text()').getall()
        # Full description will contain redundancies with the containment_procedures and the class

        yield {
            'name': response.meta.get('name'),
            'scp_number': response.meta.get('scp_number'),
            'scp_class': scp_class,
            'tags': tags,
            'containment_procedures': ' '.join(containment_procedures),
            'full_description': ' '.join(full_description),
            'rating': rating
        }
