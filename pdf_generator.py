from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# Регистрация русских шрифтов (используем стандартный, можно заменить)
try:
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
except:
    # Если шрифта нет, используем стандартный
    pass

class PDFGenerator:
    @staticmethod
    def generate_osint_report(data: dict, report_type: str) -> str:
        """Генерирует OSINT-отчёт в PDF"""
        filename = f"osint_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        # Стили
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=8
        )
        
        story = []
        
        # Заголовок
        story.append(Paragraph("Mango Instruments - OSINT Report", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Тип отчёта
        type_names = {"person": "Личность", "company": "Компания", "project": "Проект"}
        story.append(Paragraph(f"Тип отчёта: {type_names.get(report_type, report_type)}", heading_style))
        story.append(Spacer(1, 0.3*cm))
        
        # Секция: Входные данные
        story.append(Paragraph("1. Входные данные", heading_style))
        for key, value in data['input'].items():
            story.append(Paragraph(f"• <b>{key}</b>: {value}", normal_style))
        
        story.append(Spacer(1, 0.3*cm))
        
        # Секция: Найденные данные
        story.append(Paragraph("2. Результаты OSINT-анализа", heading_style))
        for key, value in data['findings'].items():
            story.append(Paragraph(f"<b>{key}</b>", normal_style))
            if isinstance(value, list):
                for item in value:
                    story.append(Paragraph(f"  - {item}", normal_style))
            else:
                story.append(Paragraph(f"  {value}", normal_style))
        
        story.append(Spacer(1, 0.3*cm))
        
        # Секция: Риски
        story.append(Paragraph("3. Потенциальные риски", heading_style))
        for risk in data.get('risks', []):
            story.append(Paragraph(f"• {risk}", normal_style))
        
        story.append(Spacer(1, 0.3*cm))
        
        # Секция: Рекомендации
        story.append(Paragraph("4. Рекомендации", heading_style))
        for rec in data.get('recommendations', []):
            story.append(Paragraph(f"• {rec}", normal_style))
        
        story.append(Spacer(1, 0.3*cm))
        
        # Секция: Источники
        story.append(Paragraph("5. Источники данных", heading_style))
        for source in data.get('sources', []):
            story.append(Paragraph(f"• {source}", normal_style))
        
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Отчёт сгенерирован: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              ParagraphStyle('Date', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
        
        doc.build(story)
        return filename
    
    @staticmethod
    def generate_chain_report(chain_data: list, final_findings: dict) -> str:
        """Генерирует PDF с логической цепочкой"""
        filename = f"osint_chain_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=A4)
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=30
        )
        step_style = ParagraphStyle(
            'StepStyle',
            parent=styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        )
        
        story = []
        
        story.append(Paragraph("Mango Instruments - Логическая цепочка OSINT", title_style))
        story.append(Spacer(1, 0.5*cm))
        
        # Схема цепочки
        story.append(Paragraph("Схема расследования:", styles['Heading2']))
        story.append(Spacer(1, 0.3*cm))
        
        for step in chain_data:
            indent = " " * (step['depth'] * 2)
            text = f"{indent}├─ <b>Шаг {step['step']}</b>: {step['input']}<br/>"
            text += f"{indent}│   → Найдено: {step['findings']}<br/>"
            text += f"{indent}│   → Выбрано: {step['chosen_action']}"
            story.append(Paragraph(text, step_style))
            story.append(Spacer(1, 0.2*cm))
        
        story.append(Spacer(1, 0.5*cm))
        
        # Итоговые выводы
        story.append(Paragraph("Итоговые выводы:", styles['Heading2']))
        for key, value in final_findings.items():
            story.append(Paragraph(f"• <b>{key}</b>: {value}", step_style))
        
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"Схема сгенерирована: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                              ParagraphStyle('Date', parent=styles['Normal'], fontSize=8, textColor=colors.grey)))
        
        doc.build(story)
        return filename
