# migration script from seda 2.1 to seda 2.2

import logging

logger = logging.getLogger("seda.migration")
logger.setLevel(logging.INFO)

logger.info("\n\nUpdate schema for seda 2.2 \n\n")

logger.info("\n\nRename entities: \n")

RENAMED_ETYPES = (
    ("SEDAAgentAbstract", "SEDAAgent"),
    ("SEDAAltAgentAbstractCorpname", "SEDAAltAgentCorpname"),
    ("SEDASeqAltAgentAbstractCorpnameFirstName", "SEDASeqAltAgentCorpnameFirstName"),
)

for old_etype, new_etype in RENAMED_ETYPES:
    try:
        eschema = cnx.repo.schema.entity_schema_for(old_etype)  # noqa
    except KeyError:
        # check the new entity exists
        cnx.repo.schema.entity_schema_for(new_etype)  # noqa
        logger.warning(
            f"Entity '{old_etype}' doesn't exist and has been replaced by {new_etype}"
        )
        continue
    count = rql(f"Any COUNT(X) WHERE X is {old_etype}")[0][0]  # noqa
    if count > 0:
        logger.error(f"Found {count} {old_etype}")
        raise
    logger.info(f"Found {count} {old_etype}")
    drop_entity_type(old_etype)  # noqa
    add_entity_type(new_etype)  # noqa

cnx.commit()  # noqa

NEW_ETYPES = (
    "SEDAHoldRuleCodeListVersion",
    "SEDADataObjectProfile",
    "SEDAHoldRule",
    "SEDASeqHoldRuleRule",
    "SEDAAltHoldRulePreventInheritance",
    "SEDAHoldEndDate",
    "SEDAHoldOwner",
    "SEDAHoldReassessingDate",
    "SEDAHoldReason",
    "SEDAPreventRearrangement",
    "SEDADateLitteral",
    "SEDAOriginatingSystemIdReplyTo",
    "SEDATextContent",
    "SEDALinkingAgentIdentifier",
    "SEDALinkingAgentIdentifierType",
    "SEDALinkingAgentIdentifierValue",
    "SEDALinkingAgentRole",
)

logger.info("\n\nAdd new entities: \n")

for new_etype in NEW_ETYPES:
    add_entity_type(new_etype)  # noqa
    logger.info(f"Add new entity type '{new_etype}'")

cnx.commit()  # noqa

# new attributes

NEW_ATTRIBUTES = (
    ("SEDADataObjectSystemId", "data_object_system_id"),
    ("SEDADataObjectGroupSystemId", "data_object_group_system_id"),
    ("SEDAClassificationAudience", "classification_audience"),
    ("SEDAEventTypeCode", "event_type_code"),
    ("SEDAOutcome", "outcome"),
    ("SEDAOutcomeDetail", "outcome_detail"),
    ("SEDAOutcomeDetailMessage", "outcome_detail_message"),
    ("SEDAEventDetailData", "event_detail_data"),
    ("SEDAIdentifier", "identifier"),
    ("SEDAGender", "gender"),
    ("SEDANationality", "nationality"),
    ("SEDAExternalReference", "external_reference"),
)

logger.info("\n\nAdd new attributes: \n")

for etype, attr in NEW_ATTRIBUTES:
    logger.info(f"Add new attribute '{attr}' for entity type '{etype}'")
    add_attribute(etype, attr)  # noqa

cnx.commit()  # noqa

# remove birth and death dates
drop_attribute("SEDABirthDate", "birth_date")
drop_attribute("SEDADeathDate", "death_date")

sync_schema_props_perms("SEDABirthDate")
sync_schema_props_perms("SEDADeathDate")
cnx.commit()


logger.info("\n\nCheck schema for seda 2.2 \n\n")

