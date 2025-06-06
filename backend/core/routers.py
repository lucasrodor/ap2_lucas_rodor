class EscolaRouter:
    """
    Roteador de banco de dados para enviar os modelos da app 'administracao'
    para o banco de dados 'escola'.
    """

    route_app_labels = {'administracao'}  # Nome da sua app com modelos que vão pro MySQL

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'escola'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'escola'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'escola'
        return None

class ImoveisRouter:
    """
    Roteador de banco de dados para enviar os modelos da app 'administracao'
    para o banco de dados 'imoveis'.
    """

    route_app_labels = {'webscrapping'}  # Nome da sua app com modelos que vão pro MySQL

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'imoveis'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'imoveis'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'imoveis'
        return None
