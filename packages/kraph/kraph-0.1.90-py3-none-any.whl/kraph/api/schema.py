from kraph.rath import KraphRath
from enum import Enum
from kraph.traits import (
    ExpressionTrait,
    EntityTrait,
    EntityRelationTrait,
    LinkedExpressionTrait,
    GraphTrait,
    OntologyTrait,
)
from pydantic import Field, ConfigDict, BaseModel
from datetime import datetime
from typing import Any, List, Tuple, Optional, Literal
from rath.scalars import ID
from kraph.funcs import execute, aexecute


class ExpressionKind(str, Enum):
    MEASUREMENT = "MEASUREMENT"
    RELATION = "RELATION"
    ENTITY = "ENTITY"
    METRIC = "METRIC"
    RELATION_METRIC = "RELATION_METRIC"
    CONCEPT = "CONCEPT"


class MetricDataType(str, Enum):
    INT = "INT"
    FLOAT = "FLOAT"
    DATETIME = "DATETIME"
    STRING = "STRING"
    CATEGORY = "CATEGORY"
    BOOLEAN = "BOOLEAN"
    THREE_D_VECTOR = "THREE_D_VECTOR"
    TWO_D_VECTOR = "TWO_D_VECTOR"
    ONE_D_VECTOR = "ONE_D_VECTOR"
    FOUR_D_VECTOR = "FOUR_D_VECTOR"
    N_VECTOR = "N_VECTOR"


