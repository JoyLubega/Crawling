import scrapy
from scrapy import FormRequest
from scrapy.utils.response import open_in_browser

class PostSpider(scrapy.Spider):
    name = "post_spider"

    def start_requests(self):
        urls = [
            'https://procesos.ramajudicial.gov.co/consultaprocesos/ConsultaJusticias21.aspx',
        ]
        for url in urls:
            yield scrapy.Request(url=url, dont_filter = True, callback=self.parse_cities)

    def parse_cities(self, response):

        # get All cities
        # cities=response.xpath('//*[@id="ddlJuzgados"]/option/text()').extract()
        urls = response.xpath('//*[@id="ddlJuzgados"]/option/@value').extract()
        urls.pop(0)
        for url in urls:
            
            valid_url = 'https://procesos.ramajudicial.gov.co'+url

            yield response.follow(url=valid_url, callback= self.parse_form)

    def parse_form(self, response):
        
        form_data ={
            "cbadju":"3",
            "norad":"98703271"
        }
        yield FormRequest.from_response(
            response, 
            formdata=form_data,
            method='POST',
            callback=self.parse_result   
        )
    def parse_result(self, response):
        number_radication = response.css('.timpar a::attr(href)').extract_first()
        headers = response.xpath('//*[@class="e_tablas"]/th/text()').extract()
        headers.pop(0)
        row = response.xpath('//*[@class="timpar"]/td/text()').extract()

        data = dict(zip(headers, row))
        yield data
        
        
            

        