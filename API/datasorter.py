def sort_by_price_range(data):
    price_map = {"": 0, "$": 1, "$$": 2, "$$$": 3, "$$$$": 4, "None": 5}  # Map price symbols to numeric values
    return sorted(data, key=lambda cafe: price_map.get(cafe.get("price_range", ""), 0))

def sort_by_contact(data):
    cafes_with_contact = [cafe for cafe in data if cafe.get("lead_contacts", None) is not None]  # Filter cafes with contact
    return sorted(cafes_with_contact, key=lambda cafe: True)  # No custom key needed, cafes with contact are already filtered

def sort_by_website(data):
    cafes_with_website = [cafe for cafe in data if cafe.get("website", None) is not None]  # Filter cafes with website
    return sorted(cafes_with_website, key=lambda cafe: True)  # No custom key needed, cafes with website are already filtered

def sort_by_photo_count(data):
    return sorted(data, key=lambda cafe: cafe.get("photo_count", 0))