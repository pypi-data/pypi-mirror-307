from django.apps import AppConfig


class FloorPlansConfig(AppConfig):
    name = "NEMO_floor_plans"
    verbose_name = "NEMO Floor Plans"

    def ready(self):
        """
        This code will be run when Django starts.
        """
        pass
