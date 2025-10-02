authorization = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Успешное выполнение запроса.",
                        "data": {
                            "access_token": "PDIGPJGPFB94357JKV;JBSD7JBLSFBNV;NDFLH873"
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Ошибка на стороне сервиса.",
            "content": {
                "answer_error/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Не удалось обновить токен доступа пользователя, повторите попытку.",
                        "data": {}
                    },
                }
            }
        },
        "401": {
            "description": "Ошибка на стороне сервиса.",
            "content": {
                "answer_error/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Логин или пароль не верен.",
                        "data": {}
                    },
                }
            }
        },
        "422": {
             "description": "Ошибка на стороне сервиса.",
            "content": {
                "answer_error_1/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Отсутствуют параметры запроса.",
                        "data": {}
                    }
                },
                "answer_error_2/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Параметры входа не соответствуют верным.",
                        "data": {}
                    }
                }
            }
        },
        "500": {
            "description": "Ошибка на стороне сервиса.",
            "content": {
                "answer_error_1/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Возникла ошибка исполнения процесса.",
                        "data": {}
                    }
                }
            }
        },
    }