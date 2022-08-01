
class NoSuchElementExeption(Exception):
    def __init__(self, name, tag, attributes):
        super().__init__("Error during parsing an element: "
                         f"Name :{name}\nTag :{tag}\nAttributes :{attributes} | "
                         "Maybe attributes are wrong or page wasn't load.",
                         )