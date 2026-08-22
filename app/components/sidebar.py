import reflex as rx
from app.states.dashboard_state import DashboardState, NavItem


def _nav_button(item: NavItem) -> rx.Component:
    return rx.el.button(
        rx.icon(
            item["icon"],
            class_name=rx.cond(
                DashboardState.active_view == item["key"],
                "h-4 w-4 text-violet-600 shrink-0",
                "h-4 w-4 text-gray-400 shrink-0 group-hover:text-gray-600",
            ),
        ),
        rx.el.div(
            rx.el.span(item["label"], class_name="text-sm font-semibold"),
            rx.el.span(
                item["description"],
                class_name="text-xs font-medium text-gray-400 leading-tight",
            ),
            class_name="flex flex-col items-start text-left min-w-0",
        ),
        on_click=lambda: DashboardState.set_view(item["key"]),
        class_name=rx.cond(
            DashboardState.active_view == item["key"],
            "group flex items-center gap-3 w-full rounded-lg border border-violet-200 bg-violet-50 px-3 py-2.5 text-violet-700 transition-colors cursor-pointer",
            "group flex items-center gap-3 w-full rounded-lg border border-transparent px-3 py-2.5 text-gray-700 hover:bg-gray-100 transition-colors cursor-pointer",
        ),
    )


def _brand() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("users", class_name="h-4 w-4 text-white"),
            class_name="flex items-center justify-center size-8 rounded-lg bg-violet-600",
        ),
        rx.el.div(
            rx.el.span(
                "Personas",
                class_name="text-sm font-semibold text-gray-900 leading-tight",
            ),
            rx.el.span(
                "Dashboard",
                class_name="text-xs font-medium text-gray-400 leading-tight",
            ),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-3 h-16 px-5 border-b border-gray-200",
    )


def _footer() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src="https://api.dicebear.com/9.x/notionists/svg?seed=personas-admin",
                class_name="size-8 rounded-full bg-gray-100",
            ),
            rx.el.div(
                rx.el.span(
                    "Ana Torres",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.span(
                    "Administradora",
                    class_name="text-xs font-medium text-gray-400",
                ),
                class_name="flex flex-col min-w-0",
            ),
            class_name="flex items-center gap-3",
        ),
        rx.icon("settings", class_name="h-4 w-4 text-gray-400"),
        class_name="flex items-center justify-between border-t border-gray-200 px-5 py-4",
    )


def sidebar_content() -> rx.Component:
    return rx.el.div(
        _brand(),
        rx.el.nav(
            rx.el.span(
                "Vistas",
                class_name="px-3 text-xs font-semibold uppercase tracking-wider text-gray-400",
            ),
            rx.el.div(
                rx.foreach(DashboardState.nav_items, _nav_button),
                class_name="flex flex-col gap-1 mt-2",
            ),
            class_name="flex flex-1 flex-col overflow-auto p-4",
        ),
        _footer(),
        class_name="flex flex-col h-full min-h-0 bg-white",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        sidebar_content(),
        class_name="hidden lg:flex flex-col w-64 shrink-0 h-screen sticky top-0 border-r border-gray-200 bg-white",
    )


def mobile_sidebar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            on_click=DashboardState.toggle_sidebar,
            class_name="absolute inset-0 bg-gray-900/40",
        ),
        rx.el.div(
            sidebar_content(),
            class_name="relative h-full w-72 border-r border-gray-200 bg-white",
        ),
        class_name=rx.cond(
            DashboardState.sidebar_open,
            "fixed inset-0 z-50 flex lg:hidden",
            "hidden",
        ),
    )
