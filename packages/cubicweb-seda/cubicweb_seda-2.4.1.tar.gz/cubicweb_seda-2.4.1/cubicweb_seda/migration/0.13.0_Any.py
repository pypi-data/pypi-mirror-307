from cubicweb_seda.xsd2yams import MULTIPLE_CHILDREN

add_relation_type("ordering")

parent_rtypes = [rtype for _, rtype in MULTIPLE_CHILDREN]

for rtype in parent_rtypes:
    for (peid,) in rql(f"Any P GROUPBY P WHERE X {rtype} P HAVING COUNT(X) > 1"):
        for idx, child in enumerate(
            rql(f"Any X WHERE X {rtype} P, P eid %(p)s", {"p": peid}).entities()
        ):
            child.cw_set(ordering=idx + 1)
    commit(ask_confirm=False)

rql("SET X ordering 1 WHERE X ordering NULL")

commit(ask_confirm=False)
