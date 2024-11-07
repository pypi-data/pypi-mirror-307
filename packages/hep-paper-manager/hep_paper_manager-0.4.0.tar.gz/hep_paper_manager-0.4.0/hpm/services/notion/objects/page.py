from dataclasses import dataclass, field

from .page_properties import ALL_PAGE_PROPERTIES


@dataclass
class Page:
    id: str | None = None
    title: str | None = None
    url: str | None = None
    properties: dict = field(default_factory=dict)

    @classmethod
    def from_response(cls, data: dict):
        title = None
        properties = {}
        for k, v in data["properties"].items():
            if v["type"] in ALL_PAGE_PROPERTIES:
                properties[k] = ALL_PAGE_PROPERTIES[v["type"]].from_dict(v)

            if v["type"] == "title" and len(v["title"]) > 0:
                title = v["title"][0]["text"]["content"]

        return cls(
            id=data["id"],
            title=title,
            url=data["url"],
            properties=properties,
        )

    @classmethod
    def from_cache(cls, data: dict):
        return cls(
            id=data["id"],
            title=data["title"],
            url=data["url"],
            properties={
                k: ALL_PAGE_PROPERTIES[v["type"]](value=v["value"], id=v["id"])
                for k, v in data["properties"].items()
            },
        )

    def as_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "properties": {k: v.as_dict() for k, v in self.properties.items()},
        }