# check new subject relations have been added
CHECK_NEW_SUBJECT_RELATIONS = (
    (
        "seda_hold_rule_code_list_version_from",
        "SEDAHoldRuleCodeListVersion",
        "archive_transfer_hold_rule_code_list_version_from",
    ),
    (
        "seda_hold_rule_code_list_version_to",
        "SEDAHoldRuleCodeListVersion",
        "hold_rule_code_list_version_hold_rule_code_list_version_to",
    ),
    (
        "seda_data_object_profile",
        "SEDADataObjectProfile",
        "binary_data_object_data_object_profile",
    ),
    (
        "seda_hold_rule",
        "SEDAHoldRule",
        "archive_transfer_hold_rule",
    ),
    (
        "seda_seq_hold_rule_rule",
        "SEDAHoldRule",
        "hold_rule_seq_hold_rule_rule",
    ),
    (
        "seda_alt_hold_rule_prevent_inheritance",
        "SEDAHoldRule",
        "hold_rule_alt_hold_rule_prevent_inheritance",
    ),
    (
        "seda_linking_agent_identifier",
        "SEDALinkingAgentIdentifier",
        "event_linking_agent_identifier",
    ),
    (
        "seda_hold_rule",
        "SEDAHoldRule",
        "seq_alt_archive_unit_archive_unit_ref_id_management_hold_rule",
    ),
    (
        "seda_date_litteral",
        "SEDADateLitteral",
        "seq_alt_archive_unit_archive_unit_ref_id_management_date_litteral",
    ),
    (
        "seda_originating_system_id_reply_to",
        "SEDAOriginatingSystemIdReplyTo",
        "seq_alt_archive_unit_archive_unit_ref_id_management_originating_system_id_reply_to",
    ),
    (
        "seda_text_content",
        "SEDATextContent",
        "seq_alt_archive_unit_archive_unit_ref_id_management_text_content",
    ),
    (
        "seda_rule",
        "SEDASeqHoldRuleRule",
        "seq_hold_rule_rule_rule",
    ),
    (
        "seda_hold_end_date",
        "SEDAHoldEndDate",
        "seq_hold_rule_rule_hold_end_date",
    ),
    (
        "seda_hold_owner",
        "SEDAHoldOwner",
        "seq_hold_rule_rule_hold_owner",
    ),
    (
        "seda_hold_reassessing_date",
        "SEDAHoldReassessingDate",
        "seq_hold_rule_rule_hold_reassessing_date",
    ),
    (
        "seda_hold_reason",
        "SEDAHoldReason",
        "seq_hold_rule_rule_hold_reason",
    ),
    (
        "seda_prevent_rearrangement",
        "SEDAPreventRearrangement",
        "seq_hold_rule_rule_prevent_rearrangement",
    ),
    (
        "seda_linking_agent_identifier_type",
        "SEDALinkingAgentIdentifierType",
        "linking_agent_identifier_linking_agent_identifier_type",
    ),
    (
        "seda_linking_agent_identifier_value",
        "SEDALinkingAgentIdentifierValue",
        "linking_agent_identifier_linking_agent_identifier_value",
    ),
    (
        "seda_linking_agent_role",
        "SEDALinkingAgentRole",
        "linking_agent_identifier_linking_agent_role",
    ),
    (
        "seda_outcome_detail",  # old relation, still exists
        "SEDAOutcomeDetail",
        "event_outcome_detail",
    ),
    (
        "seda_agent",
        "SEDAAgent",
        "seq_alt_archive_unit_archive_unit_ref_id_management_agent",
    ),
)

for relname, obj, cw_relname in CHECK_NEW_SUBJECT_RELATIONS:
    eschema = cnx.repo.schema.entity_schema_for(obj)  # noqa
    try:
        eschema.relation_definition(relname)
        logger.info(f"Relation '{relname}' for '{obj}' exists")
    except KeyError:
        logger.error(f"Relation '{relname}' for '{obj} doesn't exist")


