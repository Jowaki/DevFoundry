import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from typing import Dict
import io

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Preformatted
    from reportlab.lib import colors
except ImportError:
    raise ImportError("reportlab not installed. Run: pip install reportlab")

class PDFGenerator:
    """Generates comprehensive PDF reports for code generation."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHead',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
    
    def generate_report(self, orchestrator_result: Dict) -> bytes:
        """
        Generate PDF report from orchestrator result.
        
        Args:
            orchestrator_result: Output from OrchestratorAgent
            
        Returns:
            PDF file as bytes
        """
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        
        elements = []
        
        # Title
        elements.append(Paragraph(
            "🚀 Multi-Agent Code Generation Report",
            self.styles['CustomTitle']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Metadata
        elements.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Feature Spec
        elements.append(Paragraph("Feature Specification", self.styles['SectionHead']))
        elements.append(Paragraph(
            orchestrator_result.get('feature_spec', 'N/A'),
            self.styles['CustomBody']
        ))
        elements.append(Spacer(1, 0.2*inch))
        
        # Summary
        summary = orchestrator_result.get('summary', {})
        elements.append(Paragraph("Project Summary", self.styles['SectionHead']))
        
        summary_data = [
            ["Metric", "Value"],
            ["Pipeline Status", summary.get('pipeline_status', 'Unknown').upper()],
            ["Architecture", "✅ Complete" if summary.get('architecture_complete') else "❌ Failed"],
            ["Code Generated", "✅ Complete" if summary.get('code_generated') else "❌ Failed"],
            ["Tests Generated", "✅ Complete" if summary.get('tests_generated') else "❌ Failed"],
            ["Security Audited", "✅ Complete" if summary.get('security_audited') else "❌ Failed"],
            ["Critical Issues", str(summary.get('critical_count', 0))],
            ["Medium Issues", str(summary.get('medium_count', 0))],
            ["Total Issues", str(summary.get('total_issues', 0))],
        ]
        
        table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Architecture
        pipeline = orchestrator_result.get('pipeline', {})
        if 'architecture' in pipeline:
            elements.append(Paragraph("System Architecture", self.styles['SectionHead']))
            arch_output = pipeline['architecture'].get('output', 'No output')
            elements.append(Preformatted(arch_output[:1500], self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Generated Code
        if 'code' in pipeline:
            elements.append(PageBreak())
            elements.append(Paragraph("Generated Code", self.styles['SectionHead']))
            code = pipeline['code'].get('extracted_code') or pipeline['code'].get('output', '')
            code_preview = code[:2000] + "\n... [truncated]" if len(code) > 2000 else code
            elements.append(Preformatted(code_preview, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Test Cases
        if 'tests' in pipeline:
            elements.append(Paragraph("Generated Tests", self.styles['SectionHead']))
            tests = pipeline['tests'].get('extracted_tests') or pipeline['tests'].get('output', '')
            tests_preview = tests[:1500] + "\n... [truncated]" if len(tests) > 1500 else tests
            elements.append(Preformatted(tests_preview, self.styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Security Audit
        if 'security' in pipeline:
            elements.append(PageBreak())
            elements.append(Paragraph("Security Audit Report", self.styles['SectionHead']))
            security = pipeline['security'].get('output', 'No output')
            elements.append(Paragraph(security, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Issues Summary
        issues = orchestrator_result.get('issues', {})
        if issues.get('critical') or issues.get('medium'):
            elements.append(PageBreak())
            elements.append(Paragraph("Issues Found", self.styles['SectionHead']))
            
            if issues.get('critical'):
                elements.append(Paragraph("<b>🔴 Critical Issues</b>", self.styles['Normal']))
                for issue in issues['critical']:
                    elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
            
            if issues.get('medium'):
                elements.append(Paragraph("<b>🟡 Medium Issues</b>", self.styles['Normal']))
                for issue in issues['medium']:
                    elements.append(Paragraph(f"• {issue}", self.styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()