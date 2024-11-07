from waddle import ParamBunch

from .base import BaseConnector


class Bigquery(BaseConnector):
    engine = 'bigquery'

    @classmethod
    def connect(cls, conf: ParamBunch, *args, project=None, credentials_path=None,
                **kwargs):
        from google.cloud.bigquery import Client
        from google.cloud.bigquery.dbapi.connection import Connection
        project = project or conf.get('project')
        credentials_path = credentials_path or conf.get('credentials_path')
        if not credentials_path:
            creds = {}
            keys = [
                'private_key_id',
                'private_key',
                'client_id',
                'client_email',
                'auth_uri',
                'token_uri',
                'auth_provider_x509_cert_url',
                'client_x509_cert_url',
            ]
            for key in keys:
                value = kwargs.get(key)
                if conf:
                    value = value or conf.get(key)
                if value is not None:
                    creds[key] = value
            client = Client.from_service_account_info(project=project, info=creds)
        else:
            client = Client.from_service_account_json(
                project=project,
                json_credentials_path=credentials_path)
        return Connection(client=client)

    @classmethod
    def sql_alchemy_connection_string(
            cls, conf: ParamBunch, *args,
            project=None, client_id=None, client_email=None,
            private_key_id=None, private_key=None, auth_uri=None,
            token_uri=None, auth_provider_x509_cert_url=None,
            client_x509_cert_url=None, **kwargs):
        creds = {}
        project = project or conf.get('project')
        return f'bigquery://{project}'
