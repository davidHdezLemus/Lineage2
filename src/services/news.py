import requests
import csv
from io import StringIO
from typing import Dict

class NewsService:
    def __init__(self, config: Dict, lang: str):
        self.news_url = config.get('NewsUrl', '').strip()
        self.lang = lang

    def get_news_html(self) -> str:
        """
        Fetches news from a Google Sheet CSV and formats it as HTML.
        Returns the HTML string for the news content.
        """
        if not self.news_url:
            return '<i>No se ha configurado una URL de noticias.</i>'

        lang_col = 0 if self.lang == 'es' else 1

        try:
            resp = requests.get(self.news_url, timeout=5)
            if resp.status_code == 200:
                resp.encoding = 'utf-8'
                csvfile = StringIO(resp.text)
                reader = csv.reader(csvfile)
                rows = list(reader)

                if rows and len(rows) > 1:
                    noticias = []
                    for r in rows[1:]:
                        if len(r) > lang_col and r[lang_col].strip():
                            noticias.append(r[lang_col].strip())
                    
                    if noticias:
                        html = ''
                        apertura = noticias[0]
                        html += f'<b>{apertura}</b><br><br>'
                        for noticia in reversed(noticias[1:]):
                            html += f'- {noticia}<br>'
                        return html
                    else:
                        return '<i>No hay novedades del servidor en este momento.</i>'
                else:
                    return '<i>No hay novedades del servidor en este momento.</i>'
            else:
                return '<i>No se pudo conectar para comprobar novedades.</i>'
        except requests.RequestException:
            return '<i>No se pudo conectar para comprobar novedades.</i>'
        except Exception:
            return '<i>Error al procesar las noticias.</i>'