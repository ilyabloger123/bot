from typing import Optional, Dict, Any
from dataclasses import dataclass
import sqlite3
from datetime import datetime

@dataclass
class UserSettings:
    """Модель настроек пользователя"""
    user_id: int
    default_password_length: int = 16
    default_word_count: int = 4
    default_separator: str = '-'
    theme: str = 'light'
    notification_enabled: bool = True
    auto_save: bool = False
    language: str = 'ru'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Конвертация в словарь"""
        return {
            'user_id': self.user_id,
            'default_password_length': self.default_password_length,
            'default_word_count': self.default_word_count,
            'default_separator': self.default_separator,
            'theme': self.theme,
            'notification_enabled': self.notification_enabled,
            'auto_save': self.auto_save,
            'language': self.language
        }


class SettingsDatabase:
    """База данных для настроек пользователей"""
    def __init__(self, db_path: str = 'user_settings.db') -> None:
        self.db_path = db_path
        self._init_database()

    def  _init_database(self):
        """Инициализация таблицы настроек"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    default_password_length INTEGER NOT NULL DEFAULT 16,
                    default_word_count INTEGER NOT NULL DEFAULT 4,
                    default_separator TEXT NOT NULL DEFAULT '-',
                    theme TEXT NOT NULL DEFAULT 'light',
                    notification_enabled INTEGER NOT NULL DEFAULT 1,
                    auto_save INTEGER NOT NULL DEFAULT 0,
                    language TEXT NOT NULL DEFAULT 'ru',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER NOT NULL PRIMARY KEY,
                    passwords_generated INTEGER DEFAULT 0,
                    saved_passwords_state INTEGER DEFAULT 0,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user_settings (user_id)
                )
            """)
            conn.commit()

    def get_settings(self, user_id: int) -> UserSettings:
        """Получение настроек пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM user_settings WHERE user_id = ?
            """, (user_id,))

            result = cursor.fetchone()
            if result:
                return UserSettings(*result)
            else:
                return self.create_default_settings(user_id)

    def create_default_settings(self, user_id: int) -> UserSettings:
        """Создание настроек по умолчанию"""
        settings = UserSettings(user_id)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO user_settings (
                    user_id, default_password_length, default_word_count,
                    default_separator, theme, notification_enabled,
                    auto_save, language
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                settings.default_password_length,
                settings.default_word_count,
                settings.default_separator,
                settings.theme,
                settings.notification_enabled,
                settings.auto_save,
                settings.language
            ))

            cursor.execute("""
                INSERT INTO user_stats (user_id) VALUES (?)
                
            """, (user_id,))
            conn.commit()
        return settings

    def update_settings(self, user_id: int, **kwargs) -> bool:
        """Обновление настроек пользователя"""
        if not kwargs:
            return False
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            for key, value in kwargs.items():
                if isinstance(value, bool):
                    kwargs[key] = int(value)
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            set_clause += ", updated_at = CURRENT_TIMESTAMP"

            query = f"""
                UPDATE user_settings
                SET {set_clause}
                WHERE user_id = ?
            """
            values = list(kwargs.values()) + [user_id]

            cursor.execute(query, values)
            conn.commit()

            return cursor.rowcount > 0

    def update_stats(self, user_id: int, generated: int = 0, saved: int = 0):
        """Обновление статистики пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE user_stats
                SET passwords_generated=passwords_generated+?,
                    saved_passwords_state=saved_passwords_state+?,
                    last_active=CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (generated, saved, user_id))
            conn.commit()

    def get_stats(self, user_id: int) -> Dict[str, Any]:
        """Получение статистики пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT passwords_generated, saved_passwords_state, last_active
                FROM user_stats WHERE user_id = ?
            """, (user_id,))

            result = cursor.fetchone()
            if result:
                return {
                    "generated":result[0],
                    "saved":result[1],
                    "last_active":result[2],
                }
            return {"generated": 0, "saved": 0, "last_active": None}
