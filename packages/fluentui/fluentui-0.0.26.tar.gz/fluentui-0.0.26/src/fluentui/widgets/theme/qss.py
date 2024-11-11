from dataclasses import dataclass, field
from typing import Self


@dataclass
class Qss:
    d: dict = field(default_factory=dict)

    def merge(self, a: 'dict | Qss') -> Self:
        self.d = self.join(a if isinstance(a, dict) else a.d, self.d)
        return self

    @classmethod
    def join(cls, dst: dict, src: dict) -> dict:
        for name, elem in dst.items():
            if isinstance(elem, dict):
                src[name] = cls.join(elem, src.get(name, {}))
            else:
                src[name] = elem
        return src

    def build(self, d: dict = None) -> str:
        if not (d := d or self.d):
            return ''

        base, elems = [], {}
        for k, v in d.items():
            if isinstance(v, dict):
                elems[k] = v
                continue
            base.append(f"    {k}: {v};")

        result = "{\n" + "\n".join(base) + "\n}"
        return result + ''.join(f"\n{k} {self.build(v)}" for k, v in elems.items())

    def __or__(self, other: 'dict | Qss') -> Self:
        return self.merge(other)
