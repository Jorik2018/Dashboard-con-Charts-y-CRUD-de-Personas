import reflex as rx
import reflex_enterprise as rxe
from app.states.dashboard_state import (
    CityGroup,
    DashboardState,
    MapPoint,
)

MAP_ID = "personas-map"


def _stat(label: str, value: rx.Var | str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-violet-600"),
            class_name="flex items-center justify-center size-8 rounded-lg border border-violet-100 bg-violet-50 shrink-0",
        ),
        rx.el.div(
            rx.el.span(
                label,
                class_name="text-xs font-medium text-gray-500 leading-tight",
            ),
            rx.el.span(
                value,
                class_name="text-sm font-semibold text-gray-900 leading-tight",
            ),
            class_name="flex flex-col min-w-0",
        ),
        class_name="flex items-center gap-3 rounded-xl border border-gray-200 bg-white px-4 py-3 w-full",
    )


def _stats() -> rx.Component:
    return rx.el.div(
        _stat("Personas en el mapa", DashboardState.total_filtradas, "map-pin"),
        _stat(
            "Ciudades distintas", DashboardState.total_ciudades, "building-2"
        ),
        _stat("Ciudad con más registros", DashboardState.ciudad_top, "star"),
        _stat(
            "Seleccionada",
            rx.cond(
                DashboardState.selected_label != "",
                DashboardState.selected_label,
                "Ninguna",
            ),
            "crosshair",
        ),
        class_name="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4 w-full",
    )


def _marker(point: MapPoint) -> rx.Component:
    return rxe.map.circle_marker(
        rxe.map.tooltip(point["label"]),
        rxe.map.popup(
            rx.el.div(
                rx.el.p(
                    point["label"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"{point['ciudad']} · {point['anio']}",
                    class_name="text-xs font-medium text-gray-500",
                ),
                rx.el.p(
                    point["coords"],
                    class_name="text-xs font-medium text-violet-600",
                ),
                class_name="flex flex-col gap-0.5 font-['Inter']",
            )
        ),
        center={"lat": point["lat"], "lng": point["lon"]},
        radius=9,
        path_options=rxe.map.path_options(
            color=point["color"],
            fill_color=point["color"],
            fill_opacity=0.65,
            weight=2,
        ),
    )


def _map_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("map", class_name="h-4 w-4 text-violet-600"),
                    class_name="flex items-center justify-center size-8 rounded-lg border border-violet-100 bg-violet-50",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Mapa interactivo",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Un punto por persona según lat/lon",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        class_name="size-2.5 rounded-full shrink-0 bg-violet-600"
                    ),
                    rx.el.span(
                        "Mujeres",
                        class_name="text-xs font-medium text-gray-600",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.div(
                    rx.el.span(
                        class_name="size-2.5 rounded-full shrink-0 bg-blue-500"
                    ),
                    rx.el.span(
                        "Hombres",
                        class_name="text-xs font-medium text-gray-600",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.button(
                    rx.icon("locate-fixed", class_name="h-4 w-4"),
                    rx.el.span("Vista general", class_name="hidden sm:inline"),
                    on_click=[
                        DashboardState.reset_map_view,
                        rxe.map.api(MAP_ID).fly_to(
                            DashboardState.map_center,
                            DashboardState.map_zoom,
                        ),
                    ],
                    class_name="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer",
                ),
                class_name="flex items-center gap-4",
            ),
            class_name="flex flex-wrap items-center justify-between gap-3 border-b border-gray-200 px-5 py-4",
        ),
        rx.el.div(
            rxe.map(
                rxe.map.tile_layer(
                    url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attribution">CARTO</a>',
                ),
                rx.foreach(DashboardState.map_points, _marker),
                id=MAP_ID,
                center=DashboardState.map_center,
                zoom=DashboardState.map_zoom,
                height="100%",
                width="100%",
            ),
            class_name="w-full h-[420px] lg:h-[520px] min-w-[280px]",
        ),
        class_name="flex flex-col w-full rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _location_row(point: MapPoint) -> rx.Component:
    return rx.el.button(
        rx.el.span(
            class_name=rx.cond(
                point["genero"] == "Mujer",
                "size-2.5 rounded-full shrink-0 bg-violet-600",
                "size-2.5 rounded-full shrink-0 bg-blue-500",
            )
        ),
        rx.el.div(
            rx.el.span(
                point["label"],
                class_name="text-sm font-semibold text-gray-900 leading-tight",
            ),
            rx.el.span(
                f"{point['ciudad']} · {point['coords']}",
                class_name="text-xs font-medium text-gray-500 leading-tight",
            ),
            class_name="flex flex-col items-start text-left min-w-0",
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-300 shrink-0"),
        on_click=[
            DashboardState.select_point(point["id"]),
            rxe.map.api(MAP_ID).fly_to(
                {"lat": point["lat"], "lng": point["lon"]}, 11.0
            ),
        ],
        class_name=rx.cond(
            DashboardState.selected_point_id == point["id"],
            "flex items-center gap-3 w-full rounded-lg border border-violet-200 bg-violet-50 px-3 py-2.5 transition-colors cursor-pointer",
            "flex items-center gap-3 w-full rounded-lg border border-gray-200 bg-white px-3 py-2.5 hover:bg-gray-50 transition-colors cursor-pointer",
        ),
    )


def _city_row(city: CityGroup) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.icon("building-2", class_name="h-4 w-4 text-gray-400 shrink-0"),
            rx.el.div(
                rx.el.span(
                    city["ciudad"],
                    class_name="text-sm font-semibold text-gray-900 leading-tight",
                ),
                rx.el.span(
                    city["coords"],
                    class_name="text-xs font-medium text-gray-500 leading-tight",
                ),
                class_name="flex flex-col items-start text-left min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0",
        ),
        rx.el.span(
            city["total"],
            class_name="w-fit shrink-0 rounded-full bg-violet-100 px-2 py-1 text-xs font-semibold text-violet-600",
        ),
        on_click=rxe.map.api(MAP_ID).fly_to(
            {"lat": city["lat"], "lng": city["lon"]}, 9.0
        ),
        class_name="flex items-center justify-between gap-3 w-full rounded-lg border border-gray-200 bg-white px-3 py-2.5 hover:bg-gray-50 transition-colors cursor-pointer",
    )


def _empty_locations() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("map-pin-off", class_name="h-5 w-5 text-gray-400"),
            class_name="flex items-center justify-center size-11 rounded-xl border border-gray-200 bg-gray-50",
        ),
        rx.el.p(
            "Sin ubicaciones",
            class_name="mt-3 text-sm font-semibold text-gray-900",
        ),
        rx.el.p(
            "Ajusta los filtros o agrega personas con coordenadas.",
            class_name="text-xs font-medium text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-10 px-5 text-center w-full",
    )


