from typing import TYPE_CHECKING
if TYPE_CHECKING:
	# Help static analyzers resolve the import while avoiding runtime errors if Django isn't installed.
	from django.contrib import admin  # type: ignore

try:
	import importlib
	django_contrib = importlib.import_module("django.contrib")
	admin = django_contrib.admin
except Exception:
	# Provide a lightweight fallback so this module can be imported outside a Django environment
	class _DummySite:
		def register(self, *args, **kwargs):
			return None

	class _DummyAdmin:
		site = _DummySite()

	admin = _DummyAdmin()

# Register your models here.

from .models import Appointment, SalonBooking, Service, Staff

try:
	admin.site.register(SalonBooking)
	admin.site.register(Service)
	admin.site.register(Staff)
	admin.site.register(Appointment)
except Exception:
	# If registration fails (e.g. running outside Django), ignore to avoid import errors.
	pass
