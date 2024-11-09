import base64


def get_image_base64(filepath: str, ext: str = 'png'):
    with open(filepath, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data)
    data = f"data:image/{ext};base64," + encoded.decode("utf-8")
    return data
