# from pathlib import Path

# from fastapi import FastAPI
# from fastapi.responses import FileResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles

# BASE_DIR = Path(__file__).parent.resolve()
# ANGULAR_DIST_PATH = BASE_DIR / "browser"


# def configure_dev_web_ui(app: FastAPI):
#     @app.get("/")
#     async def redirect_to_dev_ui():
#         return RedirectResponse("/dev-ui")

#     @app.get("/dev-ui")
#     async def dev_ui():
#         return FileResponse(BASE_DIR / "browser/index.html")

#     app.mount("/", StaticFiles(directory=ANGULAR_DIST_PATH, html=True), name="static")
