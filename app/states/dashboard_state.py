import reflex as rx
from typing import TypedDict
from app.components.leaflet import LatLng, latlng
from app.services import people_service

CITY_COORDS: dict[str, tuple[float, float]] = {
    "madrid": (40.4168, -3.7038),
    "bogotá": (4.711, -74.0721),
}

class NavItem(TypedDict):
    key: str
    label: str
    icon: str
    description: str

class Persona(TypedDict):
    id: str
    nombre: str
    apellido: str
    genero: str
    anio_nacimiento: int
    ciudad: str
    lat: float
    lon: float

class MapPoint(TypedDict):
    id: int
    label: str
    genero: str
    ciudad: str
    anio: int
    lat: float
    lon: float
    color: str
    coords: str

class CityGroup(TypedDict):
    ciudad: str
    total: int
    lat: float
    lon: float
    coords: str

class DashboardState(rx.State):
    """Shell state: navegación entre vistas y datos base compartidos."""

    active_view: str = "chart"
    sidebar_open: bool = False

    nav_items: list[NavItem] = [
        {
            "key": "chart",
            "label": "Chart",
            "icon": "chart-pie",
            "description": "Distribución por género y año",
        },
        {
            "key": "table",
            "label": "Table",
            "icon": "table",
            "description": "Listado y gestión de personas",
        },
        {
            "key": "map",
            "label": "Mapa",
            "icon": "map",
            "description": "Ubicación por coordenadas",
        },
    ]

    personas: list[Persona] = []

    map_center: LatLng = latlng(lat=8.0, lng=-45.0)
    map_zoom: float = 3.0
    selected_point_id: int = 0

    search_query: str = ""
    genero_filter: str = ""
    sort_field: str = "nombre"
    sort_desc: bool = False

    form_open: bool = False
    editing_id: int = 0
    form_key: int = 0
    form_nombre: str = ""
    form_apellido: str = ""
    form_genero: str = "Mujer"
    form_anio: str = ""
    form_ciudad: str = ""
    form_lat: str = ""
    form_lon: str = ""
    form_errors: dict[str, str] = {}

    delete_id = None

    generos: list[str] = ["Hombre", "Mujer"]

    @rx.event
    def set_view(self, view: str):
        self.active_view = view
        self.sidebar_open = False

    @rx.event
    def set_search_query(self, value: str):
        self.search_query = value

    @rx.event
    def set_genero_filter(self, value: str):
        self.genero_filter = value

    @rx.event
    def clear_filters(self):
        self.search_query = ""
        self.genero_filter = ""

    @rx.event
    def sort_by(self, field: str):
        if self.sort_field == field:
            self.sort_desc = not self.sort_desc
        else:
            self.sort_field = field
            self.sort_desc = False

    def _reset_form(self):
        self.form_nombre = ""
        self.form_apellido = ""
        self.form_genero = "Mujer"
        self.form_anio = ""
        self.form_ciudad = ""
        self.form_lat = ""
        self.form_lon = ""
        self.form_errors = {}
        self.form_key += 1

    @rx.event
    def open_create(self):
        self.editing_id = 0
        self._reset_form()
        self.active_view = "table"
        self.sidebar_open = False
        self.form_open = True

    @rx.event
    def open_edit(self, persona_id: int):
        persona = next(
            (p for p in self.personas if p["id"] == persona_id), None
        )
        if persona is None:
            return rx.toast("No se encontró la persona.")
        self.editing_id = persona_id
        self.form_nombre = persona["nombre"]
        self.form_apellido = persona["apellido"]
        self.form_genero = persona["genero"]
        self.form_anio = str(persona["anio_nacimiento"])
        self.form_ciudad = persona["ciudad"]
        self.form_lat = f"{float(persona['lat']):.4f}"
        self.form_lon = f"{float(persona['lon']):.4f}"
        self.form_errors = {}
        self.form_key += 1
        self.form_open = True

    @rx.event
    def close_form(self):
        self.form_open = False
        self.editing_id = 0
        self.form_errors = {}


    @rx.event
    def load_people(self):
        self.personas = people_service.find_all()

    def _validate(
        self, nombre: str, apellido: str, genero: str, anio: str, ciudad: str
    ) -> dict[str, str]:
        errors: dict[str, str] = {}
        if len(nombre) < 2:
            errors["nombre"] = "El nombre debe tener al menos 2 caracteres."
        if len(apellido) < 2:
            errors["apellido"] = "El apellido debe tener al menos 2 caracteres."
        if genero not in ("Hombre", "Mujer"):
            errors["genero"] = "Selecciona un género válido."
        if not anio.isdigit():
            errors["anio_nacimiento"] = "Ingresa un año válido (ej. 1995)."
        elif not 1900 <= int(anio) <= 2025:
            errors["anio_nacimiento"] = "El año debe estar entre 1900 y 2025."
        if len(ciudad) < 2:
            errors["ciudad"] = "La ciudad debe tener al menos 2 caracteres."
        return errors

    def _parse_coord(
        self, value: str, limite: float, campo: str, errors: dict[str, str]
    ) -> float | None:
        if not value:
            return None
        try:
            numero = float(value.replace(",", "."))
        except ValueError:
            errors[campo] = "Ingresa un número válido (ej. 40.4168)."
            return None
        if abs(numero) > limite:
            errors[campo] = f"Debe estar entre -{limite:.0f} y {limite:.0f}."
            return None
        return numero

    def _coords_por_ciudad(self, ciudad: str) -> tuple[float, float]:
        return CITY_COORDS.get(ciudad.strip().lower(), (40.4168, -3.7038))


    @rx.event
    def submit_form(self, form_data: dict[str, str]):
        nombre = str(form_data.get("nombre", "")).strip()
        apellido = str(form_data.get("apellido", "")).strip()
        genero = str(form_data.get("genero", "")).strip()
        anio = str(form_data.get("anio_nacimiento", "")).strip()
        ciudad = str(form_data.get("ciudad", "")).strip()
        lat_raw = str(form_data.get("lat", "")).strip()
        lon_raw = str(form_data.get("lon", "")).strip()

        self.form_lat = lat_raw
        self.form_lon = lon_raw
        self.form_nombre = nombre
        self.form_apellido = apellido
        self.form_genero = genero
        self.form_anio = anio
        self.form_ciudad = ciudad

        errors = self._validate(
            nombre,
            apellido,
            genero,
            anio,
            ciudad,
        )

        lat_value = self._parse_coord(
            lat_raw,
            90.0,
            "lat",
            errors,
        )

        lon_value = self._parse_coord(
            lon_raw,
            180.0,
            "lon",
            errors,
        )

        if errors:
            self.form_errors = errors
            self.form_key += 1

            return rx.toast(
                "Revisa los campos marcados.",
                duration=3000,
            )

        self.form_errors = {}

        if self.editing_id:
            persona_actual = people_service.find_by_id(
                self.editing_id
            )

            if persona_actual is None:
                return rx.toast(
                    "No se encontró la persona.",
                    duration=3000,
                )

            lat_final = (
                lat_value
                if lat_value is not None
                else float(persona_actual["lat"])
            )

            lon_final = (
                lon_value
                if lon_value is not None
                else float(persona_actual["lon"])
            )

            persona = {
                "nombre": nombre,
                "apellido": apellido,
                "genero": genero,
                "anio_nacimiento": int(anio),
                "ciudad": ciudad,
                "lat": lat_final,
                "lon": lon_final,
            }

            people_service.update(
                self.editing_id,
                persona,
            )

            mensaje = f"{nombre} {apellido} fue actualizado."

        else:
            fallback_lat, fallback_lon = (
                self._coords_por_ciudad(ciudad)
            )

            persona = {
                "nombre": nombre,
                "apellido": apellido,
                "genero": genero,
                "anio_nacimiento": int(anio),
                "ciudad": ciudad,
                "lat": (
                    lat_value
                    if lat_value is not None
                    else fallback_lat
                ),
                "lon": (
                    lon_value
                    if lon_value is not None
                    else fallback_lon
                ),
            }

            people_service.create(persona)

            mensaje = f"{nombre} {apellido} fue agregado."

        # Recargar desde repository
        self.personas = people_service.find_all()

        self.form_open = False
        self.editing_id = 0

        return rx.toast(
            mensaje,
            duration=3000,
        )

    @rx.event
    def request_delete(self, persona_id):
        self.delete_id = persona_id

    @rx.event
    def cancel_delete(self):
        self.delete_id = None

    @rx.event
    def confirm_delete(self):
        result = people_service.delete(self.delete_id)

        if not result.deleted:
            return rx.toast(
                "No se pudo eliminar la persona.",
                duration=3000,
            )

        self.personas = people_service.find_all()
        self.delete_id = None

        return rx.toast(
            f"{result.persona['nombre']} "
            f"{result.persona['apellido']} fue eliminado.",
            duration=3000,
        )

    @rx.var
    def personas_filtradas(self) -> list[Persona]:
        query = self.search_query.strip().lower()
        resultado = list(self.personas)
        if self.genero_filter:
            resultado = [
                p for p in resultado if p["genero"] == self.genero_filter
            ]
        if query:
            resultado = [
                p
                for p in resultado
                if query in p["nombre"].lower()
                or query in p["apellido"].lower()
                or query in p["ciudad"].lower()
                or query in str(p["anio_nacimiento"])
            ]
        campo = self.sort_field
        if campo == "anio_nacimiento":
            resultado.sort(
                key=lambda p: int(p["anio_nacimiento"]),
                reverse=self.sort_desc,
            )
        else:
            resultado.sort(
                key=lambda p: str(p.get(campo, "")).lower(),
                reverse=self.sort_desc,
            )
        return resultado

    @rx.var
    def total_filtradas(self) -> int:
        return len(self.personas_filtradas)

    @rx.var
    def filtros_activos(self) -> bool:
        return bool(self.search_query) or bool(self.genero_filter)

    @rx.var
    def form_title(self) -> str:
        return "Editar persona" if self.editing_id else "Nueva persona"

    @rx.var
    def form_subtitle(self) -> str:
        if self.editing_id:
            return "Actualiza los datos del registro seleccionado."
        return "Completa los datos para agregar un registro."

    @rx.var
    def form_submit_label(self) -> str:
        return "Guardar cambios" if self.editing_id else "Agregar persona"

    @rx.var
    def delete_open(self) -> bool:
        return self.delete_id is not None

    @rx.var
    def delete_nombre(self) -> str:
        persona = next(
            (p for p in self.personas if p["id"] == self.delete_id), None
        )
        if persona is None:
            return ""
        return f"{persona['nombre']} {persona['apellido']}"

    @rx.var
    def sort_label(self) -> str:
        etiquetas = {
            "nombre": "Nombre",
            "apellido": "Apellido",
            "genero": "Género",
            "anio_nacimiento": "Año",
            "ciudad": "Ciudad",
        }
        direccion = "desc" if self.sort_desc else "asc"
        return f"{etiquetas.get(self.sort_field, 'Nombre')} · {direccion}"

    @rx.event
    def select_point(self, persona_id: int):
        self.selected_point_id = persona_id

    @rx.event
    def reset_map_view(self):
        self.selected_point_id = 0

    @rx.var
    def map_points(self) -> list[MapPoint]:
        puntos: list[MapPoint] = []
        for p in self.personas_filtradas:
            lat = float(p["lat"])
            lon = float(p["lon"])
            puntos.append(
                {
                    "id": p["id"],
                    "label": f"{p['nombre']} {p['apellido']}",
                    "genero": p["genero"],
                    "ciudad": p["ciudad"],
                    "anio": int(p["anio_nacimiento"]),
                    "lat": lat,
                    "lon": lon,
                    "color": "#7c3aed" if p["genero"] == "Mujer" else "#3b82f6",
                    "coords": f"{lat:.4f}, {lon:.4f}",
                }
            )
        return puntos

    @rx.var
    def ciudades_resumen(self) -> list[CityGroup]:
        grupos: dict[str, list[Persona]] = {}
        for p in self.personas_filtradas:
            grupos.setdefault(p["ciudad"], []).append(p)
        resumen: list[CityGroup] = []
        for ciudad, personas in grupos.items():
            lat = sum(float(p["lat"]) for p in personas) / len(personas)
            lon = sum(float(p["lon"]) for p in personas) / len(personas)
            resumen.append(
                {
                    "ciudad": ciudad,
                    "total": len(personas),
                    "lat": lat,
                    "lon": lon,
                    "coords": f"{lat:.4f}, {lon:.4f}",
                }
            )
        resumen.sort(key=lambda c: (-c["total"], c["ciudad"]))
        return resumen

    @rx.var
    def total_ciudades(self) -> int:
        return len({p["ciudad"] for p in self.personas})

    @rx.var
    def ciudad_top(self) -> str:
        resumen = self.ciudades_resumen
        if not resumen:
            return "—"
        return resumen[0]["ciudad"]

    @rx.var
    def selected_label(self) -> str:
        print(self.personas)
        persona = next(
            (p for p in self.personas if p["id"] == self.selected_point_id),
            None,
        )
        if persona is None:
            return ""
        return f"{persona['nombre']} {persona['apellido']}"

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.var
    def total_personas(self) -> int:
        return len(self.personas)

    @rx.var
    def total_hombres(self) -> int:
        return len([p for p in self.personas if p["genero"] == "Hombre"])

    @rx.var
    def total_mujeres(self) -> int:
        return len([p for p in self.personas if p["genero"] == "Mujer"])

    @rx.var
    def anios_distintos(self) -> int:
        return len({p["anio_nacimiento"] for p in self.personas})

    @rx.var
    def distribucion_genero(self) -> list[dict[str, str | int]]:
        return [
            {
                "name": "Hombres",
                "value": self.total_hombres,
                "fill": "#3b82f6",
            },
            {
                "name": "Mujeres",
                "value": self.total_mujeres,
                "fill": "#7c3aed",
            },
        ]

    @rx.var
    def porcentaje_hombres(self) -> float:
        if not self.personas:
            return 0.0
        return self.total_hombres / len(self.personas) * 100

    @rx.var
    def porcentaje_mujeres(self) -> float:
        if not self.personas:
            return 0.0
        return self.total_mujeres / len(self.personas) * 100

    @rx.var
    def personas_por_anio(self) -> list[dict[str, str | int]]:
        conteo: dict[int, int] = {}
        for p in self.personas:
            anio = int(p["anio_nacimiento"])
            conteo[anio] = conteo.get(anio, 0) + 1
        return [
            {"anio": str(anio), "total": conteo[anio]}
            for anio in sorted(conteo)
        ]

    @rx.var
    def anio_con_mas_personas(self) -> str:
        if not self.personas:
            return "—"
        conteo: dict[int, int] = {}
        for p in self.personas:
            anio = int(p["anio_nacimiento"])
            conteo[anio] = conteo.get(anio, 0) + 1
        mejor = max(conteo.items(), key=lambda item: (item[1], item[0]))
        return str(mejor[0])

    @rx.var
    def rango_anios(self) -> str:
        if not self.personas:
            return "—"
        anios = [int(p["anio_nacimiento"]) for p in self.personas]
        return f"{min(anios)} - {max(anios)}"

    @rx.var
    def view_title(self) -> str:
        titulos = {
            "chart": "Distribución de personas",
            "table": "Personas",
            "map": "Mapa de personas",
        }
        return titulos.get(self.active_view, "Personas")

    @rx.var
    def view_subtitle(self) -> str:
        subtitulos = {
            "chart": "Visualiza género y año de nacimiento de un vistazo.",
            "table": "Consulta, agrega y edita registros de personas.",
            "map": "Ubicación de cada persona según sus coordenadas.",
        }
        return subtitulos.get(
            self.active_view, "Consulta y gestiona registros de personas."
        )
