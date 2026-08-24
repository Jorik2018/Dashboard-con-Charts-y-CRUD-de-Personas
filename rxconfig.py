import reflex as rx
import os

config = rx.Config(
    app_name="app",
    plugins=[rx.plugins.SitemapPlugin(), rx.plugins.TailwindV4Plugin()],


    show_built_with_reflex=False,

    api_url=os.getenv("API_URL", "http://localhost:3000"),
    deploy_url=os.getenv("DEPLOY_URL", "http://localhost:3000"),
)
