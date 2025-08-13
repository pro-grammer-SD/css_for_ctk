import tinycss2

class Parser:
    def __init__(self, data):
        self.rules = [
            rule for rule in tinycss2.parse_stylesheet(data, skip_whitespace=True)
            if rule.type == "qualified-rule"
        ]

    def get_selectors(self):
        return [tinycss2.serialize(rule.prelude).strip() for rule in self.rules]

    def get_decs_and_props(self, selector):
        for rule in self.rules:
            if tinycss2.serialize(rule.prelude).strip() == selector:
                decls = tinycss2.parse_declaration_list(rule.content, skip_whitespace=True, skip_comments=True)
                props = {}
                for d in decls:
                    if d.type == "declaration":
                        value_str = tinycss2.serialize(d.value).strip().strip('"').strip("'")
                        props[d.name.strip()] = value_str
                return props
        return {}
    