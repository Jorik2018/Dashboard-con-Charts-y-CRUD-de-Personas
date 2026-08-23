import json
from typing import Any, TypedDict

import reflex as rx


LEAFLET_LIBRARY = "react-leaflet@5.0.0"

class LatLng(TypedDict):
    lat: float
    lng: float

def latlng(lat: float, lng: float) -> LatLng:
    return {
        "lat": lat,
        "lng": lng,
    }

class MapContainer(rx.NoSSRComponent):
    library = LEAFLET_LIBRARY
    tag = "MapContainer"
    center: rx.Var[Any]
    zoom: rx.Var[float]
    scroll_wheel_zoom: rx.Var[bool]

class TileLayer(rx.NoSSRComponent):
    library = LEAFLET_LIBRARY
    tag = "TileLayer"

    url: rx.Var[str]
    attribution: rx.Var[str]


class CircleMarker(rx.NoSSRComponent):
    library = LEAFLET_LIBRARY
    tag = "CircleMarker"

    center: rx.Var[Any]
    radius: rx.Var[float]
    path_options: rx.Var[dict[str, Any]]


class Popup(rx.NoSSRComponent):
    library = LEAFLET_LIBRARY
    tag = "Popup"


class Tooltip(rx.NoSSRComponent):
    library = LEAFLET_LIBRARY
    tag = "Tooltip"


class MapRegistry(rx.Component):
    tag = "MapRegistry"

    map_id: rx.Var[str]

    def add_imports(self):
        return {
            "react": ["useEffect"],
            LEAFLET_LIBRARY: ["useMap"],
        }

    def add_custom_code(self):
        return [
            """
function MapRegistry({ mapId }) {
    const map = useMap();

    useEffect(() => {
        window.__reflexLeafletMaps ??= {};

        window.__reflexLeafletMaps[mapId] = map;

        return () => {
            if (window.__reflexLeafletMaps) {
                delete window.__reflexLeafletMaps[mapId];
            }
        };
    }, [map, mapId]);

    return null;
}
"""
        ]

def map(
    *children,
    id: str,
    center,
    zoom,
    height: str = "100%",
    width: str = "100%",
    scroll_wheel_zoom: bool = True,
):
    """
    Wrapper equivalente a rxe.map(...).

    Además de crear MapContainer, registra la instancia Leaflet
    asociada al id.
    """

    return MapContainer.create(
        MapRegistry.create(map_id=id),
        *children,
        id=id,
        center=center,
        zoom=zoom,
        scroll_wheel_zoom=scroll_wheel_zoom,
        style={
            "height": height,
            "width": width,
        },
    )


class MapApi:
    def __init__(self, map_id: str):
        self.map_id = map_id

    def fly_to(
        self,
        center: dict[str, Any],
        zoom: float,
    ):
        lat = center["lat"]
        lng = center["lng"]

        map_id_js = json.dumps(self.map_id)

        lat_js = rx.Var.create(lat)
        lng_js = rx.Var.create(lng)
        zoom_js = rx.Var.create(zoom)

        script = rx.Var.create(
            f"""
(() => {{
    const map = window.__reflexLeafletMaps?.[{map_id_js}];

    if (!map) {{
        console.warn(
            "Leaflet map not registered:",
            {map_id_js}
        );
        return;
    }}

    map.flyTo(
        [{lat_js}, {lng_js}],
        {zoom_js}
    );
}})()
"""
        )

        return rx.call_script(script)
    

def api(map_id: str) -> MapApi:
    return MapApi(map_id)

def path_options(
    *,
    color=None,
    fill_color=None,
    fill_opacity=None,
    weight=None,
):
    options = {}

    if color is not None:
        options["color"] = color

    if fill_color is not None:
        options["fillColor"] = fill_color

    if fill_opacity is not None:
        options["fillOpacity"] = fill_opacity

    if weight is not None:
        options["weight"] = weight

    return options


map_container = MapContainer.create
tile_layer = TileLayer.create
popup = Popup.create
tooltip = Tooltip.create

def _normalize_center(center):
    if isinstance(center, dict):
        return [
            center["lat"],
            center["lng"],
        ]

    return center

def circle_marker(
    *children,
    center,
    radius=10,
    path_options=None,
    **props,
):
    return CircleMarker.create(
        *children,
        center=_normalize_center(center),
        radius=radius,
        path_options=path_options,
        **props,
    )