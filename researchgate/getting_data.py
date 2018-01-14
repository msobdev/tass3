from bs4 import BeautifulSoup
import requests

def findAuthor(name, surname, institute):
    searchLink = "https://www.researchgate.net/search/authors?q=" + name + "%2B" + surname
    page = requests.get(searchLink)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    foundAuthors = soup.find_all('div', class_='account-container')

    for author in foundAuthors:
        authorName = author.find('div', class_='name')

        authorIntitution = author.find('div', class_='institution')
        if authorIntitution != None and authorIntitution.get_text() == institute:
            print(authorName.get_text())
            print(authorIntitution.get_text())
            accountLink = authorName.a.get('href')
            print(accountLink)
            return accountLink


def getPublications(authorLink):
    page = requests.get(authorLink)
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')
    researches = soup.find_all('div', class_='nova-v-publication-item')
    return researches


def getPublicationAuthors(publication):
    authors = publication.find_all('span', class_='nova-v-publication-item__person-list-item')
    for author in authors:
        b_authorName = author.find('span', class_='nova-v-publication-item__person-list-item-name')
        authorName = b_authorName.get_text()
        print(authorName)
        b_authorLink = author.find('a', class_='nova-e-link')
        authorLink = b_authorLink.get('href')
        print(authorLink)


name = "Piotr"
surname = "Arabas"
link = findAuthor(name, surname, "Warsaw University of Technology")
researches = getPublications(link)
research = researches[0]
getPublicationAuthors(research)
# print(research.prettify())
# print(soup.prettify())

