import scrapy
from scrapy import FormRequest

class PostSpider(scrapy.Spider):
    name = "post_spider"

    def start_requests(self):
        urls = [
            'https://procesos.ramajudicial.gov.co/consultaprocesos/ConsultaJusticias21.aspx',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_cities)

    def parse_cities(self, response):
        cities=response.xpath('//*[@id="ddlJuzgados"]/option/text()').extract()
        cities.pop(0)
        valid_cities = cities
        for city in valid_cities:
            # link = response.xpath("//input/@onclick[contains(., 'juzgados')]")
            link='https://procesos.ramajudicial.gov.co/jepms/'+city.lower()+'jepms/conectar.asp'
            yield scrapy.Request(url=link, callback= self.parse_form)

    def parse_form(self, response):
        
        yield FormRequest.from_response(
            response, 
            formdata={
                "cbadju":"Identification document of the subject",
                "norad":"98703271"
            },
            callback=self.parse_result
        )
    def parse_result():
        print("hey")

           
            
            

        