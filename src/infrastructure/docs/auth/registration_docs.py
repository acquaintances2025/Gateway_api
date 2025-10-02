registration = {
        "200": {
            "description": "Успешное выполнение запроса",
            "content": {
                "application/json": {
                    "example": {
                        "isSuccess": True,
                        "message": "Код подтверждения успешно отправлен",
                        "data": {}
                    }
                }
            }
        },
        "400": {
            "description": "Ошибка на стороне сервиса.",
            "content": {
                "answer_error_1/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Отсутствует обязательный параметр (номер телефона/email) при регистрации.",
                        "data": {}
                    },
                },
                "answer_error_2/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Введенные пароли не совпадают.",
                        "data": {}
                    },
                },
                "answer_error_3/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Нарушение правил общепринятого стандарта паролей.",
                        "data": {}
                    },
                },
                "answer_error_4/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Email не соответствует стандарту",
                        "data": {}
                    },
                },
                "answer_error_5/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "Данный пользователь уже зарегистрирован.",
                        "data": {}
                    },
                },
                "answer_error_6/json": {
                    "example": {
                        "isSuccess": False,
                        "message": "В процессе отправки письма произошла ошибка.",
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

