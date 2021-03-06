import io
from io import BytesIO  # A stream implementation using an in-memory bytes buffer
# It inherits BufferIOBase
from io import StringIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

# pisa is a html2pdf converter using the ReportLab Toolkit,
# the HTML5lib and pyPdf.
#
from xhtml2pdf import pisa
# define render_to_pdf() function
def render_to_pdf(template_src, params={}):
    template = get_template(template_src)
    #context = Context(context_dict)
    html = template.render(params)
    result = BytesIO()
    # This part will create the pdf.
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
