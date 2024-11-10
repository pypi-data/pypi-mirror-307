class Report {
  constructor(license, reportName, reportFile, reportData, outputFormat) {
    this.license = license;
    this.reportName = reportName;
    this.reportFile = reportFile;
    this.reportData = reportData;
    this.outputFormat = outputFormat;

    this._report = null;
  }

  get report() {
    if (!this._report) {
      // set license
      Stimulsoft.Base.StiLicense.Key = this.license;
      // initialize report
      this._report = new Stimulsoft.Report.StiReport();
      // add fonts
      var fontFileContent = Stimulsoft.System.IO.File.getFile("/static/fonts/B Nazanin.ttf", true);
      var resource = new Stimulsoft.Report.Dictionary.StiResource(
        "B-Nazanin",
        "B-Nazanin",
        false,
        Stimulsoft.Report.Dictionary.StiResourceType.FontTtf,
        fontFileContent
      );
      this._report.dictionary.resources.add(resource);
      // load report file
      this._report.loadFile(this.reportFile);
      this._report.reportAlias = this.reportName;
      // load and bind report data
      const dataSet = new Stimulsoft.System.Data.DataSet('data');
      dataSet.readJson(this.reportData);
      this._report.dictionary.databases.clear();
      this._report.regData('data', 'data', dataSet);
    }
    return this._report;
  }

  exportToPDF() {
    this.report.exportDocumentAsync(content => {
      Stimulsoft.System.StiObject.saveAs(
        content, `${this.report.reportAlias}.pdf`, 'application/pdf'
      );
    }, Stimulsoft.Report.StiExportFormat.Pdf);
  }

  exportToHTML() {
    this.report.exportDocumentAsync(content => {
      Stimulsoft.System.StiObject.saveAs(
        content, `${this.report.reportAlias}.html`, 'text/html;charset=utf-8'
      );
    }, Stimulsoft.Report.StiExportFormat.Html);
  }

  render() {
    this.report.renderAsync(() => {
      if (this.outputFormat === 'html') {
        this.exportToHTML();
      } else if (this.outputFormat === 'pdf') {
        this.exportToPDF();
      }
    })
  }
}