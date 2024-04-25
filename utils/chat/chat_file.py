import os

import ujson as json
from chat import Chat


class ChatFile:
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self.chats: list[Chat] = []
        self.chat_data: dict[str, Chat] = {}
        self.FOLDER_LOCATION: str = f"{os.getcwd()}/data"
        self.__create_file()
        self.load_data()

    def __create_file(self) -> None:
        if not os.path.exists(f"{self.FOLDER_LOCATION}/{self.file_name}.json"):
            with open(f"{self.FOLDER_LOCATION}/{self.file_name}.json", "w") as json_file:
                json_file.write("{}")

    def load_chat(self, chat_name: str, chat_data: dict[str, any]) -> Chat:
        chat = Chat(id=chat_name, name=chat_data["chat_data"]["display_name"])
        chat.set_messages(chat_data["messages"])
        chat.set_chat_data(chat_data["chat_data"])
        return chat

    def load_data(self) -> None:
        self.chats.clear()
        with open(f"{self.FOLDER_LOCATION}/{self.file_name}.json", "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        for chat_name in data:
            self.add_chat(self.load_chat(chat_name, data[chat_name]))

    def save(self) -> None:
        with open(f"{self.FOLDER_LOCATION}/{self.file_name}.json", "w", encoding="utf-8") as json_file:
            json.dump(self.to_dict(), json_file, ensure_ascii=False, indent=4)

    def add_chat(self, chat: Chat):
        self.chats.append(chat)

    def to_dict(self) -> dict[str, dict[str, any]]:
        data = {}
        for chat in self.chats:
            data[chat.id] = chat.to_dict()
        return data
