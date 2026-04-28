# Hallucination Comparison

Same questions asked twice — once with Context7 live docs, once without.

---

## Case 1: Open-Meteo geocoding — empty result shape

**Question asked:** "What does the Open-Meteo geocoding API return when a city is not found?"

### Without Context7

> "The API returns an empty `results` array:
> ```json
> { "results": [] }
> ```
> So you should check `if not data['results']`."

**Code generated:**
```python
def get_coordinates(city):
    resp = requests.get(GEO_URL, params={"name": city, "count": 1})
    data = resp.json()
    if not data["results"]:      # KeyError crash when city not found
        raise WeatherError(f"City not found: {city}")
    ...
```

**What actually happens:** Key `results` is **absent entirely** — not an empty list.
This code crashes with `KeyError: 'results'` on every invalid city.

---

### With Context7

> "When no results are found, the `results` key is **omitted** from the response entirely.
> Do not access `data['results']` directly — use `data.get('results')`."

**Code generated:**
```python
def get_coordinates(city):
    resp = requests.get(GEO_URL, params={"name": city, "count": 1})
    data = resp.json()
    if not data.get("results"):  # safe — handles absent key
        raise WeatherError(f"City not found: {city}")
    ...
```

**Result:** Correct. Matches actual API behavior. No crash.

---

## Case 2: WMO weather codes

**Question asked:** "What are the WMO weather interpretation codes used by Open-Meteo?"

### Without Context7

> "WMO codes are standard meteorological codes. Common ones:
> - `0` = Clear
> - `1` = Partly cloudy
> - `2` = Cloudy
> - `3` = Overcast
> - `10` = Mist
> - `20` = Rain
> - `30` = Snow
> - `50` = Fog"

**Code generated:**
```python
WMO_CODES = {
    0: "Clear",
    1: "Partly cloudy",
    2: "Cloudy",
    10: "Mist",       # wrong — not used by Open-Meteo
    20: "Rain",       # wrong — Open-Meteo uses 61/63/65
    30: "Snow",       # wrong — Open-Meteo uses 71/73/75
    50: "Fog",        # wrong — Open-Meteo uses 45/48
}
```

Most codes map to `None` → template crashes or shows blank condition.

---

### With Context7

> "Open-Meteo uses a specific subset of WMO codes. The full mapping:
> - `0` Clear sky, `1` Mainly clear, `2` Partly cloudy, `3` Overcast
> - `45/48` Fog / Icy fog
> - `51/53/55` Drizzle (light/moderate/heavy)
> - `61/63/65` Rain (light/moderate/heavy)
> - `71/73/75` Snow (light/moderate/heavy)
> - `80/81/82` Rain showers
> - `95/96/99` Thunderstorm variants"

**Code generated:**
```python
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Icy fog",
    51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle",
    61: "Light rain", 63: "Rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy showers", 82: "Violent showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}
```

**Result:** Exact match with Open-Meteo's actual code set. All conditions display correctly.

---

## Summary

| | Without Live Docs | With Context7 |
|---|---|---|
| Geocoding empty result | Assumed `[]`, caused `KeyError` crash | Knew key is absent, used `.get()` |
| WMO weather codes | Invented plausible-looking codes, most wrong | Fetched exact Open-Meteo subset |
| Bugs introduced | 2 silent bugs shipped | 0 |
| Discovery method | Runtime crash / blank UI | Caught at write-time |

**Takeaway:** Both hallucinations were confident and plausible — they looked correct.
Context7 didn't just add information; it replaced wrong assumptions with verified facts.
