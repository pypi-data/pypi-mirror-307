from bs4 import BeautifulSoup
import requests
from loguru import logger

# Configuration de Loguru pour le logging
logger.add("scraper.log", rotation="500 MB", level="DEBUG", format="{time} - {level} - {message}")

class GoogleRichSearch:
    def __init__(self, lang="en", region="US"):
        self.lang = lang
        self.region = region

    def get_google_results(self, query):
        """Exécute une recherche Google Rich et renvoie les résultats sous forme de dictionnaire."""
        logger.info('Début de la fonction get_google_results')

        url = f"https://www.google.com/search?q={query}"

        try:
            # Faire la requête HTTP sans utiliser de proxy
            response = requests.get(
                url, 
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept-Language": f"{self.lang}-{self.region},{self.lang};q=0.9,en-US;q=0.8,en;q=0.7"
                },
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Erreur lors de la requête HTTP: {exc}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        logger.info('Le contenu HTML a été analysé avec succès')

        result_data = {}

        # Titre de l'entité
        title_tag = soup.find('div', attrs={'data-attrid': 'title'})
        result_data['title'] = title_tag.text.strip() if title_tag else None

        # Sous-titre (type d'organisation ou autre)
        subtitle_tag = soup.find('div', attrs={'data-attrid': 'subtitle'})
        result_data['subtitle'] = subtitle_tag.text.strip() if subtitle_tag else None

        # Description
        description_tag = soup.find('div', attrs={'data-attrid': 'description'})
        result_data['description'] = description_tag.text.strip() if description_tag else None

        # URL de l'image (thumbnail)
        thumbnail_tag = soup.find('g-img', class_='PZPZlf')
        result_data['thumbnail'] = thumbnail_tag['data-lpage'] if thumbnail_tag else None

        # Extraction dynamique des informations supplémentaires
        info_data = self._extract_info_sections(soup)
        result_data['info'] = info_data

        # Réseaux sociaux (extraction dynamique)
        socials = self._extract_social_links(soup)
        result_data['socials'] = socials

        logger.info('Fin de la fonction get_google_results')
        return result_data

    def _extract_info_sections(self, soup):
        """Extrait les informations supplémentaires dynamiques depuis les sections pertinentes."""
        info_data = {}
        info_sections = soup.find_all('div', class_='wDYxhc')

        for section in info_sections:
            label_tag = section.find('span', class_='w8qArf FoJoyf')
            if label_tag:
                label = label_tag.get_text().strip()

                value_tag = section.find('span', class_='LrzXr kno-fv wHYlTd z8gr9e')
                if value_tag:
                    value = value_tag.get_text(separator=" ").strip()

                    info_data[label] = value

        return info_data

    def _extract_social_links(self, soup):
        """Extrait les liens des réseaux sociaux."""
        socials = {}
        social_links = soup.find_all('g-link')

        for social in social_links:
            platform_tag = social.find('a')
            if platform_tag:
                platform_name = platform_tag.text.strip()
                platform_link = platform_tag['href']
                socials[platform_name] = platform_link

        return socials
