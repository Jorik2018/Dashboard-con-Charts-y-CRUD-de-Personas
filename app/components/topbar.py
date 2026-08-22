import reflex as rx
from app.states.dashboard_state import DashboardState


def _view_tab(label: str, view_key: str, icon: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-3.5 w-3.5"),
        label,
        on_click=lambda: DashboardState.set_view(view_key),
        class_name=rx.cond(
            DashboardState.active_view == view_key,
            "flex items-center gap-2 rounded-md bg-white border border-gray-200 px-3 py-1.5 text-sm font-semibold text-violet-700 transition-colors cursor-pointer",
            "flex items-center gap-2 rounded-md border border-transparent px-3 py-1.5 text-sm font-medium text-gray-500 hover:text-gray-900 transition-colors cursor-pointer",
        ),
    )


def topbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", class_name="h-5 w-5 text-gray-600"),
                on_click=DashboardState.toggle_sidebar,
                class_name="lg:hidden flex items-center justify-center size-9 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors cursor-pointer",
            ),
            rx.el.div(
                rx.el.h1(
                    DashboardState.view_title,
                    class_name="text-base font-semibold text-gray-900 leading-tight",
                ),
                rx.el.p(
                    DashboardState.view_subtitle,
                    class_name="hidden sm:block text-xs font-medium text-gray-500",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0",
        ),
        rx.el.div(
            rx.el.div(
                _view_tab("Chart", "chart", "chart-pie"),
                _view_tab("Table", "table", "table"),
                _view_tab("Mapa", "map", "map"),
                class_name="flex items-center gap-1 rounded-lg bg-gray-100 p-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                rx.el.span("Nueva persona", class_name="hidden sm:inline"),
                on_click=DashboardState.open_create,
                class_name="flex items-center gap-2 rounded-lg bg-violet-600 px-3 py-2 text-sm font-semibold text-white hover:bg-violet-700 transition-colors cursor-pointer",
            ),
            class_name="flex items-center gap-3",
        ),
        class_name="sticky top-0 z-30 flex h-16 w-full items-center justify-between gap-4 border-b border-gray-200 bg-white/90 backdrop-blur-sm px-4 sm:px-6",
    )
