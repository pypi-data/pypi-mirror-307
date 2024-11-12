from pydantic import BaseModel
from typing import TYPE_CHECKING
from kraph.vars import current_ontology, current_graph
import dataclasses

from rath.turms.utils import get_attributes_or_error


if TYPE_CHECKING:
    from kraph.api.schema import Entity


@dataclasses.dataclass
class IntermediateInstanceRelation:
    left: "EntityTrait"
    kind: "LinkedExpressionTrait"

    def __or__(self, other):
        from kraph.api.schema import create_entity_relation

        if isinstance(other, EntityTrait):
            return create_entity_relation(left=self.left, right=other, kind=self.kind)
        raise NotImplementedError


class LinkedExpressionTrait(BaseModel):
    def create_entity(self) -> "Entity":
        from kraph.api.schema import create_entity

        """Creates an entity with a name


        """
        id = get_attributes_or_error(self, "id")
        return create_entity(id)

    def __call__(self, *args, **kwargs):
        return self.create_entity(*args, **kwargs)

    def __or__(self, other):
        raise NotImplementedError

    def __str__(self):
        return self.name


class ExpressionTrait(BaseModel):
    def __or__(self, other):
        raise NotImplementedError

    def __str__(self):
        return getattr(self, "label", super().__str__())


class EntityTrait(BaseModel):
    def __or__(self, other):
        if isinstance(other, LinkedExpressionTrait):
            return IntermediateInstanceRelation(self, other)
        raise NotImplementedError

    def set(self, metric: "LinkedExpressionTrait", value: float, **kwargs):
        from kraph.api.schema import create_entity_metric, ExpressionKind

        assert isinstance(
            metric, LinkedExpressionTrait
        ), "Metric must be a LinkedExpressionTrait"
        (
            get_attributes_or_error(metric, "kind") == ExpressionKind.METRIC,
            "Expression must be a METRIC",
        )

        return create_entity_metric(entity=self, metric=metric, value=value, **kwargs)

    def subject_to(self, **kwargs):
        from kraph.api.schema import (
            create_protocol_step,
            ProtocolStepInput,
            ExpressionKind,
        )

        return create_protocol_step(input=ProtocolStepInput(entity=self, **kwargs))


class EntityRelationTrait(BaseModel):
    def __or__(self, other):
        if isinstance(other, LinkedExpressionTrait):
            return IntermediateInstanceRelation(self.right, other)
        raise NotImplementedError

    def set(self, metric: "LinkedExpressionTrait", value: float):
        from kraph.api.schema import create_relation_metric, ExpressionKind

        assert isinstance(
            metric, LinkedExpressionTrait
        ), "Metric must be a LinkedExpressionTrait"
        (
            get_attributes_or_error(metric, "kind") == ExpressionKind.RELATION_METRIC,
            "Expression must be a RELATION_METRIC",
        )

        return create_relation_metric(relation=self, metric=metric, value=value)


class OntologyTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_ontology.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_ontology.reset(self._token)


class GraphTrait(BaseModel):
    _token = None

    def __enter__(self):
        self._token = current_graph.set(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        current_graph.reset(self._token)
