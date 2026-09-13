import json
from typing import Dict, List
from config import Config
from utils.encryption import EncryptionManager


class PasswordStorage:
    def __init__(self):
        self.encrypt_manager = EncryptionManager()

    def load_user_passwords(self, user_id: int) -> Dict[str, str]:
        """Загрузка паролей пользователя"""
        try:
            with open(Config.PASSWORD_FILE, "r", encoding="utf-8") as file:
                all_data = json.load(file)
                user_data = all_data.get(str(user_id), {})

                decrypted_data = {}
                for site, encrypted_password in user_data.items():
                    try:
                        decrypted_data[site] = self.encrypt_manager.decrypt(encrypted_password)
                    except Exception as e:
                        print(f"Ошибка расшифровки пароля для {site}: {e}")
                        continue
                return decrypted_data
        except (FileNotFoundError, json.decoder.JSONDecodeError, KeyError):
            return {}

    def save_user_passwords(self, user_id: int, site: str, password: str) -> bool:
        """Сохранение пароля"""
        try:
            try:
                with open(Config.PASSWORD_FILE, "r", encoding="utf-8") as file:
                    all_data = json.load(file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                all_data = {}

            encrypted_password = self.encrypt_manager.encrypt(password)

            if str(user_id) not in all_data:
                all_data[str(user_id)] = {}

            all_data[str(user_id)][site] = encrypted_password

            with open(Config.PASSWORD_FILE, "w", encoding="utf-8") as file:
                json.dump(all_data, file, indent=4, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Ошибка сохранения пароля: {e}")
            return False

    def delete_password(self, user_id: int, site: str) -> bool:
        """Удаление пароля"""
        try:
            with open(Config.PASSWORD_FILE, "r", encoding="utf-8") as file:
                all_data = json.load(file)

            user_key = str(user_id)
            if site in all_data[user_key]:
                del all_data[user_key][site]
            else:
                raise Exception("Данные по сайту не найдены")

            # if not all_data[user_key]:
            #     del all_data[user_key]

            with open(Config.PASSWORD_FILE, "w", encoding="utf-8") as file:
                json.dump(all_data, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка удаления пароля: {e}")
            return False

    def get_user_sites(self, user_id: int) -> List[str]:
        """Получение списка сайтов пользователя"""
        passwords = self.load_user_passwords(user_id)
        return list(passwords.keys())
