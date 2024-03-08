import requests
from bs4 import BeautifulSoup
import re
from scripts.process_json import write_json
from scripts.translate_text import translate_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC


def load_web_page(url, season_index): 
    driver = webdriver.Chrome()
    driver.get(url)
    
    select_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'select')))
    select = Select(select_element)
    select.select_by_value(str(season_index))

    driver.implicitly_wait(20)
    load_more_button = driver.find_element(By.CSS_SELECTOR, '.btn-load-more')

    if load_more_button.is_displayed():
        print("Button exists and is visible.")
        load_more_button.click()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element(load_more_button))
        
    # load_more_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-load-more')))
    # load_more_button.click()

    # Wait for the page to load after clicking the button
    # WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CSS_SELECTOR, '.btn-load-more')))

    # Scrape data from the loaded page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Perform scraping operations using BeautifulSoup

    # Close the webdriver
    driver.quit()
    return soup

def scrap_content_from_html(soup):
    episodes = []
    # Find all the podcast episodes
    episode_elements = soup.find_all('div', class_='podcast-episode')

    # Iterate over each episode element
    for episode_element in episode_elements:
        # Extract episode details
        title = episode_element.find('h3').text.strip()
        title_en = translate_text(title)
        summary = episode_element.find('p', class_='episodie-description').text.strip()
        summary_en = translate_text(summary)
        episode_footer = episode_element.find('div', class_='episode-footer')
        episode_season = episode_footer.find('p', class_='season').text.strip()
        season_episode, duration = episode_season.split(' · ')
        season, episode = map(int, re.findall(r'\d+', season_episode))
        podcast_url = episode_element.find('div', class_='episode-top-content').find('a')['href']

        # Append episode details to the list
        episodes.append({
            'title': {
                'es': title, 
                'en': title_en
            },
            'summary': {
                'es': summary,
                'en': summary_en
            },
            'season': season,
            'episode': episode,
            'duration': duration,
            'podcast_url': podcast_url
        })

    return episodes

# Example usage
if __name__ == "__main__":
    podcast_url = 'https://www.podiumpodcast.com/podcasts/las-hijas-de-felipe-podium-os/'

    # for i in range(1, 5):
    loaded_html = load_web_page(podcast_url, 3)
    podcast_episodes = scrap_content_from_html(loaded_html)

    file_path = f'transcriptions/las_hijas_overview_season_3.json'
    write_json(podcast_episodes, file_path)
