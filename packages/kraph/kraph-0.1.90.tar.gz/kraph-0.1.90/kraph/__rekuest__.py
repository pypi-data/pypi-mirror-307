def register_structures(structure_reg):
    from rekuest_next.structures.default import (
        get_default_structure_registry,
        PortScope,
        id_shrink,
    )
    from rekuest_next.widgets import SearchWidget

    from kraph.api.schema import (
        Entity,
        Reagent,
        EntityRelation,
        ProtocolStep,
        aget_entity,
        aget_reagent,
        aget_entity_relation,
        Graph,
        aget_graph,
        SearchGraphsQuery,
        aget_protocol_step,
        SearchEntitiesQuery,
        SearchReagentsQuery,
        SearchEntityRelationsQuery,
        SearchProtocolStepsQuery,
    )


    structure_reg.register_as_structure(
        Entity,
        identifier="@kraph/entity",
        aexpand=aget_entity,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntitiesQuery.Meta.document, ward="kraph"
        ),
    )
    structure_reg.register_as_structure(
        Graph,
        identifier="@kraph/graph",
        aexpand=aget_graph,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchGraphsQuery.Meta.document, ward="kraph"
        ),
    )
    structure_reg.register_as_structure(
        Reagent,
        identifier="@kraph/reagent",
        aexpand=aget_reagent,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchReagentsQuery.Meta.document, ward="kraph"
        ),
    )

    structure_reg.register_as_structure(
        EntityRelation,
        identifier="@kraph/entity_relation",
        aexpand=aget_entity_relation,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchEntityRelationsQuery.Meta.document, ward="kraph"
        ),
    )
    structure_reg.register_as_structure(
        ProtocolStep,
        identifier="@kraph/protocolstep",
        aexpand=aget_protocol_step,
        ashrink=id_shrink,
        scope=PortScope.GLOBAL,
        default_widget=SearchWidget(
            query=SearchProtocolStepsQuery.Meta.document, ward="kraph"
        ),
    )

