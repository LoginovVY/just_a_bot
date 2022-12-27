import os
token = os.environ['TELEGRAM_TOKEN']
log_level = "INFO"
eng_dict = {
    "a": "ф", "b": "и", "c": "с", "d": "в", "e": "у", "f": "а", "g": "п", "h": "р", "i": "ш", "j": "о", "k": "л",
    "l": "д", "m": "ь", "n": "т", "o": "щ", "p": "з", "q": "й", "r": "к", "s": "ы", "t": "е", "u": "г", "v": "м",
    "w": "ц", "x": "ч", "y": "н", "z": "я", ",": "б", ".": "ю", "‘": "э", "'": "э", "[": "х", "]": "ъ", "\\": "ё",
    ";": "ж", ":": "ж", '"': "Э", "<": "б", ">":"Ю", "|":"Ё", "{":"Х", "}":"Ъ", "^":","
}

rus_dict = {v:k for k, v in eng_dict.items()}

len_command = len("\convert_layout ")