class LinkedExpressionFilter(BaseModel):
    graph: Optional[ID] = None
    search: Optional[str] = None
    pinned: Optional[bool] = None
    kind: Optional[ExpressionKind] = None
    ids: Optional[Tuple[ID, ...]] = None
    and_: Optional["LinkedExpressionFilter"] = Field(alias="AND", default=None)
    or_: Optional["LinkedExpressionFilter"] = Field(alias="OR", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class OffsetPaginationInput(BaseModel):
    offset: int
    limit: int
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class EntityFilter(BaseModel):
    graph: Optional[ID] = None
    kind: Optional[ID] = None
    ids: Optional[Tuple[ID, ...]] = None
    linked_expression: Optional[ID] = Field(alias="linkedExpression", default=None)
    search: Optional[str] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class GraphPaginationInput(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class StructureRelationInput(BaseModel):
    left: "Structure"
    right: "Structure"
    kind: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class Structure(BaseModel):
    identifier: str
    id: ID
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ProtocolStepInput(BaseModel):
    template: ID
    entity: ID
    reagent_mappings: Tuple["ReagentMappingInput", ...] = Field(alias="reagentMappings")
    value_mappings: Tuple["VariableInput", ...] = Field(alias="valueMappings")
    performed_at: Optional[datetime] = Field(alias="performedAt", default=None)
    performed_by: Optional[ID] = Field(alias="performedBy", default=None)
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class ReagentMappingInput(BaseModel):
    reagent: ID
    volume: int
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class VariableInput(BaseModel):
    key: str
    value: str
    model_config = ConfigDict(
        frozen=True, extra="forbid", populate_by_name=True, use_enum_values=True
    )


class LinkedExpressionGraph(GraphTrait, BaseModel):
    typename: Optional[Literal["Graph"]] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    typename: Optional[Literal["Ontology"]] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class LinkedExpressionExpression(ExpressionTrait, BaseModel):
    typename: Optional[Literal["Expression"]] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: LinkedExpressionExpressionOntology
    model_config = ConfigDict(frozen=True)


class LinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Optional[Literal["LinkedExpression"]] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: LinkedExpressionGraph
    kind: ExpressionKind
    expression: LinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionGraph(GraphTrait, BaseModel):
    typename: Optional[Literal["Graph"]] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpressionOntology(OntologyTrait, BaseModel):
    typename: Optional[Literal["Ontology"]] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ListLinkedExpressionExpression(ExpressionTrait, BaseModel):
    typename: Optional[Literal["Expression"]] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: ListLinkedExpressionExpressionOntology
    model_config = ConfigDict(frozen=True)


class ListLinkedExpression(LinkedExpressionTrait, BaseModel):
    typename: Optional[Literal["LinkedExpression"]] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    graph: ListLinkedExpressionGraph
    kind: ExpressionKind
    expression: ListLinkedExpressionExpression
    model_config = ConfigDict(frozen=True)


class Graph(GraphTrait, BaseModel):
    typename: Optional[Literal["Graph"]] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepTemplate(BaseModel):
    typename: Optional[Literal["ProtocolStepTemplate"]] = Field(
        alias="__typename", default="ProtocolStepTemplate", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappingsReagent(BaseModel):
    typename: Optional[Literal["Reagent"]] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStepReagentmappings(BaseModel):
    typename: Optional[Literal["ReagentMapping"]] = Field(
        alias="__typename", default="ReagentMapping", exclude=True
    )
    reagent: ProtocolStepReagentmappingsReagent
    model_config = ConfigDict(frozen=True)


class ProtocolStepForreagent(BaseModel):
    typename: Optional[Literal["Reagent"]] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class ProtocolStep(BaseModel):
    typename: Optional[Literal["ProtocolStep"]] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    id: ID
    template: ProtocolStepTemplate
    reagent_mappings: Tuple[ProtocolStepReagentmappings, ...] = Field(
        alias="reagentMappings"
    )
    for_reagent: Optional[ProtocolStepForreagent] = Field(
        default=None, alias="forReagent"
    )
    model_config = ConfigDict(frozen=True)


class ExpressionOntology(OntologyTrait, BaseModel):
    typename: Optional[Literal["Ontology"]] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class Expression(ExpressionTrait, BaseModel):
    typename: Optional[Literal["Expression"]] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    label: str
    ontology: ExpressionOntology
    model_config = ConfigDict(frozen=True)


class EntityRelationLeft(EntityTrait, BaseModel):
    typename: Optional[Literal["Entity"]] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelationRight(EntityTrait, BaseModel):
    typename: Optional[Literal["Entity"]] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelationLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Optional[Literal["LinkedExpression"]] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class EntityRelation(EntityRelationTrait, BaseModel):
    typename: Optional[Literal["EntityRelation"]] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    id: ID
    left: EntityRelationLeft
    right: EntityRelationRight
    linked_expression: EntityRelationLinkedexpression = Field(alias="linkedExpression")
    model_config = ConfigDict(frozen=True)


class ReagentExpression(ExpressionTrait, BaseModel):
    typename: Optional[Literal["Expression"]] = Field(
        alias="__typename", default="Expression", exclude=True
    )
    id: ID
    model_config = ConfigDict(frozen=True)


class Reagent(BaseModel):
    typename: Optional[Literal["Reagent"]] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    id: ID
    expression: Optional[ReagentExpression] = Field(default=None)
    lot_id: str = Field(alias="lotId")
    model_config = ConfigDict(frozen=True)


class EntityLinkedexpression(LinkedExpressionTrait, BaseModel):
    typename: Optional[Literal["LinkedExpression"]] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    id: ID
    label: str
    model_config = ConfigDict(frozen=True)


class Entity(EntityTrait, BaseModel):
    typename: Optional[Literal["Entity"]] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    id: ID
    label: str
    linked_expression: EntityLinkedexpression = Field(alias="linkedExpression")
    model_config = ConfigDict(frozen=True)


class Ontology(OntologyTrait, BaseModel):
    typename: Optional[Literal["Ontology"]] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    id: ID
    name: str
    model_config = ConfigDict(frozen=True)


class LinkExpressionMutation(BaseModel):
    link_expression: LinkedExpression = Field(alias="linkExpression")

    class Arguments(BaseModel):
        expression: ID
        graph: ID

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n    }\n  }\n}\n\nmutation LinkExpression($expression: ID!, $graph: ID!) {\n  linkExpression(input: {expression: $expression, graph: $graph}) {\n    ...LinkedExpression\n  }\n}"


class CreateGraphMutation(BaseModel):
    create_graph: Graph = Field(alias="createGraph")

    class Arguments(BaseModel):
        name: str

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n}\n\nmutation CreateGraph($name: String!) {\n  createGraph(input: {name: $name}) {\n    ...Graph\n  }\n}"


class CreateProtocolStepMutation(BaseModel):
    create_protocol_step: ProtocolStep = Field(alias="createProtocolStep")

    class Arguments(BaseModel):
        input: ProtocolStepInput

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n  }\n  reagentMappings {\n    reagent {\n      id\n    }\n  }\n  forReagent {\n    id\n  }\n}\n\nmutation CreateProtocolStep($input: ProtocolStepInput!) {\n  createProtocolStep(input: $input) {\n    ...ProtocolStep\n  }\n}"


