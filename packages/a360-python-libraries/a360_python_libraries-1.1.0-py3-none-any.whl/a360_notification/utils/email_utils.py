import re
import html


def html_to_text(html_content: str) -> str:
    clean_text = re.sub('<[^<]+?>', '', html_content)
    clean_text = html.unescape(clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text
