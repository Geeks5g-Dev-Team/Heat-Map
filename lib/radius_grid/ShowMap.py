from lib.radius_grid_rules.KeywordRankingRule import AnalyzeRankingWithKeywordsReturnParams
import folium
import googlemaps
from config.GoogleConfig import GoogleConfig


class ShowMap():

    def __init__(self):
        self.google_config = GoogleConfig()
        print(f"api key: {self.google_config.get_google_secret_key()}")
        self.gmaps = googlemaps.Client(
            key=self.google_config.get_google_secret_key())

    def show_map(self, lat, lng, rows: list[AnalyzeRankingWithKeywordsReturnParams | None], map_name):

        map_center = (lat, lng)
        m = folium.Map(location=map_center, zoom_start=14, tiles="https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png",
                       attr='<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
        lines = []
        for row in rows:
            if row is None:
                continue

            folium.Marker(
                location=(row.lat, row.lng),
                popup=f"{row.average_percentage}",
                tooltip="See more info.",
                icon=folium.Icon(
                    icon="cloud", color="red" if row.average_percentage <= 0 else "green")
            ).add_to(m)

            lines.extend([(row.lat, row.lng), (lat, lng)])

        folium.PolyLine(lines).add_to(m)
        m.save(f"{map_name}.html")

    def geocode(self, address):

        geocode_result = self.gmaps.geocode(address)[0]
        location = geocode_result["geometry"]["location"]
        lat, lng = location["lat"], location["lng"]

        return lat, lng
