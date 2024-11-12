from typing import Dict, Any, List
import math
from .vars import current_ontology, current_graph


def create_linked_expression(expression, graph=None):
    from kraph.api.schema import link_expression

    if graph is None:
        graph = current_graph.get()

    assert graph is not None, "Graph must be set"

    return link_expression(expression=expression, graph=graph)


def v(name, description=None):
    from kraph.api.schema import create_expression, ExpressionKind

    exp = create_expression(
        label=name,
        ontology=current_ontology.get(),
        kind=ExpressionKind.ENTITY,
        description=description,
    )
    return create_linked_expression(exp)


def e(name, description=None):
    from kraph.api.schema import create_expression, ExpressionKind

    exp = create_expression(
        label=name,
        ontology=current_ontology.get(),
        kind=ExpressionKind.RELATION,
        description=description,
    )
    return create_linked_expression(exp)


def m(name, metric_kind, description=None):
    from kraph.api.schema import create_expression, ExpressionKind, MetricDataType

    exp = create_expression(
        label=name,
        ontology=current_ontology.get(),
        kind=ExpressionKind.METRIC,
        metric_kind=metric_kind,
        description=description,
    )
    return create_linked_expression(exp)


def rm(name, metric_kind, description=None):
    from kraph.api.schema import create_expression, ExpressionKind, MetricDataType

    exp = create_expression(
        label=name,
        ontology=current_ontology.get(),
        kind=ExpressionKind.RELATION_METRIC,
        metric_kind=metric_kind,
        description=description,
    )
    return create_linked_expression(exp)


