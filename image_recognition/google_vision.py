from google.cloud import vision

from sa import credentials


def check_is_safe_image(image_content: bytes) -> bool:
    """Uses the Cloud Vision API to check if an image is safe for work (SFW)."""
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # label_response = client.label_detection(image=image)
    # labels = label_response.label_annotations
    # for label in labels:
    #     print(label.description)

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
