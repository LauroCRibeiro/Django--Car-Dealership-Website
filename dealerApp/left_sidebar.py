from .models import Brand
def left_sidebar(request):
	brands=Brand.objects.all()
	return {'brands':brands}