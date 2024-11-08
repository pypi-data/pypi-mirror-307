from cubicweb_seda import iter_all_rdefs

for rdef, role in iter_all_rdefs(schema, "SEDAArchiveTransfer"):
    if role == "subject":
        target_etype = rdef.subject
    else:
        target_etype = rdef.object
    if target_etype == "SEDAArchiveUnit":
        sync_schema_props_perms((rdef.subject, rdef.rtype, rdef.object))

sync_schema_props_perms("clone_of")

add_relation_type("code_keyword_type")

scheme = cnx.find("ConceptScheme", title="SEDA 2 : Types de mot-clé").one()
with cnx.deny_all_hooks_but():
    scheme.cw_set(title="SEDA : Types de mot-clé")
    cnx.commit()
    cnx.execute(
        'SET L language_code "seda" WHERE L label_of C, C in_scheme CS, CS eid %(cs)s',
        {"cs": scheme.eid},
    )
    cnx.commit()

for concept in scheme.reverse_in_scheme:
    label = {
        "corpname": "Collectivité",
        "famname": "Nom de famille",
        "geogname": "Nom géographique",
        "name": "Nom",
        "occupation": "Fonction",
        "persname": "Nom de personne",
        "subject": "Mot-matière",
        "genreform": "Typologie documentaire",
        "function": "Activité",
    }[concept.label("seda")]
    cnx.create_entity(
        "Label", label_of=concept, label=label, kind="preferred", language_code="fr"
    )

cnx.commit()
