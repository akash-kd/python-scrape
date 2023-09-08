import requests

requests.post("https://ntfy.sh/ph-scrape",
  data="Backup successful 😀".encode(encoding='utf-8'))