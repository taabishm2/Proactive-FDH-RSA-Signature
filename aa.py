from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup


def simple_get(url):
    try:
        r = get(url)
        if is_good_resp(r):
            return r.content
        else:
            print('Invalid URL')
            return None
    except RequestException as e:
        print('Exception')


def is_good_resp(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def get_names(url):
    raw_html = simple_get(url)
    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')
        names = set()  # add to set to prevent duplicates
        for li in html.select('li'):
            for name in li.text.split('\n'):  # list of strings found by breaking the string at enter
                if len(name) > 0:
                    names.add(name.strip())  # remove leading and trailing whitespaces
        return list(names)  # convert set back to list
        raise Exception('Error retrieving contents at {}'.format(url))


def get_hits(name):
    math = get_url(name)
    response = simple_get(math)
    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        hit_link = [a for a in html.select('a') if a['href'].find('latest-60') > -1]
        if len(hit_link) > 0:
            link_text = hit_link[0].text.replace(',', '')
            try:
                print(int(link_text))
            except:
                print('Couldnt parse as int')
        log_error('No pageviews found for {}'.format(name))
        return None


def get_url(name):
    mid1 = name.replace('  ', ' ')
    mid2 = mid1.replace(' ', '%20')
    url_1 = 'https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/'
    url_2 = '/monthly/20180123/20180228'
    return (url_1 + mid2 + url_2)


if __name__ == '__main__':
    names = []
    print('Getting the list of names....')
    names = get_names('http://www.fabpedigree.com/james/mathmen.htm')
    print('... done.\n')
    results = []
    print('Getting stats for each name....')
    for name in names:
        try:
            hits = get_hits(name)
            if hits is None:
                hits = -1
            results.append((hits, name))
        except:
            results.append((-1, name))
            log_error('error encountered while processing '
                      '{}, skipping'.format(name))

    print('... done.\n')

    results.sort()
    results.reverse()

    if len(results) > 5:
        top_marks = results[:5]
    else:
        top_marks = results

    print('\nThe most popular mathematicians are:\n')
    for (mark, mathematician) in top_marks:
        print('{} with {} pageviews'.format(mathematician, mark))

    no_results = len([res for res in results if res[0] == -1])
    print('\nBut we did not find results for '
          '{} mathematicians on the list'.format(no_results))