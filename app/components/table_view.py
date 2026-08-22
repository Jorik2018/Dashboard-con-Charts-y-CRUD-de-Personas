import reflex as rx
from app.states.dashboard_state import DashboardState, Persona
from app.components.persona_modals import (
    delete_confirm_modal,
    persona_form_modal,
)


def _toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "search",
                class_name="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400",
            ),
            rx.el.input(
                placeholder="Buscar por nombre, apellido, ciudad o año...",
                default_value=DashboardState.search_query,
                on_change=DashboardState.set_search_query.debounce(300),
                class_name="w-full rounded-lg border border-gray-300 bg-white pl-9 pr-3 py-2 text-sm font-medium text-gray-700 placeholder:text-gray-400 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 outline-hidden transition-colors",
            ),
            class_name="relative w-full sm:max-w-sm",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.select(
                    rx.el.option("Todos los géneros", value=""),
                    rx.foreach(
                        DashboardState.generos,
                        lambda g: rx.el.option(g, value=g),
                    ),
                    value=DashboardState.genero_filter,
                    on_change=DashboardState.set_genero_filter,
                    class_name="appearance-none rounded-lg border border-gray-300 bg-white pl-3 pr-9 py-2 text-sm font-medium text-gray-700 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30 outline-hidden cursor-pointer",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.cond(
                DashboardState.filtros_activos,
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4"),
                    rx.el.span("Limpiar", class_name="hidden sm:inline"),
                    on_click=DashboardState.clear_filters,
                    class_name="flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer",
                ),
                rx.fragment(),
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                rx.el.span("Nueva persona", class_name="hidden sm:inline"),
                on_click=DashboardState.open_create,
                class_name="flex items-center gap-2 rounded-lg bg-violet-600 px-3 py-2 text-sm font-semibold text-white hover:bg-violet-700 transition-colors cursor-pointer",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 w-full",
    )


def _sort_icon(field: str) -> rx.Component:
    return rx.cond(
        DashboardState.sort_field == field,
        rx.cond(
            DashboardState.sort_desc,
            rx.icon("arrow-down", class_name="h-3.5 w-3.5 text-violet-600"),
            rx.icon("arrow-up", class_name="h-3.5 w-3.5 text-violet-600"),
        ),
        rx.icon("chevrons-up-down", class_name="h-3.5 w-3.5 text-gray-300"),
    )


def _header_cell(label: str, field: str, icon: str) -> rx.Component:
    return rx.el.th(
        rx.el.button(
            rx.icon(icon, class_name="h-3.5 w-3.5 text-gray-400"),
            label,
            _sort_icon(field),
            on_click=lambda: DashboardState.sort_by(field),
            class_name=rx.cond(
                DashboardState.sort_field == field,
                "flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-violet-700 cursor-pointer",
                "flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-gray-500 hover:text-gray-900 transition-colors cursor-pointer",
            ),
        ),
        class_name="px-5 py-3 text-left whitespace-nowrap",
    )


def _row(persona: Persona) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={persona['nombre']} {persona['apellido']}",
                    class_name="size-8 rounded-full bg-gray-100 shrink-0",
                ),
                rx.el.span(
                    persona["nombre"],
                    class_name="text-sm font-semibold text-gray-900",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            class_name="px-5 py-3 whitespace-nowrap",
        ),
        rx.el.td(
            persona["apellido"],
            class_name="px-5 py-3 text-sm font-medium text-gray-600 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                persona["genero"],
                class_name=rx.cond(
                    persona["genero"] == "Mujer",
                    "w-fit rounded-full bg-violet-100 px-2 py-1 text-xs font-semibold text-violet-600",
                    "w-fit rounded-full bg-blue-100 px-2 py-1 text-xs font-semibold text-blue-500",
                ),
            ),
            class_name="px-5 py-3",
        ),
        rx.el.td(
            persona["anio_nacimiento"],
            class_name="px-5 py-3 text-sm font-medium text-gray-600",
        ),
        rx.el.td(
            persona["ciudad"],
            class_name="px-5 py-3 text-sm font-medium text-gray-600 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("square-pen", class_name="h-4 w-4"),
                    on_click=lambda: DashboardState.open_edit(persona["id"]),
                    title="Editar",
                    class_name="flex items-center justify-center size-8 rounded-lg border border-gray-200 bg-white text-gray-500 hover:text-violet-600 hover:border-violet-200 hover:bg-violet-50 transition-colors cursor-pointer",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DashboardState.request_delete(
                        persona["id"]
                    ),
                    title="Eliminar",
                    class_name="flex items-center justify-center size-8 rounded-lg border border-gray-200 bg-white text-gray-500 hover:text-red-500 hover:border-red-200 hover:bg-red-100 transition-colors cursor-pointer",
                ),
                class_name="flex items-center justify-end gap-2",
            ),
            class_name="px-5 py-3",
        ),
        class_name="hover:bg-gray-50 transition-colors",
    )


def _empty_state() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("users", class_name="h-5 w-5 text-gray-400"),
            class_name="flex items-center justify-center size-11 rounded-xl border border-gray-200 bg-gray-50",
        ),
        rx.el.p(
            "Sin resultados",
            class_name="mt-3 text-sm font-semibold text-gray-900",
        ),
        rx.el.p(
            "Ajusta la búsqueda o agrega una nueva persona.",
            class_name="text-xs font-medium text-gray-500",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Agregar persona",
            on_click=DashboardState.open_create,
            class_name="flex items-center gap-2 mt-4 rounded-lg bg-violet-600 px-3 py-2 text-sm font-semibold text-white hover:bg-violet-700 transition-colors cursor-pointer",
        ),
        class_name="flex flex-col items-center justify-center py-14 px-5 text-center w-full",
    )


def _table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    _header_cell("Nombre", "nombre", "user"),
                    _header_cell("Apellido", "apellido", "type"),
                    _header_cell("Género", "genero", "venetian-mask"),
                    _header_cell("Año", "anio_nacimiento", "calendar"),
                    _header_cell("Ciudad", "ciudad", "map-pin"),
                    rx.el.th(
                        rx.el.span(
                            "Acciones",
                            class_name="text-xs font-semibold uppercase tracking-wider text-gray-500",
                        ),
                        class_name="px-5 py-3 text-right whitespace-nowrap",
                    ),
                    class_name="bg-gray-50 border-b border-gray-200",
                ),
            ),
            rx.el.tbody(
                rx.foreach(
                    DashboardState.personas_filtradas,
                    _row,
                ),
                class_name="divide-y divide-gray-200",
            ),
            class_name="table-auto w-full",
        ),
        class_name="w-full overflow-x-auto",
    )


def _card() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Registros de personas",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    f"{DashboardState.total_filtradas} de {DashboardState.total_personas} registros",
                    class_name="text-xs font-medium text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.span(
                f"Orden: {DashboardState.sort_label}",
                class_name="w-fit rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-500",
            ),
            class_name="flex items-center justify-between gap-3 border-b border-gray-200 px-5 py-4",
        ),
        rx.cond(
            DashboardState.total_filtradas > 0,
            _table(),
            _empty_state(),
        ),
        class_name="w-full rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def table_view() -> rx.Component:
    return rx.el.div(
        _toolbar(),
        _card(),
        persona_form_modal(),
        delete_confirm_modal(),
        class_name="flex flex-col gap-4 w-full",
    )
