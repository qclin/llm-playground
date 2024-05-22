import time
import os
import requests
from bs4 import BeautifulSoup
import re
from scripts.process_json import write_json
from scripts.translate_text import translate_with_deepl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def load_web_page(url, season_index): 
    driver = webdriver.Chrome()
    driver.get(url)
    
    popup = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "didomi-popup-view"))
    )
    accept_button = popup.find_element(By.ID, "didomi-notice-agree-button")
    accept_button.click()

    select_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, 'select')))
    select = Select(select_element)
    select.select_by_value(str(season_index))
    driver.implicitly_wait(60)

    while True: 
        try:
            load_more_button = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.btn-load-more'))
            )
            load_more_button.is_displayed()
            load_more_button.click()
            print("Button exists and is visible.")
        except:
            break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # Close the webdriver
    driver.quit()
    return soup

def scrap_content_from_html(soup, season_index):
    episodes = []
    # Find all the podcast episodes
    episode_elements = soup.find_all('div', class_='podcast-episode')

    download_dir = f"Audio/season_{season_index}"
    os.makedirs(download_dir, exist_ok=True)

    # Iterate over each episode element
    for episode_element in episode_elements:
        # # Extract episode details
        title = episode_element.find('h3').text.strip()
        # title_en = translate_with_deepl(title)
        # summary = episode_element.find('p', class_='episodie-description').text.strip()
        # summary_en = translate_with_deepl(summary)
        # episode_footer = episode_element.find('div', class_='episode-footer')
        # episode_data = episode_footer.find('p', class_='season').text.strip()
   
        # podcast_url = episode_element.find('div', class_='episode-top-content').find('a')['href']
        # if ' · ' in episode_data:
        #     season_episode, duration = episode_data.split(' · ')
        #     season, episode = map(int, re.findall(r'\d+', season_episode))
        # # Append episode details to the list
        # episodes.append({
        #     'title': {
        #         'es': title, 
        #         'en': title_en
        #     },
        #     'summary': {
        #         'es': summary,
        #         'en': summary_en
        #     },
        #     'season': season,
        #     'episode': episode,
        #     'duration': duration,
        #     'podcast_url': podcast_url,
        #     'audio_path': f'season_{season}/{title}.mp3'
        # })
        episode_left_part = episode_element.find('div', class_="episode-left-part")
        download_url = episode_left_part.find('a')['href']
        print(download_url)
                # Check if the file already exists in the directory
        if os.path.exists(os.path.join(download_dir, title)):
            print(f"File {title} already exists. Skipping download.")
            continue
        else:                 
            # Download the file
            response = requests.get(download_url)
            
            # Save the file to the specified directory
            with open(os.path.join(download_dir, title), "wb") as file:
                file.write(response.content)
    return episodes

# Example usage
if __name__ == "__main__":
    podcast_url = 'https://www.podiumpodcast.com/podcasts/las-hijas-de-felipe-podium-os/'

    season = 3
    # for i in range(1, 5):
    loaded_html = load_web_page(podcast_url, season)
    podcast_episodes = scrap_content_from_html(loaded_html, season)

    # file_path = f'transcriptions/las_hijas_overview_season_{season}.json'
    # write_json(podcast_episodes, file_path)
