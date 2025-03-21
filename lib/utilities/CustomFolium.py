import folium
from typing import Literal
from lib.radius_grid_rules.RankRule import RankRule
from datatypes.KeywordRankingRuleDatatypes import AnalyzeRankingWithKeywordsReturnParams
from datatypes.KeywordRankingRuleByScrappingDatatypes import FinalRankAnalysis
from public.html.map_marker_icon import map_marker_icon, map_star_marker, map_x_marker, map_flag_marker

TileTypes = Literal["", "MAPNIK", "DE", "CH", "FRANCE", "HOT", "BZH", "CAT", "OSM_ENGLISH",
                    "TOPO_MAP", "ALIDADE_SMOOTH", "ALIDADE_SMOOTH_DARK", "ALIDADE_SATELLITE", "TRANSPORT_DARK",
                    "OPEN_STREET_MAP_DE"]


class Folium ():

    def __init__(self):

        self.rank_math_rules = RankRule()

    def map(self, tile_type: TileTypes, **fm_keys: folium.Map):

        tiles = "https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png"
        attr = '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases" title="CyclOSM - Open Bicycle render">CyclOSM</a> | Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

        if tile_type == "ALIDADE_SATELLITE":
            tiles = ""
            attr = ""
        elif tile_type == "OPEN_STREET_MAP_DE":
            tiles = "https://tile.openstreetmap.de/{z}/{x}/{y}.png"
            attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

        return folium.Map(
            **fm_keys,
            tiles=tiles,
            attr=attr
        )

    def marker_number(self, rank: FinalRankAnalysis, **fm_keys: folium.Marker):

        color_type = self.rank_math_rules.avg_number_into_icon_info(
            rank.average_percentage)
        color = ""

        if color_type == "success":
            color = "green"
            mark_design = map_marker_icon if rank.final_rank != 1 else map_star_marker

        elif color_type == "danger":
            color = "red"
            mark_design = map_x_marker

        elif color_type == "warn":
            color = "yellow"
            mark_design = map_flag_marker

        elif color_type == "info":
            color = "#dc3545"
            mark_design = map_marker_icon

        return folium.Marker(
            **fm_keys,
            icon=folium.DivIcon(
                icon_size=(30, 50),
                icon_anchor=(15, 50),
                html=mark_design(
                    color, rank.final_rank if rank.final_rank != 0 else "20+")
            )
        )
