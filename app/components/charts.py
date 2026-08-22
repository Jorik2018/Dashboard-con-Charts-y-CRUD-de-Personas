import reflex as rx
from app.states.dashboard_state import DashboardState

VIOLET = "#7c3aed"
BLUE = "#3b82f6"


def chart_card(
    title: str,
    subtitle: str,
    icon: str,
    badge: rx.Var | str,
    body: rx.Component,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(icon, class_name="h-4 w-4 text-violet-600"),
                    class_name="flex items-center justify-center size-8 rounded-lg border border-violet-100 bg-violet-50",
                ),
                rx.el.div(
                    rx.el.h3(
                        title, class_name="text-sm font-semibold text-gray-900"
                    ),
                    rx.el.p(
                        subtitle,
                        class_name="text-xs font-medium text-gray-500",
                    ),
                    class_name="flex flex-col min-w-0",
                ),
                class_name="flex items-center gap-3 min-w-0",
            ),
            rx.el.span(
                badge,
                class_name="w-fit shrink-0 rounded-full bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-600",
            ),
            class_name="flex items-center justify-between gap-3 border-b border-gray-200 px-5 py-4",
        ),
        body,
        class_name="flex flex-col w-full h-full rounded-xl border border-gray-200 bg-white overflow-hidden",
    )


def _legend_item(
    label: str, color: str, value: rx.Var, percent: rx.Var
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                class_name="size-2.5 rounded-full shrink-0",
                style={"backgroundColor": color},
            ),
            rx.el.span(label, class_name="text-sm font-medium text-gray-600"),
            class_name="flex items-center gap-2 min-w-0",
        ),
        rx.el.div(
            rx.el.span(value, class_name="text-sm font-semibold text-gray-900"),
            rx.el.span(
                f"{percent:.1f}%",
                class_name="text-xs font-medium text-gray-400",
            ),
            class_name="flex items-baseline gap-2",
        ),
        class_name="flex items-center justify-between gap-4 rounded-lg border border-gray-200 px-3 py-2",
    )


def gender_pie_chart() -> rx.Component:
    return chart_card(
        "Distribución por género",
        "Proporción de hombres y mujeres",
        "chart-pie",
        f"{DashboardState.total_personas} personas",
        rx.el.div(
            rx.el.div(
                rx.recharts.pie_chart(
                    rx.recharts.graphing_tooltip(
                        content_style={
                            "borderRadius": "0.75rem",
                            "border": "1px solid #e5e7eb",
                            "fontSize": "12px",
                            "fontWeight": "500",
                        }
                    ),
                    rx.recharts.pie(
                        data=DashboardState.distribucion_genero,
                        data_key="value",
                        name_key="name",
                        inner_radius="62%",
                        outer_radius="88%",
                        padding_angle=3,
                        stroke="#ffffff",
                        stroke_width=2,
                    ),
                    width="100%",
                    height=260,
                    min_width=280,
                ),
                rx.el.div(
                    rx.el.span(
                        DashboardState.total_personas,
                        class_name="text-2xl font-semibold text-gray-900 leading-none",
                    ),
                    rx.el.span(
                        "Total",
                        class_name="text-xs font-medium text-gray-400 uppercase tracking-wider",
                    ),
                    class_name="pointer-events-none absolute inset-0 flex flex-col items-center justify-center gap-1",
                ),
                class_name="relative w-full min-w-[280px]",
            ),
            rx.el.div(
                _legend_item(
                    "Hombres",
                    BLUE,
                    DashboardState.total_hombres,
                    DashboardState.porcentaje_hombres,
                ),
                _legend_item(
                    "Mujeres",
                    VIOLET,
                    DashboardState.total_mujeres,
                    DashboardState.porcentaje_mujeres,
                ),
                class_name="flex flex-col gap-2 w-full mt-2",
            ),
            class_name="flex flex-col w-full p-5",
        ),
    )


def birth_year_bar_chart() -> rx.Component:
    return chart_card(
        "Personas por año de nacimiento",
        "Conteo agrupado por año",
        "chart-column",
        f"Rango {DashboardState.rango_anios}",
        rx.el.div(
            rx.recharts.bar_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    stroke="#e5e7eb",
                ),
                rx.recharts.graphing_tooltip(
                    content_style={
                        "borderRadius": "0.75rem",
                        "border": "1px solid #e5e7eb",
                        "fontSize": "12px",
                        "fontWeight": "500",
                    },
                    cursor={"fill": "#f5f3ff"},
                ),
                rx.recharts.bar(
                    data_key="total",
                    name="Personas",
                    fill=VIOLET,
                    radius=[6, 6, 0, 0],
                ),
                rx.recharts.x_axis(
                    data_key="anio",
                    type_="category",
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    interval="preserveStartEnd",
                    custom_attrs={"fontSize": "12px"},
                ),
                rx.recharts.y_axis(
                    allow_decimals=False,
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    width=32,
                    custom_attrs={"fontSize": "12px"},
                ),
                data=DashboardState.personas_por_anio,
                bar_category_gap="25%",
                max_bar_size=48,
                margin={"left": 4, "right": 12, "top": 16, "bottom": 4},
                width="100%",
                height=260,
                min_width=300,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        class_name="size-2.5 rounded-full shrink-0",
                        style={"backgroundColor": VIOLET},
                    ),
                    rx.el.span(
                        "Personas por año",
                        class_name="text-sm font-medium text-gray-600",
                    ),
                    class_name="flex items-center gap-2",
                ),
                rx.el.span(
                    f"Año con más registros: {DashboardState.anio_con_mas_personas}",
                    class_name="text-xs font-medium text-gray-400",
                ),
                class_name="flex flex-wrap items-center justify-between gap-2 mt-2",
            ),
            class_name="flex flex-col w-full p-5",
        ),
    )
