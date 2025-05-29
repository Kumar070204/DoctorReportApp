import openpyxl
from datetime import datetime
import json
import base64

def excel(request):
    try:
        # Parse JSON data
        data = request.get_json()
        if not data or 'entries' not in data:
            return {'error': 'Missing entries'}, 400

        entries = data['entries']
        if not entries:
            return {'error': 'No entries to export'}, 400

        # Create Excel workbook
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Daily Report"

        # Add headers
        headers = ["S.No", "Date", "Day", "Consultant", "Speciality", "Area", "Remarks"]
        ws.append(headers)

        # Add entries
        for entry in entries:
            ws.append([
                entry.get('sno', ''),
                entry.get('date', ''),
                entry.get('day', ''),
                entry.get('consultant', ''),
                entry.get('speciality', ''),
                entry.get('area', ''),
                entry.get('remarks', '')
            ])

        # Save to bytes
        from io import BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Encode as base64
        excel_data = base64.b64encode(output.getvalue()).decode('utf-8')
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"Daily Report {today} Ganesan.xlsx"

        return {
            'status': 200,
            'headers': {
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'Content-Disposition': f'attachment; filename="{filename}"'
            },
            'body': excel_data,
            'isBase64Encoded': True
        }
    except Exception as e:
        return {'error': str(e)}, 500