from sky_api_client.entity.base import Entity
from sky_api_client.entity.registry import EntityRegistry


@EntityRegistry.register('action_status')
class ActionStatus(Entity):
    LIST_URL = '/constituent/v1/actionstatustypes'