class CreateExpressionMutation(BaseModel):
    create_expression: Expression = Field(alias="createExpression")

    class Arguments(BaseModel):
        label: str
        ontology: Optional[ID] = Field(default=None)
        purl: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)
        color: Optional[List[int]] = Field(default=None)
        metric_kind: Optional[MetricDataType] = Field(alias="metricKind", default=None)
        kind: ExpressionKind

    class Meta:
        document = "fragment Expression on Expression {\n  id\n  label\n  ontology {\n    id\n    name\n  }\n}\n\nmutation CreateExpression($label: String!, $ontology: ID, $purl: String, $description: String, $color: [Int!], $metricKind: MetricDataType, $kind: ExpressionKind!) {\n  createExpression(\n    input: {label: $label, ontology: $ontology, description: $description, purl: $purl, color: $color, kind: $kind, metricKind: $metricKind}\n  ) {\n    ...Expression\n  }\n}"


class CreateEntityRelationMutation(BaseModel):
    create_entity_relation: EntityRelation = Field(alias="createEntityRelation")

    class Arguments(BaseModel):
        left: ID
        right: ID
        kind: ID

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n  }\n  right {\n    id\n  }\n  linkedExpression {\n    id\n  }\n}\n\nmutation CreateEntityRelation($left: ID!, $right: ID!, $kind: ID!) {\n  createEntityRelation(input: {left: $left, right: $right, kind: $kind}) {\n    ...EntityRelation\n  }\n}"


class CreateRoiEntityRelationMutation(BaseModel):
    create_structure_relation: EntityRelation = Field(alias="createStructureRelation")

    class Arguments(BaseModel):
        input: StructureRelationInput

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n  }\n  right {\n    id\n  }\n  linkedExpression {\n    id\n  }\n}\n\nmutation CreateRoiEntityRelation($input: StructureRelationInput!) {\n  createStructureRelation(input: $input) {\n    ...EntityRelation\n  }\n}"


class CreateReagentMutation(BaseModel):
    create_reagent: Reagent = Field(alias="createReagent")

    class Arguments(BaseModel):
        expression: ID
        lot_id: str = Field(alias="lotId")

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n  }\n  lotId\n}\n\nmutation CreateReagent($expression: ID!, $lotId: String!) {\n  createReagent(input: {expression: $expression, lotId: $lotId}) {\n    ...Reagent\n  }\n}"


class CreateEntityMetricMutation(BaseModel):
    create_entity_metric: Entity = Field(alias="createEntityMetric")

    class Arguments(BaseModel):
        entity: ID
        metric: ID
        value: Any
        timepoint: Optional[datetime] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n  }\n}\n\nmutation CreateEntityMetric($entity: ID!, $metric: ID!, $value: Metric!, $timepoint: DateTime) {\n  createEntityMetric(\n    input: {entity: $entity, metric: $metric, value: $value, timepoint: $timepoint}\n  ) {\n    ...Entity\n  }\n}"


class CreateRelationMetricMutation(BaseModel):
    create_relation_metric: EntityRelation = Field(alias="createRelationMetric")

    class Arguments(BaseModel):
        relation: ID
        metric: ID
        value: Any
        timepoint: Optional[datetime] = Field(default=None)

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n  }\n  right {\n    id\n  }\n  linkedExpression {\n    id\n  }\n}\n\nmutation CreateRelationMetric($relation: ID!, $metric: ID!, $value: Metric!, $timepoint: DateTime) {\n  createRelationMetric(\n    input: {relation: $relation, metric: $metric, value: $value, timepoint: $timepoint}\n  ) {\n    ...EntityRelation\n  }\n}"


class CreateEntityMutation(BaseModel):
    create_entity: Entity = Field(alias="createEntity")

    class Arguments(BaseModel):
        kind: ID
        group: Optional[ID] = Field(default=None)
        name: Optional[str] = Field(default=None)
        parent: Optional[ID] = Field(default=None)
        instance_kind: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n  }\n}\n\nmutation CreateEntity($kind: ID!, $group: ID, $name: String, $parent: ID, $instance_kind: String) {\n  createEntity(\n    input: {group: $group, kind: $kind, name: $name, parent: $parent, instanceKind: $instance_kind}\n  ) {\n    ...Entity\n  }\n}"


class CreateMeasurementMutation(BaseModel):
    create_measurement: Entity = Field(alias="createMeasurement")

    class Arguments(BaseModel):
        structure: str
        graph: ID

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n  }\n}\n\nmutation CreateMeasurement($structure: StructureString!, $graph: ID!) {\n  createMeasurement(input: {structure: $structure, graph: $graph}) {\n    ...Entity\n  }\n}"


