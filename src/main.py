import uvicorn

from app.core.api_app import create_app

from app.config.settings import Config


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host=Config.HOST, port=int(Config.PORT))