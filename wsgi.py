import os
from app import create_app

app = create_app()


if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "production")
    port = os.getenv("PORT", 5000)
    app.run(host="0.0.0.0", port=port, debug=(env == "development"))
        