from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


class PDFExporter:
    def export(self, report_data: dict, output_path: str) -> str:
        doc      = SimpleDocTemplate(output_path, pagesize=A4,
                                     leftMargin=20*mm, rightMargin=20*mm,
                                     topMargin=20*mm, bottomMargin=20*mm)
        styles   = getSampleStyleSheet()
        elements = []

        meta    = report_data.get("meta", {})
        summary = report_data.get("summary", {})
        evidence = report_data.get("evidence", [])

        # Title
        title_style = ParagraphStyle("title", fontSize=20, fontName="Helvetica-Bold",
                                     textColor=colors.HexColor("#0f172a"), spaceAfter=4)
        elements.append(Paragraph("APIForge Test Report", title_style))

        sub_style = ParagraphStyle("sub", fontSize=10, textColor=colors.HexColor("#64748b"),
                                   spaceAfter=16)
        elements.append(Paragraph(
            f"{meta.get('api_title','')} v{meta.get('api_version','')} | {meta.get('generated_at','')}",
            sub_style
        ))
        elements.append(Spacer(1, 8))

        # Summary Cards
        pass_rate = summary.get('pass_rate', 0)
        rate_color = colors.HexColor("#22c55e") if pass_rate >= 80 else colors.HexColor("#ef4444")

        summary_data = [
            ["Total", "Passed", "Failed", "Pass Rate", "Avg Latency"],
            [
                str(summary.get("total", 0)),
                str(summary.get("passed", 0)),
                str(summary.get("failed", 0)),
                f"{pass_rate}%",
                f"{summary.get('avg_latency', 0)}ms"
            ]
        ]
        summary_table = Table(summary_data, colWidths=[35*mm]*5)
        summary_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR",    (0,0), (-1,0), colors.white),
            ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",     (0,0), (-1,-1), 10),
            ("ALIGN",        (0,0), (-1,-1), "CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1), [colors.HexColor("#f8fafc"), colors.white]),
            ("GRID",         (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING",   (0,0), (-1,-1), 8),
            ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 16))

        # Evidence Table
        header = ["ID", "Method", "URL", "Status", "Latency", "Result"]
        rows   = [header]
        for e in evidence:
            status = e["assertions"]["status"].upper()
            rows.append([
                e.get("id", ""),
                e["endpoint"]["method"],
                e["endpoint"]["url"][:45] + "..." if len(e["endpoint"]["url"]) > 45 else e["endpoint"]["url"],
                str(e["response"]["status_code"]),
                f"{e['response']['latency_ms']}ms",
                status
            ])

        col_widths = [15*mm, 18*mm, 65*mm, 18*mm, 20*mm, 22*mm]
        table      = Table(rows, colWidths=col_widths, repeatRows=1)

        row_styles = [
            ("BACKGROUND",    (0,0), (-1,0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
            ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
            ("FONTSIZE",      (0,0), (-1,-1), 8),
            ("ALIGN",         (0,0), (-1,-1), "CENTER"),
            ("GRID",          (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING",    (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ]

        for i, e in enumerate(evidence, start=1):
            bg = colors.HexColor("#f0fdf4") if e["assertions"]["status"] == "passed" else colors.HexColor("#fef2f2")
            row_styles.append(("BACKGROUND", (0,i), (-1,i), bg))

        table.setStyle(TableStyle(row_styles))
        elements.append(table)

        doc.build(elements)
        return output_path
