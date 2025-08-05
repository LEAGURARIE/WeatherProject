from utills.city_list import cities, cities_hebrew

def get_city_coordinates(city_input: str) -> dict:
    """
    Get city coordinates from normalized city input.
    Handles both English and Hebrew city names with flexible matching.
    """
    if not city_input:
        return {"error": "No city input provided"}

    # Strategy 1: Exact match (case-insensitive)
    for city_key in cities.keys():
        if city_input.lower().strip() == city_key.lower():
            return cities[city_key]

    for heb_key in cities_hebrew.keys():
        if city_input.strip() == heb_key:
            eng_key = cities_hebrew[heb_key]
            return cities.get(eng_key, {"error": "City not found"})

    # Strategy 2: Normalized match (no spaces, case-insensitive)
    normalized_input = city_input.lower().strip().replace(" ", "")

    for city_key in cities.keys():
        normalized_key = city_key.lower().replace(" ", "")
        if normalized_input == normalized_key:
            return cities[city_key]

    for heb_key in cities_hebrew.keys():
        normalized_heb_key = heb_key.replace(" ", "")
        if normalized_input == normalized_heb_key:
            eng_key = cities_hebrew[heb_key]
            return cities.get(eng_key, {"error": "City not found"})

    return {"error": "City not found"}


def filter_cities(query, city_list):
    """Filter cities based on user query with smart matching"""
    if not query:
        return []

    query_lower = query.lower().strip()

    # Exact matches first
    exact_matches = [city for city in city_list if city.lower() == query_lower]

    # Starts with matches
    starts_with = [city for city in city_list
                   if city.lower().startswith(query_lower) and city not in exact_matches]

    # Contains matches
    contains = [city for city in city_list
                if query_lower in city.lower() and city not in exact_matches + starts_with]

    return exact_matches + starts_with + contains


#def get_english_city_name(selected_city_display, lang):
 #   """Convert selected city to English name for API calls"""
 #   if lang == "English":
  #      return selected_city_display
  #  else:
  #      return cities_hebrew.get(selected_city_display, selected_city_display)


