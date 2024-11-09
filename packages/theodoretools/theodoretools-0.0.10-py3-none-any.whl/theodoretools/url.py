
def url_to_name(url: str):
    return url.replace(":", "").replace("/", "").replace("https", "").replace("http", "").replace("%", "")
