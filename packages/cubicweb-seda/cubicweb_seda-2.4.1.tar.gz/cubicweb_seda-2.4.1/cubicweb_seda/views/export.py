# copyright 2015-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-seda views related to XSD download"""

from logilab.common.registry import objectify_predicate

from cubicweb import _
from cubicweb.predicates import is_instance, one_line_rset
from cubicweb_web import httpcache, action
from cubicweb_web.view import EntityView
from cubicweb_web.views import idownloadable

DEFAULT_VERSION = "2.2"
SEDA2_VERSIONS = ("2.1", "2.2")


@objectify_predicate
def format_supported(cls, req, rset=None, entity=None, **kwargs):
    """Predicate matching cases where an expected format (specified as `version` form param or as a
    `seda_version` class attribute on the appobject) is supported by the context's transfer entity.
    """
    if entity is None:
        entity = rset.get_entity(0, 0)
    version = getattr(
        cls,
        "seda_version",
        kwargs.get("version", req.form.get("version", DEFAULT_VERSION)),
    )
    if version not in SEDA2_VERSIONS and not entity.simplified_profile:
        return 0
    return int(f"SEDA {version}" in entity.formats_compat)


class SEDADownloadAction(action.Action):
    __abstract__ = True
    __select__ = (
        action.Action.__select__
        & one_line_rset()
        & is_instance("SEDAArchiveTransfer")
        & format_supported()
    )
    category = "moreactions"

    # set those in concret classes
    __regid__ = title = seda_version = export_format = order = None

    def url(self):
        entity = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        return entity.absolute_url(
            vid="seda.export", version=self.seda_version, format=self.export_format
        )


class SEDA22DownloadRNGAction(SEDADownloadAction):
    title = _("SEDA 2.2 RNG export")
    order = 90
    seda_version = "2.2"
    export_format = "rng"
    __regid__ = f"seda.export.{seda_version}.{export_format}"


class SEDA20DownloadRNGAction(SEDADownloadAction):
    title = _("SEDA 2.1 RNG export")
    order = 100
    seda_version = "2.1"
    export_format = "rng"
    __regid__ = f"seda.export.{seda_version}.{export_format}"


class SEDA1DownloadRNGAction(SEDADownloadAction):
    title = _("SEDA 1.0 RNG export")
    order = 102
    seda_version = "1.0"
    export_format = "rng"
    __regid__ = f"seda.export.{seda_version}.{export_format}"


class SEDA02DownloadRNGAction(SEDADownloadAction):
    title = _("SEDA 0.2 RNG export")
    order = 104
    seda_version = "0.2"
    export_format = "rng"
    __regid__ = f"seda.export.{seda_version}.{export_format}"


class SEDA2DownloadHTMLAction(SEDADownloadAction):
    title = _("HTML documentation")
    order = 110
    seda_version = "2.2"
    export_format = "html"
    __regid__ = f"seda.export.{seda_version}.{export_format}"


class SEDAExportViewMixin:
    __regid__ = "seda.export"
    __select__ = one_line_rset() & is_instance("SEDAArchiveTransfer")


class SEDAExportView(SEDAExportViewMixin, idownloadable.DownloadView):
    """SEDA archive transfer export view, to download rng, html or xsd
    representation of a profile."""

    __select__ = SEDAExportViewMixin.__select__ & format_supported()

    http_cache_manager = httpcache.NoHTTPCacheManager

    @property
    def seda_adapter_id(self):
        return "SEDA-{}.{}".format(
            self.cw_extra_kwargs.get(
                "version", self._cw.form.get("version", DEFAULT_VERSION)
            ),
            self.cw_extra_kwargs.get(
                "format", self._cw.form.get("format", "rng")
            ).lower(),
        )

    def set_request_content_type(self):
        entity = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        adapter = entity.cw_adapt_to(self.seda_adapter_id)
        filename = "{}-{}.{}".format(
            entity.dc_title(),
            self._cw.form.get("version", DEFAULT_VERSION),
            self._cw.form.get("format", "rng").lower(),
        )
        self._cw.set_content_type(
            adapter.content_type,
            filename=filename,
            encoding=adapter.encoding,
            disposition="attachment",
        )

    def call(self, **kwargs):
        entity = self.cw_rset.get_entity(self.cw_row or 0, self.cw_col or 0)
        adapter = entity.cw_adapt_to(self.seda_adapter_id)
        self.w(adapter.dump())


class SEDANonSupportedExportView(SEDAExportViewMixin, EntityView):
    """SEDA archive transfer export view for cases where an unsupported export is specified."""

    __select__ = SEDAExportViewMixin.__select__ & ~format_supported()

    def entity_call(self, entity):
        self.w('<div class="page">')
        self.w('<p class="alert alert-danger">')
        version = self.cw_extra_kwargs.get(
            "version", self._cw.form.get("version", DEFAULT_VERSION)
        )
        self.w(
            self._cw._("Export to SEDA version {0} is not possible.").format(version)
        )
        self.w("</p>")
        self.w("<p>")
        self.w(self._cw._("Supported formats: {0}.").format(entity.compat_list))
        self.w("</p>")
        self.w("</div>")
