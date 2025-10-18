confirmation_email = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                            "isSuccess": True,
                            "message": "Отправлен код подтверждения на указанный email.",
                            "data": {}
                        }
                    }
                }
            },
        "400": {
            "description": "Ошибка на стороне сервиса.",
            "content": {
                "application_1/json": {
                    "example": {
                            "isSuccess": False,
                            "message": "Email не соответствует стандарту.",
                            "data": {}
                        }
                    },
                "application_2/json": {
                    "example": {
                            "isSuccess": False,
                            "message": "Не удалось отправить код подтверждения на указанный email, повторите попытку.",
                            "data": {}
                        }
                    }
                }
            },
        "401": {
            "description": "Ошибка токена доступа пользователя.",
            "content": {
                "answer_error_1/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "У вас нет доступа к данному запросу.",
                        "data": {}
                    }
                },
                "answer_error_2/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Токен пользователя не действителен.",
                        "data": {}
                    }
                },
                "answer_error_3/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Отсутствует токен авторизации пользователя.",
                        "data": {}
                    },
                "answer_error_4/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Получен токен не принадлежащий авторизованному пользователю.",
                        "data": {}
                    }
                },
                }
            }
        },
        "403": {
            "description": "Отсутствие сессии пользователя.",
            "content": {
                "answer_error_1/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Пользователь не авторизован.",
                        "data": {}
                    }
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