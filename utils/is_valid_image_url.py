def is_valid_image_url(url: str) -> bool:
    if not url:
        return False
    url = url.lower()
    return url.startswith("http") and url.split("?")[0].endswith((".jpg", ".jpeg", ".png", ".webp"))
