class ReportsRouter:
    """
    Router de base de datos para separar el esquema propio de reportes
    de las tablas académicas de solo lectura.
    """
    def db_for_read(self, model, **hints):
        return "default" if model._meta.app_label == "reports" else "follow"

    def db_for_write(self, model, **hints):
        return "default" if model._meta.app_label == "reports" else "follow"

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._meta.app_label == obj2._meta.app_label

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default" and app_label == "reports"
