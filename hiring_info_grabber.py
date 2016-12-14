import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin
import re

searchUrl = 'http://sfbay.craigslist.org/search/fbh'
baseUrl = 'http://sfbay.craigslist.org/'

class JobDescription:
    def __init__(self, dateTime, jobTitle, location, link):
        self.dateTime = dateTime
        self.jobTitle = jobTitle
        self.link = link
        self.location = location
        self.body = None
        self.contact = []
    
    def print_job(self):
        print(self.dateTime, self.jobTitle, self.location, self.body, self.contact, self.link)

def grab_hiring_info():
    response = urllib.request.urlopen(searchUrl)
    html = response.read()
    htmlNorm = html.decode("utf8")
    jobRegexp = re.compile("<li class=\"result-row\"(.*?)</li>", re.S)
    timeRegexp = re.compile("<time class=\"result-date\" datetime=\"(.*?)\" title=\"")
    titleRegexp = re.compile("<a href=\"(.*?)\" data-id=\"(.*?)\" class=\"result-title hdrlnk\">(.*?)</a>")
    locationRegexp = re.compile("<span class=\"result-hood\"> \((.*?)\)</span>")
    result = jobRegexp.findall(htmlNorm)
    jobs = []
    for item in result:
        dateTime = timeRegexp.findall(item)[0]
        tmpRes = titleRegexp.findall(item)[0]
        jobLink = tmpRes[0]
        jobTitle = tmpRes[2]
        try:
            jobLocation = locationRegexp.findall(item)[0]
        except:
            jobLocation= ""
        job = JobDescription(dateTime, jobTitle, jobLocation, urljoin(baseUrl, jobLink))
        job.print_job()
        jobs.append(job)
    return jobs

def fetch_details(jobs):
    for job in jobs:
        url = job.link
        # url = 'http://sfbay.craigslist.org/sby/fbh/5918647854.html'
        response = urllib.request.urlopen(url)
        html = response.read()
        htmlNorm = html.decode("utf8")
        bodyRegexp = re.compile("<section id=\"postingbody\">(.*?)</div>\n        </div>\n(.*?)</section>", re.S)
        results = bodyRegexp.findall(htmlNorm)[0][1]
        results = results.split('<br>')
        jobBody = []
        for result in results:
            jobBody.append(result.strip('\n'))
        jobString = ''.join(jobBody)
        job.body = jobString

        contactRegexp = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
        contacts = contactRegexp.findall(jobString)
        job.contact += contacts
        job.print_job()


def main():
    jobs = grab_hiring_info()
    fetch_details(jobs)
    # fetch_details()

    
if __name__ == '__main__':
    main()