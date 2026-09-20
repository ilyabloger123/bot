import secrets
import string
import random
from typing import Optional, List

class PasswordGenerator:
    def __init__(self):
        self.word_list = self._load_word_list()

    def _load_word_list(self) -> List[str]:
        """Загрузка списка слов для запоминающихся паролей"""
        # Можно расширить этот список
        words = [
            # Животные
            'tiger', 'dragon', 'eagle', 'panther', 'wolf', 'lion', 'fox', 'bear',
            'hawk', 'falcon', 'shark', 'whale', 'dolphin', 'octopus',

            # Природа
            'ocean', 'mountain', 'forest', 'river', 'sunset', 'thunder', 'storm',
            'rainbow', 'galaxy', 'comet', 'planet', 'star', 'moon', 'sun',

            # Эмоции и состояния
            'victory', 'courage', 'wisdom', 'serenity', 'harmony', 'peace',
            'energy', 'passion', 'freedom', 'dream', 'hope', 'joy',

            # Технологии
            'quantum', 'digital', 'cyber', 'neural', 'matrix', 'binary',
            'code', 'algorithm', 'network', 'data', 'cloud', 'server',

            # Мифология и фэнтези
            'phoenix', 'unicorn', 'wizard', 'sorcerer', 'knight', 'dwarf',
            'elf', 'goblin', 'troll', 'witch', 'warlock', 'necromancer',

            # Музыка
            'guitar', 'piano', 'violin', 'symphony', 'melody', 'rhythm',
            'harmony', 'note', 'chord', 'scale', 'octave',

            # Цвета
            'scarlet', 'crimson', 'emerald', 'sapphire', 'amber', 'violet',
            'indigo', 'turquoise', 'golden', 'silver', 'bronze',

            # Профессии
            'explorer', 'pioneer', 'inventor', 'scientist', 'artist', 'poet',
            'warrior', 'guardian', 'protector', 'messenger', 'traveler',

            # Еда и напитки
            'chocolate', 'caramel', 'espresso', 'cappuccino', 'honey',
            'caramel', 'vanilla', 'cinnamon', 'pepper', 'saffron',

            # Города и места
            'atlantis', 'olympus', 'camelot', 'valhalla', 'avalon',
            'shangrila', 'utopia', 'elysium', 'nirvana'
        ]
        return words

    @staticmethod
    def generate_password(
            length: int = 16,
            use_digits: bool = True,
            use_special: bool = True,
            use_uppercase: bool = True,
            use_lowercase: bool = True,
            exclude_similar: bool = True,
    ) -> Optional[str]:
        """Генерация безопасного пароля"""
        characters = ""

        if use_digits:
            characters += string.digits
        if use_special:
            characters += string.punctuation
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_lowercase:
            characters += string.ascii_lowercase

        if not characters:
            return None

        if exclude_similar:
            similar_chars = 'il1Lo0O'
            characters = "".join(c for c in characters if c not in similar_chars)
        password = []
        if use_lowercase and string.ascii_lowercase:
            password.append(secrets.choice(string.ascii_lowercase))

        if use_uppercase and string.ascii_uppercase:
            password.append(secrets.choice(string.ascii_uppercase))

        if use_digits and string.digits:
            password.append(secrets.choice(string.digits))

        if use_special and string.punctuation:
            password.append(secrets.choice(string.punctuation))

        remaining_length = length - len(password)
        if remaining_length > 0:
            password.extend(secrets.choice(characters) for _ in range(remaining_length))

        secrets.SystemRandom().shuffle(password)
        return ''.join(password)

    def generate_memorable_password(
            self,
            word_count: int = 4,
            separator: str = "-",
            capitalise: bool = False,
            add_number:bool = False,
            add_special: bool = False
    ) -> str:
        """Генерация запоминающегося пароля"""
        word_count = max(2, min(6, word_count))
        selected_words = secrets.SystemRandom().sample(self.word_list, word_count)
        if capitalise:
            selected_words = [word.capitalize() for word in selected_words]
        password = separator.join(selected_words)
        if add_number:
            password += str(secrets.randbelow(100))
        if add_special:
            password += secrets.choice("!@#$%^&*")
        return password

    def generate_pronounceable_password(self, length: int = 12) -> str:
        """Генерация произносимого пароля"""
        vowels = "aeiou"
        consonants = "bcdfghjklmnpqrstvwxyz"
        password = []
        for i in range(length):
            if i % 2 == 0:
                password.append(secrets.choice(consonants))
            else:
                password.append(secrets.choice(vowels))
        for i in range(len(password) // 3):
            idx = secrets.randbelow(len(password))
            password[idx] = password[idx].upper()
        password.append(str(secrets.randbelow(10)))
        return "".join(password)

    def check_password_strength(self, password: str) -> dict:
        """Проверка силы пароля"""
        score = 0
        feedback = []

        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("❌ Слишком короткий пароль")

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        if has_upper and has_lower:
            score += 1
        else:
            feedback.append("⚠️ Добавьте и заглавные и строчные буквы")
        if has_digit:
            score += 1
        else:
            feedback.append("⚠️ Добавьте цифры")
        if has_special:
            score += 1
        else:
            feedback.append("⚠️ Добавьте символы")
        if score >= 5:
            strength = "🛡️ Очень сильный"
        elif score >= 4:
            strength = "🔐️ Сильный"
        elif score >= 3:
            strength = "🔒 Средний"
        else:
            strength = "⚠️ Слабый"
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback,
            "length": len(password),
            "has_upper": has_upper,
            "has_lower": has_lower,
            "has_digit": has_digit,
            "has_special": has_special
        }

