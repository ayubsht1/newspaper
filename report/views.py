import csv
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
# Create your views here.
import tempfile
from django.template.loader import render_to_string
from weasyprint import HTML
from newspaper.models import Post
User = get_user_model()

COLUMNS = [
    "first_name",
    "last_name",
    "username",
    "email",
    "is_staff",
    "is_active",
    "is_superuser",
    "last_login",
    "date_joined",
]

class UserReportView(View):
    def get(self, request):
        """documentation"""
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=users.csv"

        users = User.objects.all().only(*COLUMNS).values(*COLUMNS)

        writer = csv.DictWriter(response, fieldnames=users[0].keys())
        writer.writeheader()
        writer.writerows(users)

        return response

# class PostPdfFileView(View):
#     def get(self, request,*args,**kwargs):
#         posts= Post.objects.all()
#         html_string = render_to_string("reports/posts.html", {"posts":posts})
#         html = HTML(string=html_string, base_url=request.build_absolute_uri())
#         result = html.write_pdf()

#         response = HttpResponse(content_type="application/pdf;")
#         response["Content-Disposition"]= "inline; filename=posts.pdf"
#         response["Content-Transfer-Encoding"]="binary"
        
#         with tempfile.NamedTemporaryFile(delete=True) as output:
#             output.write(result)
#             output.flush()

#             with open(output.name, "rb") as f:
#                 response.write(f.read())

#         return response

