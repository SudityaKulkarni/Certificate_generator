from django.shortcuts import render
from django.http import HttpResponse
from .forms import CertificateForm
from .models import Certificate
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader

def generate_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()

            # Set up PDF response
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.name}_certificate.pdf"'

            # Create a canvas with landscape mode
            p = canvas.Canvas(response, pagesize=landscape(letter))
            width, height = landscape(letter)

            # Add border
            border_margin = 20
            p.setStrokeColor(colors.black)
            p.setLineWidth(5)
            p.rect(border_margin, border_margin, width - 2 * border_margin, height - 2 * border_margin)

            # Add heading
            p.setFont("Helvetica-Bold", 36)
            p.drawCentredString(width / 2, height - 100, "Certificate of Completion")

            # Add recipient's name
            p.setFont("Helvetica-Bold", 28)
            p.setFillColor(colors.darkblue)
            p.drawCentredString(width / 2, height - 200, certificate.name)

            # Add course name
            p.setFont("Helvetica", 20)
            p.setFillColor(colors.black)
            p.drawCentredString(width / 2, height - 250, f"has successfully completed the {certificate.course} course.")

            # Add issue date
            p.setFont("Helvetica-Oblique", 16)
            p.drawCentredString(width / 2, height - 300, f"Issued on: {certificate.date_issued}")

            # Add a logo (if you have one)
            try:
                logo_path = "path/to/your/logo.png"  # Change this to your actual logo path
                logo = ImageReader(logo_path)
                p.drawImage(logo, width - 180, height - 120, width=100, height=100, mask='auto')
            except:
                pass  # Skip if no logo found

            # Add a signature (if needed)
            try:
                signature_path = "path/to/signature.png"  # Change this to actual path
                signature = ImageReader(signature_path)
                p.drawImage(signature, width / 2 - 50, 100, width=150, height=50, mask='auto')
                p.setFont("Helvetica", 14)
                p.drawCentredString(width / 2, 80, "Authorized Signature")
            except:
                pass  # Skip if no signature found

            # Save and return the PDF
            p.showPage()
            p.save()
            return response
    else:
        form = CertificateForm()

    return render(request, 'certificate_form.html', {'form': form})
