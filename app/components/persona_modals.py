import reflex as rx
from app.states.dashboard_state import DashboardState

INPUT_BASE = "w-full rounded-lg border bg-white px-3 py-2 text-sm font-medium text-gray-900 placeholder:text-gray-400 outline-hidden transition-colors"
INPUT_OK = f"{INPUT_BASE} border-gray-300 focus:border-violet-500 focus:ring-2 focus:ring-violet-500/30"
INPUT_ERROR = f"{INPUT_BASE} border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500/30"


def _error_text(name: str) -> rx.Component:
    return rx.cond(
        DashboardState.form_errors.get(name, "") != "",
        rx.el.p(
            DashboardState.form_errors.get(name, ""),
            class_name="mt-1 text-xs font-medium text-red-500",
        ),
        rx.fragment(),
    )


def _text_field(
    label: str,
    name: str,
    placeholder: str,
    value: rx.Var,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            html_for=name,
            class_name="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1.5",
        ),
        rx.el.input(
            id=name,
            name=name,
            placeholder=placeholder,
            default_value=value,
            key=f"{name}-{DashboardState.form_key}",
            class_name=rx.cond(
                DashboardState.form_errors.get(name, "") != "",
                INPUT_ERROR,
                INPUT_OK,
            ),
        ),
        _error_text(name),
        class_name="w-full",
    )


def _genero_field() -> rx.Component:
    return rx.el.div(
        rx.el.label(
            "Género",
            html_for="genero",
            class_name="block text-xs font-semibold uppercase tracking-wider text-gray-500 mb-1.5",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    DashboardState.generos,
                    lambda g: rx.el.option(g, value=g),
                ),
                id="genero",
                name="genero",
                default_value=DashboardState.form_genero,
                key=f"genero-{DashboardState.form_key}",
                class_name=rx.cond(
                    DashboardState.form_errors.get("genero", "") != "",
                    f"{INPUT_ERROR} appearance-none pr-9 cursor-pointer",
                    f"{INPUT_OK} appearance-none pr-9 cursor-pointer",
                ),
            ),
            rx.icon(
                "chevron-down",
                class_name="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none",
            ),
            class_name="relative w-full",
        ),
        _error_text("genero"),
        class_name="w-full",
    )


def persona_form_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_click=DashboardState.close_form,
            class_name="absolute inset-0 bg-gray-900/40",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "user-plus", class_name="h-4 w-4 text-violet-600"
                        ),
                        class_name="flex items-center justify-center size-8 rounded-lg border border-violet-100 bg-violet-50",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            DashboardState.form_title,
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            DashboardState.form_subtitle,
                            class_name="text-xs font-medium text-gray-500",
                        ),
                        class_name="flex flex-col min-w-0",
                    ),
                    class_name="flex items-center gap-3 min-w-0",
                ),
                rx.el.button(
                    rx.icon("x", class_name="h-4 w-4 text-gray-400"),
                    type="button",
                    on_click=DashboardState.close_form,
                    class_name="flex items-center justify-center size-8 rounded-lg hover:bg-gray-100 transition-colors cursor-pointer",
                ),
                class_name="flex items-center justify-between gap-3 border-b border-gray-200 px-5 py-4",
            ),
            rx.el.form(
                rx.el.div(
                    _text_field(
                        "Nombre",
                        "nombre",
                        "Ej. Lucía",
                        DashboardState.form_nombre,
                    ),
                    _text_field(
                        "Apellido",
                        "apellido",
                        "Ej. Fernández",
                        DashboardState.form_apellido,
                    ),
                    _genero_field(),
                    _text_field(
                        "Año de nacimiento",
                        "anio_nacimiento",
                        "Ej. 1995",
                        DashboardState.form_anio,
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-2 gap-4",
                ),
                rx.el.div(
                    _text_field(
                        "Ciudad",
                        "ciudad",
                        "Ej. Madrid",
                        DashboardState.form_ciudad,
                    ),
                    _text_field(
                        "Latitud",
                        "lat",
                        "Ej. 40.4168",
                        DashboardState.form_lat,
                    ),
                    _text_field(
                        "Longitud",
                        "lon",
                        "Ej. -3.7038",
                        DashboardState.form_lon,
                    ),
                    class_name="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4",
                ),
                rx.el.p(
                    "Si dejas las coordenadas vacías, se conservan las actuales o se estiman por ciudad.",
                    class_name="mt-2 text-xs font-medium text-gray-400",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=DashboardState.close_form,
                        class_name="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer",
                    ),
                    rx.el.button(
                        DashboardState.form_submit_label,
                        type="submit",
                        class_name="rounded-lg bg-violet-600 px-4 py-2 text-sm font-semibold text-white hover:bg-violet-700 transition-colors cursor-pointer",
                    ),
                    class_name="flex items-center justify-end gap-2 mt-6",
                ),
                on_submit=DashboardState.submit_form,
                class_name="p-5",
            ),
            class_name="relative w-full max-w-xl rounded-xl border border-gray-200 bg-white overflow-hidden",
        ),
        class_name=rx.cond(
            DashboardState.form_open,
            "fixed inset-0 z-50 flex items-center justify-center p-4",
            "hidden",
        ),
    )


def delete_confirm_modal() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_click=DashboardState.cancel_delete,
            class_name="absolute inset-0 bg-gray-900/40",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "triangle-alert", class_name="h-4 w-4 text-red-500"
                    ),
                    class_name="flex items-center justify-center size-8 rounded-lg border border-red-100 bg-red-100",
                ),
                rx.el.div(
                    rx.el.h3(
                        "Eliminar persona",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Esta acción no se puede deshacer.",
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 border-b border-gray-200 px-5 py-4",
            ),
            rx.el.div(
                rx.el.p(
                    f"¿Seguro que quieres eliminar a {DashboardState.delete_nombre}?",
                    class_name="text-sm font-medium text-gray-600",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DashboardState.cancel_delete,
                        class_name="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", class_name="h-4 w-4"),
                        "Eliminar",
                        on_click=DashboardState.confirm_delete,
                        class_name="flex items-center gap-2 rounded-lg bg-red-500 px-4 py-2 text-sm font-semibold text-white hover:bg-red-600 transition-colors cursor-pointer",
                    ),
                    class_name="flex items-center justify-end gap-2 mt-6",
                ),
                class_name="p-5",
            ),
            class_name="relative w-full max-w-md rounded-xl border border-gray-200 bg-white overflow-hidden",
        ),
        class_name=rx.cond(
            DashboardState.delete_open,
            "fixed inset-0 z-50 flex items-center justify-center p-4",
            "hidden",
        ),
    )
