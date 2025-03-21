from datatypes.KeywordRankingRuleByScrappingDatatypes import FinalRankAnalysis
import googlemaps
from config.GoogleConfig import GoogleConfig
import os
from pathlib import Path
from lib.utilities.CustomFolium import Folium
from public.html.popup_display import popup_display


class ShowMap():

    def __init__(self):
        self.google_config = GoogleConfig()
        self.gmaps = googlemaps.Client(
            key=self.google_config.get_google_secret_key())
        self.fm = Folium()

    def show_map(self, lat, lng, rows: list[FinalRankAnalysis | None], map_name):

        map_center = (lat, lng)
        m = self.fm.map(
            "OPEN_STREET_MAP_DE",
            location=map_center,
            zoom_start=14
        )
        # lines = []
        for row in rows:
            if row is None:
                continue

            self.fm.marker_number(row, location=(
                row.lat, row.lng),
                tooltip=f"Latitude: {row.lat} Longitude: {row.lng}",
                popup=popup_display(row)
            )\
                .add_to(m)

            # lines.extend([(row.lat, row.lng), (lat, lng)])

        file_name = os.path.join(os.getcwd(), "maps", f"{map_name}.html")
        # folium.PolyLine(lines).add_to(m)
        m.save(file_name)

    def geocode(self, address):

        geocode_result = self.gmaps.geocode(address)[0]
        location = geocode_result["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        return lat, lng
