import reflex as rx
from app.states.dashboard_state import DashboardState


def _stat_card(
    label: str, value: rx.Var | str, icon: str, hint: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                label,
                class_name="text-xs font-semibold uppercase tracking-wider text-gray-400",
            ),
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-violet-600"),
                class_name="flex items-center justify-center size-8 rounded-lg bg-violet-50 border border-violet-100",
            ),
            class_name="flex items-start justify-between gap-2",
        ),
        rx.el.p(value, class_name="mt-3 text-2xl font-semibold text-gray-900"),
        rx.el.p(hint, class_name="text-xs font-medium text-gray-500"),
        class_name="w-full rounded-xl border border-gray-200 bg-white p-4",
    )


def stats_row() -> rx.Component:
    return rx.el.div(
        _stat_card(
            "Total",
            DashboardState.total_personas,
            "users",
            "Personas registradas",
        ),
        _stat_card(
            "Hombres", DashboardState.total_hombres, "user", "Género masculino"
        ),
        _stat_card(
            "Mujeres",
            DashboardState.total_mujeres,
            "user-round",
            "Género femenino",
        ),
        _stat_card(
            "Años",
            DashboardState.anios_distintos,
            "calendar",
            "Años de nacimiento",
        ),
        class_name="grid grid-cols-2 md:grid-cols-4 gap-4 w-full",
    )
