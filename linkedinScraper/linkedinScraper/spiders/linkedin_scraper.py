import scrapy
from linkedinScraper.items import JobItem

class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=data%2Banalyst&location=Worldwide&trk=public_jobs_jobs-search-bar_search-submit&start=0' 

    def start_requests(self):
        job0 = 0
        # first_url = self.api_url + str(job0)
        first_url = self.api_url
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': job0})


    def parse_job(self, response):
        if response.status == 403:
            self.logger.warning("Forbidden response received.")
            return

        job_item = JobItem()
        jobs = response.css("li")
        job_count = 0
        
        
        for job in jobs:
            
            job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            job_item['location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            job_item['job_post_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['company_link'] = job.css('h4 a::attr(href)').get(default='not-found')
            job_item['date_listed'] = job.css('time::text').get(default='not-found').strip()

        
            self.logger.info(job_item)
            
            yield job_item
            
            job_count += 1
            if job_count >= 20:
                self.logger.info("Maximum limit (20) reached. Stopping further scraping.")
                return