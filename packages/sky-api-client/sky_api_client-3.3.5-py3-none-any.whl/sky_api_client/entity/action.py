from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('action')
class Action(Entity):
    LIST_URL = '/constituent/v1/constituents/{id}/actions'
    CREATE_URL = '/constituent/v1/actions'
    GET_URL = '/constituent/v1/actions/{id}'
    UPDATE_URL = '/constituent/v1/actions/{id}'
    DELETE_URL = '/constituent/v1/actions/{id}'
    LIST_ALL_URL = '/constituent/v1/actions'
    TYPES_URL = '/constituent/v1/actiontypes'
