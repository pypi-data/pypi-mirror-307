# standard
import json

# dj
from django.views import View
from django.shortcuts import render, get_object_or_404

# internal
from .models import Report
from .conf import djreport_conf
from .forms import RenderReportForm


class RenderReportView(View):
    """Render Report View"""

    output_format = djreport_conf.output_format
    template = djreport_conf.report_render_template
    queryset = Report.objects.select_related("data_source").filter(active=True)

    @property
    def query_params(self) -> dict:
        return self.request.GET.dict()

    @property
    def render_params(self) -> dict:
        f = RenderReportForm(data=self.query_params)
        f.is_valid()
        return f.cleaned_data

    def get_queryset(self):
        return self.queryset

    def get_report(self, report_pk) -> Report:
        queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=report_pk)

    def get_output_format(self) -> str:
        return self.render_params.get("output_format") or self.output_format

    def get_report_data(self, report) -> str:
        params = {"request": self.request}
        params.update(self.query_params)
        report_data = report.data_source.get_data(**params)
        return json.dumps(report_data)

    def get(self, request, report_pk):
        report = self.get_report(report_pk)
        report_data = self.get_report_data(report)
        output_format = self.get_output_format()
        context = {
            "report": report,
            "report_data": report_data,
            "output_format": output_format,
        }
        # check for license
        if djreport_conf.stimulsoft_license:
            context["license"] = djreport_conf.stimulsoft_license
        # render report
        return render(request, self.template, context)
