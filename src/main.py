import uvicorn

from src.core.api_app import create_app

from src.config.settings import Config


app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host=Config.HOST, port=int(Config.PORT))