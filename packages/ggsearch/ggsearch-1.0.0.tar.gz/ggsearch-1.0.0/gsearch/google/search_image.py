import requests
from bs4 import BeautifulSoup
import re
from loguru import logger

class GoogleImageSearch:
    SEARCH_URL = "https://www.google.com/search?tbm=isch"  # tbm=isch est pour Google Images

    def __init__(self, lang="fr", region="FR"):
        self.lang = lang
        self.region = region
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            "Accept-Language": f"{lang}-{self.region},{lang};q=0.9,en-US;q=0.8,en;q=0.7"
        }

    def search(self, query, num_images=10):
        """Effectue la recherche d'images Google et retourne les images avec leurs dimensions."""
        logger.info('Début de la fonction de recherche d\'images Google.')

        params = {
            "q": query,
            "hl": self.lang,
            "gl": self.region,
        }

        # Faire la requête HTTP sans utiliser de proxy
        try:
            response = requests.get(self.SEARCH_URL, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            logger.error(f"Erreur lors de la requête HTTP: {exc}")
            return None

        # Créer un objet BeautifulSoup pour l'analyse du HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Extraction des images et de leurs métadonnées
        image_results = self.extract_image_results(soup, response.url)

        # Limiter le nombre de résultats selon `num_images`
        search_results = image_results[:num_images]

        return search_results

    def extract_image_results(self, soup, full_url):
        """Extrait les images et leurs métadonnées des résultats Google Image Search."""
        images_data = []
        image_blocks = soup.find_all("div", class_="eA0Zlc")

        position = 1
        for block in image_blocks:
            img_tag = block.find("img")
            if not img_tag:
                continue

            thumbnail_id = img_tag.get("id")
            title_tag = block.find("div", class_="ptes9b")
            title = title_tag.get_text(strip=True) if title_tag else "Titre non disponible"
            description_tag = block.find("div", class_="JMWMJ")
            description = description_tag.get_text(strip=True) if description_tag else "Description non disponible"
            link_tag = block.find("a", class_="EZAeBe")
            source_url = link_tag.get("href") if link_tag else "URL non disponible"
            img_width = img_tag.get("width", "Unknown")
            img_height = img_tag.get("height", "Unknown")

            image_url_from_script = self.extract_image_url_from_script(soup, thumbnail_id)

            if image_url_from_script == "URL non trouvée":
                image_url_from_script = self.extract_base64_image_from_script(soup, thumbnail_id)

                if image_url_from_script != "URL non trouvée":
                    logger.info(f"Image trouvée en format base64 pour l'ID {thumbnail_id}")

            image_url_from_script = image_url_from_script.replace("\\x3d", "").replace("\\x3d", "")

            images_data.append({
                "position": position,
                "id": thumbnail_id,
                "title": title,
                "description": description,
                "source_url": source_url,
                "width": img_width,
                "height": img_height,
                "image": image_url_from_script,
                "query_url": full_url
            })

            position += 1

        return images_data

    def extract_image_url_from_script(self, soup, thumbnail_id):
        """Cherche l'URL d'image dans les balises <script> contenant "id:url"."""
        try:
            if thumbnail_id.startswith("dimg_"):
                thumbnail_script_id = thumbnail_id
            else:
                return "ID incorrect"

            scripts = soup.find_all("script")

            for script in scripts:
                script_text = script.string
                if script_text and thumbnail_script_id in script_text:
                    pattern = re.escape(thumbnail_script_id) + r'":"(https://[^"]+)"'
                    match = re.search(pattern, script_text)
                    if match:
                        return match.group(1).replace("\\u003d", "=").replace("\\u0026", "&")

        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de l'URL à partir du script : {e}")

        return "URL non trouvée"

    def extract_base64_image_from_script(self, soup, thumbnail_id):
        """Cherche une image encodée en base64 dans les balises <script> avec un ID."""
        try:
            scripts = soup.find_all("script")

            for script in scripts:
                script_text = script.string
                if script_text and thumbnail_id in script_text:
                    logger.info(f"ID {thumbnail_id} trouvé dans un script pour une image encodée en base64.")
                    pattern = r"'data:image/[^']+base64,[^']+'"
                    match = re.search(pattern, script_text)
                    if match:
                        return match.group(0).strip("'").replace("\\x3d", "=")

        except Exception as e:
            logger.error(f"Erreur lors de l'extraction de l'image encodée en base64 : {e}")

        return "URL non trouvée"