class CreateOntologyMutation(BaseModel):
    create_ontology: Ontology = Field(alias="createOntology")

    class Arguments(BaseModel):
        name: str
        purl: Optional[str] = Field(default=None)
        description: Optional[str] = Field(default=None)

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n}\n\nmutation CreateOntology($name: String!, $purl: String, $description: String) {\n  createOntology(input: {name: $name, purl: $purl, description: $description}) {\n    ...Ontology\n  }\n}"


class GetLinkedExpressionQuery(BaseModel):
    linked_expression: LinkedExpression = Field(alias="linkedExpression")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment LinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n    }\n  }\n}\n\nquery GetLinkedExpression($id: ID!) {\n  linkedExpression(id: $id) {\n    ...LinkedExpression\n  }\n}"


class SearchLinkedExpressionsQueryOptions(LinkedExpressionTrait, BaseModel):
    typename: Optional[Literal["LinkedExpression"]] = Field(
        alias="__typename", default="LinkedExpression", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchLinkedExpressionsQuery(BaseModel):
    options: Tuple[SearchLinkedExpressionsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchLinkedExpressions($search: String, $values: [ID!]) {\n  options: linkedExpressions(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n  }\n}"


class ListLinkedExpressionsQuery(BaseModel):
    linked_expressions: Tuple[ListLinkedExpression, ...] = Field(
        alias="linkedExpressions"
    )

    class Arguments(BaseModel):
        filters: Optional[LinkedExpressionFilter] = Field(default=None)
        pagination: Optional[OffsetPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment ListLinkedExpression on LinkedExpression {\n  id\n  graph {\n    id\n  }\n  kind\n  expression {\n    id\n    label\n    ontology {\n      id\n      name\n    }\n  }\n}\n\nquery ListLinkedExpressions($filters: LinkedExpressionFilter, $pagination: OffsetPaginationInput) {\n  linkedExpressions(filters: $filters, pagination: $pagination) {\n    ...ListLinkedExpression\n  }\n}"


class GetGraphQuery(BaseModel):
    graph: Graph

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Graph on Graph {\n  id\n  name\n}\n\nquery GetGraph($id: ID!) {\n  graph(id: $id) {\n    ...Graph\n  }\n}"


class SearchGraphsQueryOptions(GraphTrait, BaseModel):
    typename: Optional[Literal["Graph"]] = Field(
        alias="__typename", default="Graph", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchGraphsQuery(BaseModel):
    options: Tuple[SearchGraphsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchGraphs($search: String, $values: [ID!]) {\n  options: graphs(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class GetProtocolStepQuery(BaseModel):
    protocol_step: ProtocolStep = Field(alias="protocolStep")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment ProtocolStep on ProtocolStep {\n  id\n  template {\n    id\n    name\n  }\n  reagentMappings {\n    reagent {\n      id\n    }\n  }\n  forReagent {\n    id\n  }\n}\n\nquery GetProtocolStep($id: ID!) {\n  protocolStep(id: $id) {\n    ...ProtocolStep\n  }\n}"


class SearchProtocolStepsQueryOptions(BaseModel):
    typename: Optional[Literal["ProtocolStep"]] = Field(
        alias="__typename", default="ProtocolStep", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchProtocolStepsQuery(BaseModel):
    options: Tuple[SearchProtocolStepsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchProtocolSteps($search: String, $values: [ID!]) {\n  options: protocolSteps(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


class GetEntityRelationQuery(BaseModel):
    entity_relation: EntityRelation = Field(alias="entityRelation")

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment EntityRelation on EntityRelation {\n  id\n  left {\n    id\n  }\n  right {\n    id\n  }\n  linkedExpression {\n    id\n  }\n}\n\nquery GetEntityRelation($id: ID!) {\n  entityRelation(id: $id) {\n    ...EntityRelation\n  }\n}"


class SearchEntityRelationsQueryOptions(EntityRelationTrait, BaseModel):
    typename: Optional[Literal["EntityRelation"]] = Field(
        alias="__typename", default="EntityRelation", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntityRelationsQuery(BaseModel):
    options: Tuple[SearchEntityRelationsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntityRelations($search: String, $values: [ID!]) {\n  options: entityRelations(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n  }\n}"


class GetReagentQuery(BaseModel):
    reagent: Reagent

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Reagent on Reagent {\n  id\n  expression {\n    id\n  }\n  lotId\n}\n\nquery GetReagent($id: ID!) {\n  reagent(id: $id) {\n    ...Reagent\n  }\n}"


class SearchReagentsQueryOptions(BaseModel):
    typename: Optional[Literal["Reagent"]] = Field(
        alias="__typename", default="Reagent", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchReagentsQuery(BaseModel):
    options: Tuple[SearchReagentsQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchReagents($search: String, $values: [ID!]) {\n  options: reagents(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n  }\n}"


class GetEntityQuery(BaseModel):
    entity: Entity

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n  }\n}\n\nquery GetEntity($id: ID!) {\n  entity(id: $id) {\n    ...Entity\n  }\n}"


class SearchEntitiesQueryOptions(EntityTrait, BaseModel):
    typename: Optional[Literal["Entity"]] = Field(
        alias="__typename", default="Entity", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchEntitiesQuery(BaseModel):
    options: Tuple[SearchEntitiesQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchEntities($search: String, $values: [ID!]) {\n  options: entities(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: label\n  }\n}"


class EntitiesQuery(BaseModel):
    entities: Tuple[Entity, ...]

    class Arguments(BaseModel):
        filters: Optional[EntityFilter] = Field(default=None)
        pagination: Optional[GraphPaginationInput] = Field(default=None)

    class Meta:
        document = "fragment Entity on Entity {\n  id\n  label\n  linkedExpression {\n    id\n    label\n  }\n}\n\nquery Entities($filters: EntityFilter, $pagination: GraphPaginationInput) {\n  entities(filters: $filters, pagination: $pagination) {\n    ...Entity\n  }\n}"


class GetOntologyQuery(BaseModel):
    ontology: Ontology

    class Arguments(BaseModel):
        id: ID

    class Meta:
        document = "fragment Ontology on Ontology {\n  id\n  name\n}\n\nquery GetOntology($id: ID!) {\n  ontology(id: $id) {\n    ...Ontology\n  }\n}"


class SearchOntologiesQueryOptions(OntologyTrait, BaseModel):
    typename: Optional[Literal["Ontology"]] = Field(
        alias="__typename", default="Ontology", exclude=True
    )
    value: ID
    label: str
    model_config = ConfigDict(frozen=True)


class SearchOntologiesQuery(BaseModel):
    options: Tuple[SearchOntologiesQueryOptions, ...]

    class Arguments(BaseModel):
        search: Optional[str] = Field(default=None)
        values: Optional[List[ID]] = Field(default=None)

    class Meta:
        document = "query SearchOntologies($search: String, $values: [ID!]) {\n  options: ontologies(\n    filters: {search: $search, ids: $values}\n    pagination: {limit: 10}\n  ) {\n    value: id\n    label: name\n  }\n}"


async def alink_expression(
    expression: ID, graph: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """LinkExpression



    Arguments:
        expression (ID): expression
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return (
        await aexecute(
            LinkExpressionMutation,
            {"expression": expression, "graph": graph},
            rath=rath,
        )
    ).link_expression


def link_expression(
    expression: ID, graph: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """LinkExpression



    Arguments:
        expression (ID): expression
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return execute(
        LinkExpressionMutation, {"expression": expression, "graph": graph}, rath=rath
    ).link_expression


async def acreate_graph(name: str, rath: Optional[KraphRath] = None) -> Graph:
    """CreateGraph



    Arguments:
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (await aexecute(CreateGraphMutation, {"name": name}, rath=rath)).create_graph


def create_graph(name: str, rath: Optional[KraphRath] = None) -> Graph:
    """CreateGraph



    Arguments:
        name (str): name
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(CreateGraphMutation, {"name": name}, rath=rath).create_graph


async def acreate_protocol_step(
    input: ProtocolStepInput, rath: Optional[KraphRath] = None
) -> ProtocolStep:
    """CreateProtocolStep



    Arguments:
        input (ProtocolStepInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (
        await aexecute(CreateProtocolStepMutation, {"input": input}, rath=rath)
    ).create_protocol_step


def create_protocol_step(
    input: ProtocolStepInput, rath: Optional[KraphRath] = None
) -> ProtocolStep:
    """CreateProtocolStep



    Arguments:
        input (ProtocolStepInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(
        CreateProtocolStepMutation, {"input": input}, rath=rath
    ).create_protocol_step


async def acreate_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[List[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression



    Arguments:
        label (str): label
        kind (ExpressionKind): kind
        ontology (Optional[ID], optional): ontology.
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        color (Optional[List[int]], optional): color.
        metric_kind (Optional[MetricDataType], optional): metricKind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Expression"""
    return (
        await aexecute(
            CreateExpressionMutation,
            {
                "label": label,
                "ontology": ontology,
                "purl": purl,
                "description": description,
                "color": color,
                "metricKind": metric_kind,
                "kind": kind,
            },
            rath=rath,
        )
    ).create_expression


def create_expression(
    label: str,
    kind: ExpressionKind,
    ontology: Optional[ID] = None,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    color: Optional[List[int]] = None,
    metric_kind: Optional[MetricDataType] = None,
    rath: Optional[KraphRath] = None,
) -> Expression:
    """CreateExpression



    Arguments:
        label (str): label
        kind (ExpressionKind): kind
        ontology (Optional[ID], optional): ontology.
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        color (Optional[List[int]], optional): color.
        metric_kind (Optional[MetricDataType], optional): metricKind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Expression"""
    return execute(
        CreateExpressionMutation,
        {
            "label": label,
            "ontology": ontology,
            "purl": purl,
            "description": description,
            "color": color,
            "metricKind": metric_kind,
            "kind": kind,
        },
        rath=rath,
    ).create_expression


async def acreate_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation



    Arguments:
        left (ID): left
        right (ID): right
        kind (ID): kind
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(
            CreateEntityRelationMutation,
            {"left": left, "right": right, "kind": kind},
            rath=rath,
        )
    ).create_entity_relation


def create_entity_relation(
    left: ID, right: ID, kind: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateEntityRelation



    Arguments:
        left (ID): left
        right (ID): right
        kind (ID): kind
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateEntityRelationMutation,
        {"left": left, "right": right, "kind": kind},
        rath=rath,
    ).create_entity_relation


async def acreate_roi_entity_relation(
    input: StructureRelationInput, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation



    Arguments:
        input (StructureRelationInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(CreateRoiEntityRelationMutation, {"input": input}, rath=rath)
    ).create_structure_relation


def create_roi_entity_relation(
    input: StructureRelationInput, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """CreateRoiEntityRelation



    Arguments:
        input (StructureRelationInput): input
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateRoiEntityRelationMutation, {"input": input}, rath=rath
    ).create_structure_relation


async def acreate_reagent(
    expression: ID, lot_id: str, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent



    Arguments:
        expression (ID): expression
        lot_id (str): lotId
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (
        await aexecute(
            CreateReagentMutation,
            {"expression": expression, "lotId": lot_id},
            rath=rath,
        )
    ).create_reagent


def create_reagent(
    expression: ID, lot_id: str, rath: Optional[KraphRath] = None
) -> Reagent:
    """CreateReagent



    Arguments:
        expression (ID): expression
        lot_id (str): lotId
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(
        CreateReagentMutation, {"expression": expression, "lotId": lot_id}, rath=rath
    ).create_reagent


async def acreate_entity_metric(
    entity: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric



    Arguments:
        entity (ID): entity
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateEntityMetricMutation,
            {
                "entity": entity,
                "metric": metric,
                "value": value,
                "timepoint": timepoint,
            },
            rath=rath,
        )
    ).create_entity_metric


def create_entity_metric(
    entity: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntityMetric



    Arguments:
        entity (ID): entity
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateEntityMetricMutation,
        {"entity": entity, "metric": metric, "value": value, "timepoint": timepoint},
        rath=rath,
    ).create_entity_metric


async def acreate_relation_metric(
    relation: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric



    Arguments:
        relation (ID): relation
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(
            CreateRelationMetricMutation,
            {
                "relation": relation,
                "metric": metric,
                "value": value,
                "timepoint": timepoint,
            },
            rath=rath,
        )
    ).create_relation_metric


def create_relation_metric(
    relation: ID,
    metric: ID,
    value: Any,
    timepoint: Optional[datetime] = None,
    rath: Optional[KraphRath] = None,
) -> EntityRelation:
    """CreateRelationMetric



    Arguments:
        relation (ID): relation
        metric (ID): metric
        value (Any): value
        timepoint (Optional[datetime], optional): timepoint.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(
        CreateRelationMetricMutation,
        {
            "relation": relation,
            "metric": metric,
            "value": value,
            "timepoint": timepoint,
        },
        rath=rath,
    ).create_relation_metric


async def acreate_entity(
    kind: ID,
    group: Optional[ID] = None,
    name: Optional[str] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity



    Arguments:
        kind (ID): kind
        group (Optional[ID], optional): group.
        name (Optional[str], optional): name.
        parent (Optional[ID], optional): parent.
        instance_kind (Optional[str], optional): instance_kind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateEntityMutation,
            {
                "kind": kind,
                "group": group,
                "name": name,
                "parent": parent,
                "instance_kind": instance_kind,
            },
            rath=rath,
        )
    ).create_entity


def create_entity(
    kind: ID,
    group: Optional[ID] = None,
    name: Optional[str] = None,
    parent: Optional[ID] = None,
    instance_kind: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Entity:
    """CreateEntity



    Arguments:
        kind (ID): kind
        group (Optional[ID], optional): group.
        name (Optional[str], optional): name.
        parent (Optional[ID], optional): parent.
        instance_kind (Optional[str], optional): instance_kind.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateEntityMutation,
        {
            "kind": kind,
            "group": group,
            "name": name,
            "parent": parent,
            "instance_kind": instance_kind,
        },
        rath=rath,
    ).create_entity


async def acreate_measurement(
    structure: str, graph: ID, rath: Optional[KraphRath] = None
) -> Entity:
    """CreateMeasurement



    Arguments:
        structure (str): structure
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (
        await aexecute(
            CreateMeasurementMutation,
            {"structure": structure, "graph": graph},
            rath=rath,
        )
    ).create_measurement


def create_measurement(
    structure: str, graph: ID, rath: Optional[KraphRath] = None
) -> Entity:
    """CreateMeasurement



    Arguments:
        structure (str): structure
        graph (ID): graph
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(
        CreateMeasurementMutation, {"structure": structure, "graph": graph}, rath=rath
    ).create_measurement


async def acreate_ontology(
    name: str,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology



    Arguments:
        name (str): name
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (
        await aexecute(
            CreateOntologyMutation,
            {"name": name, "purl": purl, "description": description},
            rath=rath,
        )
    ).create_ontology


def create_ontology(
    name: str,
    purl: Optional[str] = None,
    description: Optional[str] = None,
    rath: Optional[KraphRath] = None,
) -> Ontology:
    """CreateOntology



    Arguments:
        name (str): name
        purl (Optional[str], optional): purl.
        description (Optional[str], optional): description.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(
        CreateOntologyMutation,
        {"name": name, "purl": purl, "description": description},
        rath=rath,
    ).create_ontology


async def aget_linked_expression(
    id: ID, rath: Optional[KraphRath] = None
) -> LinkedExpression:
    """GetLinkedExpression



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return (
        await aexecute(GetLinkedExpressionQuery, {"id": id}, rath=rath)
    ).linked_expression


def get_linked_expression(id: ID, rath: Optional[KraphRath] = None) -> LinkedExpression:
    """GetLinkedExpression



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        LinkedExpression"""
    return execute(GetLinkedExpressionQuery, {"id": id}, rath=rath).linked_expression


async def asearch_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return (
        await aexecute(
            SearchLinkedExpressionsQuery,
            {"search": search, "values": values},
            rath=rath,
        )
    ).options


def search_linked_expressions(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchLinkedExpressionsQueryOptions]:
    """SearchLinkedExpressions



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchLinkedExpressionsQueryLinkedexpressions]"""
    return execute(
        SearchLinkedExpressionsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def alist_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions



    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): filters.
        pagination (Optional[OffsetPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpression]"""
    return (
        await aexecute(
            ListLinkedExpressionsQuery,
            {"filters": filters, "pagination": pagination},
            rath=rath,
        )
    ).linked_expressions


def list_linked_expressions(
    filters: Optional[LinkedExpressionFilter] = None,
    pagination: Optional[OffsetPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[ListLinkedExpression]:
    """ListLinkedExpressions



    Arguments:
        filters (Optional[LinkedExpressionFilter], optional): filters.
        pagination (Optional[OffsetPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[ListLinkedExpression]"""
    return execute(
        ListLinkedExpressionsQuery,
        {"filters": filters, "pagination": pagination},
        rath=rath,
    ).linked_expressions


async def aget_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return (await aexecute(GetGraphQuery, {"id": id}, rath=rath)).graph


def get_graph(id: ID, rath: Optional[KraphRath] = None) -> Graph:
    """GetGraph



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Graph"""
    return execute(GetGraphQuery, {"id": id}, rath=rath).graph


async def asearch_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return (
        await aexecute(
            SearchGraphsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_graphs(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchGraphsQueryOptions]:
    """SearchGraphs



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchGraphsQueryGraphs]"""
    return execute(
        SearchGraphsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return (await aexecute(GetProtocolStepQuery, {"id": id}, rath=rath)).protocol_step


def get_protocol_step(id: ID, rath: Optional[KraphRath] = None) -> ProtocolStep:
    """GetProtocolStep



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        ProtocolStep"""
    return execute(GetProtocolStepQuery, {"id": id}, rath=rath).protocol_step


async def asearch_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return (
        await aexecute(
            SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_protocol_steps(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchProtocolStepsQueryOptions]:
    """SearchProtocolSteps



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchProtocolStepsQueryProtocolsteps]"""
    return execute(
        SearchProtocolStepsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity_relation(
    id: ID, rath: Optional[KraphRath] = None
) -> EntityRelation:
    """GetEntityRelation



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return (
        await aexecute(GetEntityRelationQuery, {"id": id}, rath=rath)
    ).entity_relation


def get_entity_relation(id: ID, rath: Optional[KraphRath] = None) -> EntityRelation:
    """GetEntityRelation



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        EntityRelation"""
    return execute(GetEntityRelationQuery, {"id": id}, rath=rath).entity_relation


async def asearch_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return (
        await aexecute(
            SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entity_relations(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntityRelationsQueryOptions]:
    """SearchEntityRelations



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntityRelationsQueryEntityrelations]"""
    return execute(
        SearchEntityRelationsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return (await aexecute(GetReagentQuery, {"id": id}, rath=rath)).reagent


def get_reagent(id: ID, rath: Optional[KraphRath] = None) -> Reagent:
    """GetReagent



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Reagent"""
    return execute(GetReagentQuery, {"id": id}, rath=rath).reagent


async def asearch_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return (
        await aexecute(
            SearchReagentsQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_reagents(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchReagentsQueryOptions]:
    """SearchReagents



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchReagentsQueryReagents]"""
    return execute(
        SearchReagentsQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aget_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return (await aexecute(GetEntityQuery, {"id": id}, rath=rath)).entity


def get_entity(id: ID, rath: Optional[KraphRath] = None) -> Entity:
    """GetEntity



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Entity"""
    return execute(GetEntityQuery, {"id": id}, rath=rath).entity


async def asearch_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return (
        await aexecute(
            SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_entities(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchEntitiesQueryOptions]:
    """SearchEntities



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchEntitiesQueryEntities]"""
    return execute(
        SearchEntitiesQuery, {"search": search, "values": values}, rath=rath
    ).options


async def aentities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities



    Arguments:
        filters (Optional[EntityFilter], optional): filters.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[Entity]"""
    return (
        await aexecute(
            EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
        )
    ).entities


def entities(
    filters: Optional[EntityFilter] = None,
    pagination: Optional[GraphPaginationInput] = None,
    rath: Optional[KraphRath] = None,
) -> List[Entity]:
    """Entities



    Arguments:
        filters (Optional[EntityFilter], optional): filters.
        pagination (Optional[GraphPaginationInput], optional): pagination.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[Entity]"""
    return execute(
        EntitiesQuery, {"filters": filters, "pagination": pagination}, rath=rath
    ).entities


async def aget_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return (await aexecute(GetOntologyQuery, {"id": id}, rath=rath)).ontology


def get_ontology(id: ID, rath: Optional[KraphRath] = None) -> Ontology:
    """GetOntology



    Arguments:
        id (ID): id
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        Ontology"""
    return execute(GetOntologyQuery, {"id": id}, rath=rath).ontology


async def asearch_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return (
        await aexecute(
            SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
        )
    ).options


def search_ontologies(
    search: Optional[str] = None,
    values: Optional[List[ID]] = None,
    rath: Optional[KraphRath] = None,
) -> List[SearchOntologiesQueryOptions]:
    """SearchOntologies



    Arguments:
        search (Optional[str], optional): search.
        values (Optional[List[ID]], optional): values.
        rath (kraph.rath.KraphRath, optional): The mikro rath client

    Returns:
        List[SearchOntologiesQueryOntologies]"""
    return execute(
        SearchOntologiesQuery, {"search": search, "values": values}, rath=rath
    ).options


LinkedExpressionFilter.model_rebuild()
ProtocolStepInput.model_rebuild()
StructureRelationInput.model_rebuild()
