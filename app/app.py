import reflex as rx
from app.components.sidebar import sidebar, mobile_sidebar
from app.components.map_view import map_view
from app.components.topbar import topbar
from app.components.chart_view import chart_view
from app.components.table_view import table_view
from app.states.dashboard_state import DashboardState
from app.controllers.people_controller import fastapi_app

def content() -> rx.Component:
    return rx.el.div(
        rx.match(
            DashboardState.active_view,
            ("chart", chart_view()),
            ("map", map_view()),
            table_view(),
        ),
        class_name="flex flex-col gap-6 w-full min-w-0 p-4 sm:p-6",
    )


def index() -> rx.Component:
    return rx.el.main(
        mobile_sidebar(),
        sidebar(),
        rx.el.div(
            topbar(),
            content(),
            class_name="flex flex-1 w-full min-w-0 flex-col",
        ),
        class_name="flex min-h-screen w-full bg-gray-50 font-['Inter'] text-gray-900",
    )


# app = rx.App(
#     theme=rx.theme(appearance="light"),
#     head_components=[
#         rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
#         rx.el.link(
#             rel="preconnect",
#             href="https://fonts.gstatic.com",
#             cross_origin="",
#         ),
#         rx.el.link(
#             href="https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap",
#             rel="stylesheet",
#         ),
#         rx.el.link(
#             rel="stylesheet",
#             href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
#         ),
#     ],
# )
app = rx.App(
    api_transformer=[fastapi_app],
    theme=rx.theme(appearance="light"),
    # head_components=[
    #     rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    #     rx.el.link(
    #         rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
    #     ),
    #     rx.el.link(
    #         href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
    #         rel="stylesheet",
    #     ),
    # ],
)
app.add_page(index, route="/",on_load=DashboardState.load_people)
app.add_page(rx.text("Hi" ), route="/hi")
# Create a Reflex app with the FastAPI app as the API transformer