confirmation = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Учетная запись пользователя активирована.",
                        "data": {}
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
                        "message": "Не удалась активировать учетную запись, возможно срок жизни кода подтверждения истек повторите попытку.",
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
                        "message": "Срок жизни токена истек.",
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