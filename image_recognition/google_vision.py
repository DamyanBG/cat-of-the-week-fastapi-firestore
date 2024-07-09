from google.cloud.vision import ImageAnnotatorClient, Image

from sa import credentials


def check_is_safe_image(image: Image, client: ImageAnnotatorClient) -> bool:
    """Uses the Cloud Vision API to check if an image is safe for work (SFW)."""

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Define your safety thresholds here (adjust as needed)
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )
    if likelihood_name[safe.adult] in ["LIKELY", "VERY_LIKELY"] or likelihood_name[
        safe.violence
    ] in ["LIKELY", "VERY_LIKELY"]:
        return False
    return True


def check_contains_cat(image: Image, client: ImageAnnotatorClient) -> bool:
    label_response = client.label_detection(image=image)
    labels = label_response.label_annotations
    for label in labels:
        if "cat" in label.description.lower():
            return True

    return False


def check_is_safe_and_contains_cat(image_content: bytes) -> bool:
    client = ImageAnnotatorClient(credentials=credentials)
    image = Image(content=image_content)

    is_safe = check_is_safe_image(image, client)
    contains_cat = check_contains_cat(image, client)

    is_safe_and_contains_cat = is_safe and contains_cat

    return is_safe_and_contains_cat
