from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from .forms import CertificateForm
from .models import Certificate
from reportlab.pdfgen import canvas

def generate_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()

            # Generate PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.name}_certificate.pdf"'

            p = canvas.Canvas(response)
            p.setFont("Helvetica-Bold", 20)
            p.drawString(200, 750, "Certificate of Completion")
            p.setFont("Helvetica", 14)
            p.drawString(200, 720, f"This certifies that {certificate.name}")
            p.drawString(200, 690, f"has successfully completed the {certificate.course} course.")
            p.drawString(200, 660, f"Issued on: {certificate.date_issued}")

            p.showPage()
            p.save()
            return response
    else:
        form = CertificateForm()

    return render(request, 'certificate_form.html', {'form': form})


