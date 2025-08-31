from typing import List, Dict, Any


class Button:
    def __init__(self, type: str, text: str, payload: str = None, url: str = None):
        self.type = type
        self.text = text
        self.payload = payload
        self.url = url

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "type": self.type,
            "text": self.text,
        }
        if self.payload is not None:
            data["payload"] = self.payload
        if self.url is not None:
            data["url"] = self.url
        return data


class InlineKeyboard:
    def __init__(self):
        self._rows: List[List[Button]] = []

    def row(self, *buttons: Button) -> "InlineKeyboard":
        self._rows.append(list(buttons))
        return self

    def callback(self, text: str, payload: str) -> Button:
        return Button(type="callback", text=text, payload=payload)

    def link(self, text: str, url: str) -> Button:
        return Button(type="link", text=text, url=url)

    def to_attachment(self) -> Dict[str, Any]:
        return {
            "type": "inline_keyboard",
            "payload": {
                "buttons": [[b.to_dict() for b in row] for row in self._rows]
            },
        }