def _side_panel() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Ubicaciones",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"{DashboardState.total_filtradas} personas geolocalizadas",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.span(
                f"{DashboardState.total_ciudades} ciudades",
                class_name="w-fit rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-500",
            ),
            class_name="flex items-center justify-between gap-3 border-b border-gray-200 px-5 py-4",
        ),
        rx.cond(
            DashboardState.total_filtradas > 0,
            rx.el.div(
                rx.el.div(
                    rx.foreach(DashboardState.map_points, _location_row),
                    class_name="flex flex-col gap-2",
                ),
                rx.el.div(
                    rx.el.span(
                        "Resumen por ciudad",
                        class_name="text-xs font-semibold uppercase tracking-wider text-gray-400",
                    ),
                    rx.el.div(
                        rx.foreach(DashboardState.ciudades_resumen, _city_row),
                        class_name="flex flex-col gap-2 mt-2",
                    ),
                    class_name="flex flex-col mt-5 pt-5 border-t border-gray-200",
                ),
                class_name="flex flex-col p-5 max-h-[520px] overflow-y-auto",
            ),
            _empty_locations(),
        ),
        class_name="flex flex-col w-full rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def map_view() -> rx.Component:
    return rx.el.div(
        _stats(),
        rx.el.div(
            rx.el.div(_map_card(), class_name="flex-1 min-w-0"),
            rx.el.div(
                _side_panel(),
                class_name="w-full xl:w-80 shrink-0",
            ),
            class_name="flex flex-col xl:flex-row gap-4 w-full",
        ),
        class_name="flex flex-col gap-4 w-full",
    )
