from bs4 import BeautifulSoup
import requests
from polon.getting_data import getPatentByRow
import urllib3
import time

def add_patent_authors_to_graph(csvFile):
    patent = getPatentByRow(csvFile, 1)
    # print(patent)
    authors = patent.get('authors')
    authors = authors.split("/")
    print(authors)
    final_connections = ""
    for author in authors:
        author = author.split(" ")
        if len(author) == 3:
            author[1] = author[1] + "-" + author[2]
        # print(author)
        connections = add_author_to_graph(author[0], author[1], None)
        # print(connections)
        if connections is not None:
            final_connections = final_connections + ";" + connections
    final_connections = final_connections[:-1]
    print(final_connections)
    return final_connections


def add_author_to_graph(name, surname, institute):
    link = find_author_link(name, surname, institute)
    main_author = name + "_" + surname
    if link is None:
        return
    publications = get_publications(link)
    full_author_list = []
    for publication in publications:
        full_author_list.extend(get_publication_authors(publication))
    full_author_list.sort()
    counted_list = dict([(x, full_author_list.count(x)) for x in full_author_list])
    full_author_list = list(set(full_author_list))
    final_string = ""
    # print(counted_list)
    for author in full_author_list:
        if main_author != author:
            final_string = final_string + main_author + "/" + author + "-" + str(counted_list.get(author)) + ";"
    final_string = final_string[:-1]
    print(final_string)
    return final_string


def find_author_link(name, surname, institute):
    search_link = "https://www.researchgate.net/search/authors?q=" + name + "%2B" + surname
    # print(search_link)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(search_link, headers=headers, timeout=urllib3.Timeout(connect=2.0, read=2.0))
    time.sleep(5)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    print(soup)

    found_authors = soup.find_all('div', class_='account-container')
    for author in found_authors:
        author_name = author.find('div', class_='name')

        # author_institution = author.find('div', class_='institution')
        # if author_institution is not None and author_institution.get_text() == institute:
        #     # print(author_name.get_text())
        #     # print(author_institution.get_text())
        #     account_link = author_name.a.get('href')
        #     account_link = (account_link.split("?", 1))[0]
        #     account_link = account_link[29:]
        #     # print(account_link)
        #     return account_link

        account_link = author_name.a.get('href')
        account_link = (account_link.split("?", 1))[0]
        account_link = account_link[29:]
        return account_link


def get_institute(author_link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get("https://www.researchgate.net/" + author_link, headers=headers, timeout=urllib3.Timeout(connect=2.0, read=2.0))
    time.sleep(5)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    s_institution = soup.find('div', class_="institution")
    s_institution = s_institution.find('b')
    return s_institution.get_text()

def get_publications(author_link):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get("https://www.researchgate.net/" + author_link, headers=headers, timeout=urllib3.Timeout(connect=2.0, read=2.0))
    time.sleep(5)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    # print(soup.prettify())
    researches = soup.find_all('div', class_='nova-v-publication-item')
    return researches


def get_publication_authors(publication):
    authors = publication.find_all('span', class_='nova-v-publication-item__person-list-item')
    author_list = []
    for author in authors:
        s_author_name = author.find('span', class_='nova-v-publication-item__person-list-item-name')
        author_name = s_author_name.get_text()
        author_name = author_name.replace(" ", "_")
        author_list.append(author_name)
        # print(author_name)
        # s_author_link = author.find('a', class_='nova-e-link')
        # author_link = s_author_link.get('href')
        # print(author_link)
    return author_list


add_patent_authors_to_graph('../polon/Technologia.csv')

name = "Piotr"
surname = "Arabas"
# institute = "Warsaw University of Technology"
