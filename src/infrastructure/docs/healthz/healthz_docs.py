healthz = logout = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Успешное выполнение запроса.",
                        "data": {}
                    }
                }
            }
        }
    }