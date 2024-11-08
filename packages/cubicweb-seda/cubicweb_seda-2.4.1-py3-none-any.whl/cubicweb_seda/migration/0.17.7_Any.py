sync_schema_props_perms("AuthorityRecord")

add_relation_type("wrap_dataobjects")

# XXX restore relations to [Binary|Physical]DataObjects

for group in rql("Any X WHERE X is SEDADataObjectGroup").entities():
    archive = group.seda_data_object_group
    if len(archive) != 1:
        continue
    archive = archive[0]
    if archive.cw_etype == "SEDAArchiveTransfer":
        archive.cw_set(
            reverse_seda_binary_data_object=group.reverse_seda_binary_data_object,
            reverse_seda_physical_data_object=group.reverse_seda_physical_data_object,
        )
        group.cw_delete()
        cnx.commit()


print(
    f"found {rql('Any COUNT(X) WHERE X is SEDADataObjectGroup')[0][0]} SEDADataObjectGroup(s) left"
)
