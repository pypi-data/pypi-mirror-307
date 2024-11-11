import requests
from bs4 import BeautifulSoup
import time
from loguru import logger

class GoogleSearchAPI:
    def __init__(self, lang='en', region='US', safe='off', advanced=False, ssl_verify=True, site_filter=None, file_type=None):
        self.search_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": f"{lang}-{region},{lang};q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.safe = safe
        self.advanced = advanced
        self.ssl_verify = ssl_verify
        self.site_filter = site_filter
        self.file_type = file_type
        logger.add("google_search.log", rotation="500 MB")

    def fetch_html(self, url, params):
        """Télécharge le HTML de la page Google Search avec les paramètres donnés."""
        try:
            # Faire la requête HTTP sans utiliser de proxy
            response = requests.get(url, params=params, headers=self.headers, verify=self.ssl_verify)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Erreur lors de la récupération de {url}: {e}")
            return None

    def google_search(self, query, num_results=10):
        """Exécute la recherche Google pour la requête spécifiée et retourne les résultats."""
        start_time = time.time()
        results = []
        seen_urls = set()
        total_results = 0
        page_size = 10
        result_id = 1

        if self.site_filter:
            query += f" site:{self.site_filter}"

        if self.file_type:
            query += f" filetype:{self.file_type}"

        while total_results < num_results:
            params = {
                "q": query,
                "num": page_size,
                "start": total_results,
                "safe": self.safe,
            }

            if self.advanced:
                params.update({"as_qdr": "y"})

            html = self.fetch_html(self.search_url, params)
            if not html:
                break

            soup = BeautifulSoup(html, 'html.parser')
            search_results = soup.find_all('div', class_='tF2Cxc')
            additional_results = soup.find_all('div', class_='g')

            all_results = search_results + additional_results

            for g in all_results:
                title_element = g.find('h3')
                link_element = g.find('a')

                if not link_element or not title_element:
                    continue

                link = link_element['href']

                if link in seen_urls:
                    continue

                seen_urls.add(link)

                snippet = ""
                snippet_element = g.find('div', class_='VwiC3b')
                if not snippet_element:
                    snippet_element = g.find('span', class_='aCOpRe')
                if snippet_element:
                    snippet = snippet_element.get_text()

                title = title_element.text if title_element else "No title available"

                meta_title = ""
                meta_about = ""
                meta_container = g.find('div', class_='CA5RN')
                if meta_container:
                    meta_title_element = meta_container.find('span', class_='VuuXrf')
                    meta_about_element = meta_container.find('cite', class_='qLRx3b')
                    if meta_title_element:
                        meta_title = meta_title_element.get_text()
                    if meta_about_element:
                        meta_about = meta_about_element.get_text()

                thumbnail = ""
                img_element = g.find('img')
                if img_element and img_element.get('src'):
                    thumbnail = img_element['src']

                results.append({
                    'id': result_id,
                    'title': title,
                    'link': link,
                    'snippet': snippet if snippet else "No snippet available",
                    'displayed_link': link_element.text if link_element else "No displayed link available",
                    'meta': {
                        'title': meta_title if meta_title else "No meta title available",
                        'about': meta_about if meta_about else "No meta about available",
                        'thumbnails': thumbnail if thumbnail else "No thumbnail available"
                    }
                })

                result_id += 1
                total_results += 1
                if total_results >= num_results:
                    break

            if len(all_results) == 0:
                break

        end_time = time.time()
        runtime = end_time - start_time

        metadata = {
            "num_requested": num_results,
            "total_items_fetched": total_results,
            "runtime_seconds": runtime
        }

        result_data = {'metadata': metadata, 'results': results}

        logger.info(f"Temps d'exécution : {runtime:.2f} secondes.")
        return result_data
