FROM python:3.6 

#copy all to app-directory
COPY ./ /app/

# change working-directory to /app
WORKDIR /app

# install required apps
RUN pip install -r requirements.txt

# go into the scrapy directory
WORKDIR /app/gant

# execute crawler
CMD scrapy crawl gant -s CLOSESPIDER_ITEMCOUNT=50

