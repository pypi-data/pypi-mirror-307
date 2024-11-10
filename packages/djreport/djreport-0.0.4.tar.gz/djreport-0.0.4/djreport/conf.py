# dj
from django.conf import settings
from django.utils.functional import cached_property

# internal
from . import consts


class DJReportConf(object):
    """DJReport Conf"""

    @staticmethod
    def _get_settings(key, default=None):
        return getattr(settings, key, default)

    @cached_property
    def output_format(self):
        return self._get_settings("DJREPORT_OUTPUT_FORMAT", consts.OUTPUT_FORMAT_PDF)

    @cached_property
    def report_render_template(self):
        return self._get_settings("DJREPORT_REPORT_RENDER_TEMPLATE", "report.html")

    @cached_property
    def stimulsoft_license(self):
        return self._get_settings("DJREPORT_STIMULSOFT_LICENSE")


djreport_conf = DJReportConf()