# check new object relations have been added
CHECK_NEW_OBJECT_RELATIONS = (
    (
        "seda_start_date",
        (
            "SEDASeqAltArchiveUnitArchiveUnitRefIdManagement",
            "SEDASeqAccessRuleRule",
            "SEDASeqAppraisalRuleRule",
            "SEDASeqClassificationRuleRule",
            "SEDASeqDisseminationRuleRule",
            "SEDASeqHoldRuleRule",
            "SEDASeqReuseRuleRule",
            "SEDASeqStorageRuleRule",
        ),
        "seq_storage_rule_rule_start_date",
    ),
    (
        "seda_prevent_inheritance",
        (
            "SEDAAltAccessRulePreventInheritance",
            "SEDAAltAppraisalRulePreventInheritance",
            "SEDAAltClassificationRulePreventInheritance",
            "SEDAAltDisseminationRulePreventInheritance",
            "SEDAAltHoldRulePreventInheritance",
            "SEDAAltReuseRulePreventInheritance",
            "SEDAAltStorageRulePreventInheritance",
        ),
        "alt_storage_rule_prevent_inheritance_prevent_inheritance",
    ),
    (
        "seda_ref_non_rule_id_from",
        (
            "SEDAAltAccessRulePreventInheritance",
            "SEDAAltAppraisalRulePreventInheritance",
            "SEDAAltClassificationRulePreventInheritance",
            "SEDAAltDisseminationRulePreventInheritance",
            "SEDAAltHoldRulePreventInheritance",
            "SEDAAltReuseRulePreventInheritance",
            "SEDAAltStorageRulePreventInheritance",
        ),
        "alt_storage_rule_prevent_inheritance_ref_non_rule_id_from",
    ),
    (
        "seda_external_reference",
        (
            "SEDAAltIsPartOfArchiveUnitRefId",
            "SEDAAltIsVersionOfArchiveUnitRefId",
            "SEDAAltReferencesArchiveUnitRefId",
            "SEDAAltReplacesArchiveUnitRefId",
            "SEDAAltRequiresArchiveUnitRefId",
        ),
        "alt_is_version_of_archive_unit_ref_id_external_reference",
    ),
    (
        "seda_function",
        ("SEDAAgent",),
        "agent_function",
    ),
    (
        "seda_activity",
        ("SEDAAgent",),
        "agent_activity",
    ),
    (
        "seda_position",
        ("SEDAAgent",),
        "agent_position",
    ),
    (
        "seda_role",
        ("SEDAAgent",),
        "agent_role",
    ),
    (
        "seda_mandate",
        ("SEDAAgent",),
        "agent_mandate",
    ),
    (
        "seda_corpname",
        (
            "SEDAAltAgentCorpname",
            "SEDAAltSenderCorpname",
            "SEDAAltTransmitterCorpname",
        ),
        "alt_agent_corpname_corpname",
    ),
    (
        "seda_gender",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_gender",
    ),
    (
        "seda_nationality",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_nationality",
    ),
    (
        "seda_identifier",
        ("SEDAAgent", "SEDASender", "SEDATransmitter"),
        "agent_identifier",
    ),
    (
        "seda_first_name",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_first_name",
    ),
    (
        "seda_full_name",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_full_name",
    ),
    (
        "seda_given_name",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_given_name",
    ),
    (
        "seda_birth_name",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_birth_name",
    ),
    (
        "seda_birth_date",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_birth_date",
    ),
    (
        "seda_birth_place",
        ("SEDASeqAltAgentCorpnameFirstName",),
        "seq_alt_agent_corpname_first_name_birth_place",
    ),
    (
        "seda_death_date",
        (
            "SEDASeqAltAgentCorpnameFirstName",
            "SEDASeqAltSenderCorpnameFirstName",
            "SEDASeqAltTransmitterCorpnameFirstName",
        ),
        "seq_alt_agent_corpname_first_name_death_date",
    ),
    (
        "seda_death_place",
        ("SEDASeqAltAgentCorpnameFirstName",),
        "seq_alt_agent_corpname_first_name_death_place",
    ),
    (
        "seda_alt_agent_corpname",
        ("SEDAAltAgentCorpname",),
        "agent_alt_agent_corpname",
    ),
    (
        "seda_seq_alt_agent_corpname_first_name",
        ("SEDASeqAltAgentCorpnameFirstName",),
        "alt_agent_corpname_seq_alt_agent_corpname_first_name",
    ),
)

for relname, objects, cw_relname in CHECK_NEW_OBJECT_RELATIONS:
    for obj in objects:
        eschema = cnx.repo.schema.entity_schema_for(obj)  # noqa
        try:
            eschema.relation_definition(relname, role="object")
            logger.info(f"Relation '{relname}' for '{obj}' exists")
        except KeyError:
            logger.error(f"ERROR, Relation '{relname}' for '{obj} doesn't exist")


# check new attributes have been added
for etype, attr in NEW_ATTRIBUTES:
    eschema = cnx.repo.schema.entity_schema_for(etype)  # noqa
    try:
        eschema.relation_definition(attr)
        logger.info("Attribute '%s' for '%s' is known" % (attr, etype))
    except KeyError:
        logger.error("ERROR, Attribute '%s' for '%s' doesn't exist" % (attr, etype))

CHECK_REMOVED_ATTRIBUTES = (
    ("SEDABirthDate", "birth_date"),
    ("SEDADeathDate", "death_date"),
)

for etype, attr in CHECK_REMOVED_ATTRIBUTES:
    eschema = cnx.repo.schema.entity_schema_for(etype)  # noqa
    try:
        eschema.relation_definition(attr)
        logger.error("ERROR, Attribute '%s' for '%s' is still known" % (attr, etype))
    except KeyError:
        logger.info("Attribute '%s' for '%s' doesn't exist" % (attr, etype))


# check add agent_abstract related relations have been removed
for rtype in (
    "seda_agent_abstract",
    "seda_alt_agent_abstract_corpname",
    "seda_seq_alt_agent_abstract_corpname_first_name",
):
    try:
        cnx.repo.schema.relation_schema_for(rtype)  # noqa
        logger.error("ERROR, Relation definition '%s' still exists" % rtype)
    except KeyError:
        logger.info("Relation definition '%s' doesn't exist" % rtype)

# relation en double (!!!)
# class event_linking_agent_identifier(RelationDefinition):

logger.info("\n\n Update compat_list for SEDA 2.1 : mark them SEDA 2.2 exportable \n")

SEDA22 = "SEDA 2.2"
COMPAT_SEP = ", "

for entity, compat in rql(
    "Any X, R WHERE X compat_list R"
).iter_rows_with_entities():  # noqa
    compats = compat.split(COMPAT_SEP)
    if "SEDA 2.1" in compats and not SEDA22 in compats:
        compats.append(SEDA22)
        entity.cw_set(compat_list=COMPAT_SEP.join(compats))

cnx.commit()  # noqa
