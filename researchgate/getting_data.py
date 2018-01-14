from bs4 import BeautifulSoup
import requests


def add_author_to_graph(name, surname, institute):
    link = find_author_link(name, surname, institute)
    main_author = name + "_" + surname
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
            final_string = final_string + main_author + "/" + author + "-" + str(counted_list.get(author)) + ","
    final_string = final_string[:-1]
    print(final_string)


def find_author_link(name, surname, institute):
    search_link = "https://www.researchgate.net/search/authors?q=" + name + "%2B" + surname
    page = requests.get(search_link)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    found_authors = soup.find_all('div', class_='account-container')

    for author in found_authors:
        author_name = author.find('div', class_='name')

        author_institution = author.find('div', class_='institution')
        if author_institution is not None and author_institution.get_text() == institute:
            # print(author_name.get_text())
            # print(author_institution.get_text())
            account_link = author_name.a.get('href')
            account_link = (account_link.split("?", 1))[0]
            account_link = account_link[29:]
            # print(account_link)
            return account_link


def get_institute(author_link):
    page = requests.get("https://www.researchgate.net/" + author_link)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    s_institution = soup.find('div', class_="institution")
    s_institution = s_institution.find('b')
    return s_institution.get_text()

def get_publications(author_link):
    page = requests.get("https://www.researchgate.net/" + author_link)
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


name = "Piotr"
surname = "Arabas"
institute = "Warsaw University of Technology"
add_author_to_graph(name, surname, institute)
# link = find_author_link(name, surname, institute)
# print(get_institute(link))

# research = researches[0]
# getPublicationAuthors(research)
# print(research.prettify())
# print(soup.prettify())

