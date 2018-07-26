import json
import datetime
import csv
import time
#may choose to only import urllb.request
import urllib.request

#id of the access token as formed by the dummy application
#needs to be filled

app_id = ""
app_secret = ""

access_token = app_id + "|" + app_secret

#alter as needed to find out which page to identify
#numeric id of bamboo grove page = 560898400668463
page_id = "SNUBamboo"

#YYYY_MM_DD
since = ""
until = ""

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False;
    while success is False:
        try:
            response = urllib.reuest.urlopen(req)
            if response.getcode() = 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            #optionally print error
    return response.read()

#check if works for korean
def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')

def getFacebookPageFeedUrl(base_url):
    fields = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true)"

    return base_url + fields

def getReactionsForStatuses(base_url):

    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}

    for reaction_type in reaction_types:
        fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(
            reaction_type.upper())

        url = base_url + fields

        data = json.loads(request_until_succeed(url))['data']

        data_processed = set()  # set() removes rare duplicates in statuses
        for status in data:
            id = status['id']
            count = status['reactions']['summary']['total_count']
            data_processed.add((id, count))

        for id, count in data_processed:
            if id in reactions_dict:
                reactions_dict[id] = reactions_dict[id] + (count,)
            else:
                reactions_dict[id] = (count,)

    return reactions_dict

def processFacebookPageFeedStatus(status):
    status_id = status['id']
    status_type = status['type']

    status_message = '' if 'message' not in status else  unicode_decode(status['message'])
    link_name = '' if 'name' not in status else unicode_decode(status['name'])
    status_link = '' if 'link' not in status else unicode_decode(status['link'])

    status_published = datetime.datetime.strptime(status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=+9) #is this KST??? need to check
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S)

    num_reactions = 0 if 'reactions' not in status else status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else status['comments']['summary']['total_count']
    num_shares = 0 if 'num_shares' not in status else status['shares']['count']

    return (status_id, status_message, link_name, status_type, status_link, status_published, num_reactions, num_comments, num_shares)

def scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date):
    with open('{}_facebook_statuses.csv'.format(page_id), 'w') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "link_name", "status_type",
                    "status_link", "status_published", "num_reactions",
                    "num_comments", "num_shares", "num_likes", "num_loves",
                    "num_wows", "num_hahas", "num_sads", "num_angrys",
                    "num_special"])

        has_next_page = True
        num_processed = 0
        scrape_starttime = datetime.datetime.now()
        after = ''
        base = "https://graph.facebook.com/v2.9"
        node = "/{}/posts".format(page_id)
        parameters = "/?limit={}&access_token={}".format(100, access_token)
        since = "&since={}".format(since_date) if since_date is not '' else ''
        until = "&until={}".format(until_date) if until_date is not '' else ''

        print("Scraping {} Facebook Page: {}\n".format(page_id, scrape_starttime))

        while has_next_page:
            after = '' if after is '' else "&after={}".format(after)
            base_url = base + node + parameters + after + since + until

            url = getFacebookPageFeedUrl(base_url)
            statuses = json.loads(request_until_succeed(url))
            reactions = getReactionsForStatuses(base_url)

            for status in statuses['data']:

                if 'reactions' in status:
                    status_data = processFacebookPageFeedStatus(status)
                    reactions_data = reactions[status_data[0]]

                    num_special = status_data[6] - sum(reactions_data)
                    w.writerow(status_data + reactions_data + (num_special,))

                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format
                          (num_processed, datetime.datetime.now()))

            # if there is no next page
            if 'paging' in statuses:
                after = statuses['paging']['cursors']['after']
            else:
                has_next_page = False

        print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(page_id, access_token, since_date, until_date)
