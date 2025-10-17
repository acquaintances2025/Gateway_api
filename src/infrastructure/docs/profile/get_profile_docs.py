profile = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                            "isSuccess": True,
                            "message": "Успешное выполнение запроса",
                            "data": {
                                "id": 109,
                                "uuid": "274f9b58-c604-4bb3-a233-ad2f17b56613",
                                "name": "Дмитрий",
                                "surname": "Вадимович",
                                "lastname": "Уранов",
                                "email": "i@dok2412.ru",
                                "number": "89999666229",
                                "age": 31,
                                "birthday": "24.12.1993 00:00:00",
                                "created_at": "12.10.2025 20:31:09",
                                "active_phone": False,
                                "active_email": False,
                                "active": True
                            }
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