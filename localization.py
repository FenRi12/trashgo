# localization.py
from typing import Optional
from database_users import get_user
from lang_uz import UZ

def get_user_lang(user_id: int) -> str:
    """
    Возвращает 'uz' или 'ru'. Если пользователя нет или поле не установлено — 'ru'.
    """
    user = get_user(user_id)
    if not user:
        return "ru"
    return (user.get("language") or "ru")

def L_text(original_text: str, user_id: Optional[int] = None, lang: Optional[str] = None) -> str:
    """
    Возвращает переведённый текст для пользователя (если lang == 'uz').
    - original_text: точная строка-ключ из кода
    - user_id: если указан, используется язык пользователя
    - lang: можно явно передать 'ru' или 'uz'
    Если перевода нет — возвращается original_text.
    """
    # Выбор языка
    if lang is None:
        if user_id is None:
            lang = "ru"
        else:
            lang = get_user_lang(user_id)

    if lang == "uz":
        return UZ.get(original_text, original_text)
    return original_text
