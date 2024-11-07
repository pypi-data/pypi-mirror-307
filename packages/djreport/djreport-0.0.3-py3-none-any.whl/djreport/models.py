# dj
from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.utils.module_loading import import_string

# internal
from .mixins import ReportDataSourceMixin


class DataSource(models.Model):
    """Data Source"""

    name = models.CharField(max_length=150, unique=True)
    dotted_path = models.CharField(
        max_length=255, help_text="E.g. apps.accounting.models.Invoice"
    )

    class Meta:
        abstract = "djreport" not in settings.INSTALLED_APPS

    @cached_property
    def instance(self) -> ReportDataSourceMixin:
        # get data source class from given dotted path
        data_source_class = import_string(self.dotted_path)
        # initialize and return class
        return data_source_class()

    def get_data(self, **kwargs) -> dict:
        return self.instance.get_data(**kwargs)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"DataSource(id={self.id}, name={self.name})"


class Report(models.Model):
    """Report"""

    active = models.BooleanField(default=True)
    name = models.CharField(max_length=150, unique=True)
    file = models.FileField(upload_to="reports/")
    data_source = models.ForeignKey(
        "DataSource", related_name="reports", on_delete=models.CASCADE
    )

    class Meta:
        abstract = "djreport" not in settings.INSTALLED_APPS

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Report(id={self.id}, name={self.name})"
