from parse import Parser
import re

def apply_styles(data):
    p = Parser(data)
    selectors = p.get_selectors()

    def to_value(v):
        if not isinstance(v, str):
            return v
        s = v.strip()
        ls = s.lower()
        if ls in ("true", "false"):
            return ls == "true"
        if re.fullmatch(r"[+-]?\d+", s):
            return int(s)
        if re.fullmatch(r"[+-]?\d*\.\d+", s):
            return float(s)
        return s

    def collect_all_widgets(root):
        out = []
        stack = [root]
        while stack:
            w = stack.pop()
            out.append(w)
            try:
                children = w.winfo_children()
            except Exception:
                children = []
            stack.extend(children)
        return out

    def decorator(cls: type):
        orig_init = cls.__init__

        def new_init(self, *args, **kwargs):
            orig_init(self, *args, **kwargs)
            all_widgets = collect_all_widgets(self)
            layout_methods = {
                "place": lambda w, props: w.place(**props),
                "pack":  lambda w, props: w.pack(**props),
                "grid":  lambda w, props: w.grid(**props),
            }

            for selector in selectors:
                if not selector:
                    continue
                base = selector
                pseudo = None
                if ":" in selector:
                    base, pseudo = selector.split(":", 1)
                props_raw = p.get_decs_and_props(selector)
                if not props_raw:
                    continue
                props = {k: to_value(v) for k, v in props_raw.items()}

                if base.startswith("#"):
                    name = base[1:]
                    if hasattr(self, name):
                        widget = getattr(self, name)
                        if pseudo in layout_methods:
                            try:
                                layout_methods[pseudo](widget, props)
                            except Exception:
                                pass
                        else:
                            try:
                                widget.configure(**props)
                            except Exception:
                                pass
                    continue

                is_main = base == cls.__name__ or any(base == b.__name__ for b in cls.mro())
                if is_main:
                    if "title" in props:
                        try:
                            self.title(props.pop("title"))
                        except Exception:
                            pass
                    if "geometry" in props:
                        try:
                            self.geometry(props.pop("geometry"))
                        except Exception:
                            pass
                    if props:
                        try:
                            self.configure(**props)
                        except Exception:
                            pass
                    continue

                base_lower = base.lower()
                for w in all_widgets:
                    if base_lower in w.__class__.__name__.lower():
                        if pseudo in layout_methods:
                            try:
                                layout_methods[pseudo](w, props)
                            except Exception:
                                pass
                        else:
                            try:
                                w.configure(**props)
                            except Exception:
                                pass

        cls.__init__ = new_init
        return cls

    return decorator
