from drf_spectacular.utils import OpenApiResponse
from apps.users.serializers.login import LoginSerializer


doc_login = {
    'responses': {
        '201': OpenApiResponse(
            description='Operación exitosa.',
            response={'token': 'token'},
            ),
    },
    'operation_id': 'Login in the platform.',
    'description': 'Login in the platform.',
    'request': LoginSerializer
}
