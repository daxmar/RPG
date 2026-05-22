from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Type


@dataclass
class Entity:
    id: int
    name: str
    tags: List[str] = field(default_factory=list)


class EntityManager:
    def __init__(self):
        self._next_id = 1
        self.entities: Dict[int, Entity] = {}
        self.components: Dict[int, Dict[Type[Any], Any]] = {}

    def create_entity(self, name: str, tags: List[str] | None = None) -> Entity:
        eid = self._next_id
        self._next_id += 1
        e = Entity(id=eid, name=name, tags=tags or [])
        self.entities[eid] = e
        self.components[eid] = {}
        return e

    def add_component(self, entity: Entity, component: Any) -> None:
        ctype = type(component)
        self.components[entity.id][ctype] = component

    def get_component(self, entity: Entity, ctype: Type[Any]) -> Any:
        return self.components[entity.id][ctype]

    def has_component(self, entity: Entity, ctype: Type[Any]) -> bool:
        return ctype in self.components[entity.id]

