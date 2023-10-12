import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_filmography(actor_name):
    # Create a search URL for the actor on IMDb
    search_url = f"https://www.imdb.com/find?q={actor_name.replace(' ', '+')}&s=nm"

    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    
    # Send an HTTP GET request to the search URL
    response = requests.get(search_url, headers = HEADERS);
    
    if response.status_code != 200:
        print("Failed to fetch data from IMDb. Please check your input or try again later.")
        return

    # Parse the search page to find the actor's IMDb page
    soup = BeautifulSoup(response.text, 'html.parser')
    name_link = soup.find("li", class_="find-name-result").find("a")
    actor_url = "https://www.imdb.com" + name_link['href']
    
    # Send an HTTP GET request to the actor's IMDb page
    response = requests.get(actor_url, headers = HEADERS);

    if response.status_code != 200:
        print("Failed to fetch data from IMDb. Please check your input or try again later.")
        return

    # Parse the actor's page to find their filmography
    soup = BeautifulSoup(response.text, 'html.parser')
    filmography_section = soup.find("div", class_="sc-a6d4b6c0-0 jGufEe")    
    films = filmography_section.find_all("div", class_="ipc-list-card--span");
    
    filmography = []

    for film in films:
        title = film.find("a", class_="ipc-primary-image-list-card__title").text
        year = film.find("div", class_="ipc-primary-image-list-card__content-bottom").find("span", class_="ipc-primary-image-list-card__secondary-text").text;
        filmography.append({"title" : title.strip(), "year" : year.strip()})

    filmography = sorted(filmography, key=lambda x: datetime.strptime(x['year'], '%Y'))
    return filmography

if __name__ == "__main__":
    actor_name = input("Enter the name of the actor: ")
    filmography = get_filmography(actor_name)

    if filmography:
        print(f"Filmography of {actor_name} in descending order:")
        for film in reversed(filmography):
            print(film['title'], film['year'])
    else:
        print("No filmography data found for the actor.")