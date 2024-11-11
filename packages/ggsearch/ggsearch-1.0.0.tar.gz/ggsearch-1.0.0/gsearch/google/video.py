import requests
from bs4 import BeautifulSoup
import re
import json
from loguru import logger
from concurrent.futures import ThreadPoolExecutor, as_completed

class GoogleVideoSearch:
    SEARCH_URL = "https://www.google.com/search"
    RESULT_SELECTOR = "div.MjjYud"
    TOTAL_SELECTOR = "#result-stats"
    RELATED_SEARCH_SELECTOR = "div.qR29te"

    def __init__(self, lang="fr", region="FR", country_restriction=None, safe_mode="off", time_filter=None):
        self.lang = lang
        self.region = region
        self.country_restriction = country_restriction
        self.safe_mode = safe_mode
        self.time_filter = time_filter
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": f"{lang}-{region},{lang};q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def search(self, query, num_results=10, results_per_page=10, num_prefetch_threads=5):
        search_results = []
        related_searches = []
        total = None
        search_futures = []

        # Calcule le nombre de pages complètes et les résultats restants
        pages = num_results // results_per_page
        remaining_results = num_results % results_per_page

        with ThreadPoolExecutor(max_workers=num_prefetch_threads) as executor:
            # Pour chaque page complète
            for i in range(pages):
                start = i * results_per_page
                params = {
                    "q": query,
                    "start": start,
                    "tbm": "vid",
                    "hl": self.lang,
                    "gl": self.region,
                    "num": results_per_page,
                    "safe": self.safe_mode
                }

                if self.country_restriction:
                    params["cr"] = self.country_restriction

                if self.time_filter:
                    params["tbs"] = f"qdr:{self.time_filter}"  # Ajout du préfixe "qdr:"

                search_futures.append(executor.submit(self.fetch_results_page, params))

            # S'il reste des résultats (si num_results n'est pas un multiple de results_per_page)
            if remaining_results > 0:
                start = pages * results_per_page
                params = {
                    "q": query,
                    "start": start,
                    "tbm": "vid",
                    "hl": self.lang,
                    "gl": self.region,
                    "num": remaining_results,
                    "safe": self.safe_mode
                }

                if self.country_restriction:
                    params["cr"] = self.country_restriction

                if self.time_filter:
                    params["tbs"] = f"qdr:{self.time_filter}"  # Ajout du préfixe "qdr:"

                search_futures.append(executor.submit(self.fetch_results_page, params))

            # Collecte les résultats au fur et à mesure que les threads se terminent
            for future in as_completed(search_futures):
                results_page, page_total, page_related_searches = future.result()
                if page_total and total is None:
                    total = page_total
                search_results.extend(results_page)
                related_searches.extend(page_related_searches)

        return self.to_dict(search_results, total, related_searches)

    def fetch_results_page(self, params):
        try:
            # Faire la requête HTTP sans utiliser de proxy
            response = requests.get(self.SEARCH_URL, headers=self.headers, params=params, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            total_text = soup.select_one(self.TOTAL_SELECTOR)
            total = None
            if total_text:
                total = int(re.sub("[', ]", "", re.search(r"([0-9, ]+)", total_text.text).group(1)))

            results = self.parse_results(soup.select(self.RESULT_SELECTOR))
            related_searches = self.extract_related_searches(soup)

            return results, total, related_searches
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la page : {e}")
            return [], None, []

    def parse_results(self, results):
        search_results = []
        for result in results:
            video_info = self.extract_video_info(result)
            if video_info:
                search_results.append(video_info)
        return search_results

    def extract_video_info(self, div):
        try:
            # Remplace les messages "non trouvé" par des chaînes vides ("") quand il n'y a pas de données
            link_tag = div.find('a')
            link = link_tag['href'] if link_tag else ""

            title_tag = div.find('h3', class_="LC20lb")
            title = title_tag.text if title_tag else ""

            source_tag = div.find('cite', class_="iUh30")
            source = source_tag.text.strip() if source_tag else ""

            preview_tag = div.find('div', class_="VYkpsb")
            preview_link = preview_tag['data-url'] if preview_tag else ""

            description_tag = div.find('div', class_="ITZIwc")
            description = description_tag.text if description_tag else ""

            author_tag = div.find('span', class_="cuFRh")
            author = author_tag.text if author_tag else ""

            date_tag = div.find_all('span')[-1]
            date = date_tag.text if date_tag else ""

            return {
                "title": title,
                "link": link,
                "source": source,
                "preview": preview_link,
                "description": description,
                "author": author,
                "date": date
            }
        except Exception as e:
            logger.error(f"Erreur lors de l'extraction des informations de la vidéo: {e}")
            return None

    def extract_related_searches(self, soup):
        related_searches = []
        related_search_elements = soup.select(self.RELATED_SEARCH_SELECTOR)
        for related_search in related_search_elements:
            a_tag = related_search.find("a")
            if a_tag:
                search_text = a_tag.get_text().strip()
                search_url = a_tag['href']
                related_searches.append({
                    "text": search_text,
                    "url": f"https://google.com{search_url}"
                })
        return related_searches

    def to_dict(self, search_results, total, related_searches):
        """Retourne un dictionnaire Python pour pouvoir l'afficher directement."""
        result_dict = {
            "total_results": total,
            "related_searches": related_searches,
            "results": search_results
        }
        logger.info(f"Résultats générés:\n{json.dumps(result_dict, indent=4, ensure_ascii=False)}")
        return result_dict
