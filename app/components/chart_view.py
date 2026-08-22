import reflex as rx
from app.components.charts import birth_year_bar_chart, gender_pie_chart
from app.components.stats import stats_row


def chart_view() -> rx.Component:
    return rx.el.div(
        stats_row(),
        rx.el.div(
            rx.el.div(
                gender_pie_chart(),
                class_name="flex-1 min-w-[300px]",
            ),
            rx.el.div(
                birth_year_bar_chart(),
                class_name="flex-1 min-w-[300px]",
            ),
            class_name="flex flex-col xl:flex-row gap-4 w-full",
        ),
        class_name="flex flex-col gap-4 w-full",
    )
