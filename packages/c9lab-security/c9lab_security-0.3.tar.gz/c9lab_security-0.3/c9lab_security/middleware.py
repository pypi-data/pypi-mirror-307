from django.utils.deprecation import MiddlewareMixin
import json
from django.http import JsonResponse
from .encryption_utility import EncryptionUtility
from django.conf import settings


class DecryptRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # Skip decryption for excluded paths
        if request.path in getattr(settings, 'MIDDLEWARE_EXCLUDED_PATHS', []):
            return None

        if request.content_type == 'application/json':
            try:
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                encrypted_data = body_data.get('statistics')
                if encrypted_data:
                    decrypted_data = EncryptionUtility.decrypt(encrypted_data)
                    # Modify the request body with the decrypted data
                    request._body = json.dumps(decrypted_data).encode('utf-8')
            except Exception as e:
                return JsonResponse({'error': 'Decryption failed', 'details': str(e)}, status=400)
        return None


class EncryptResponseMiddleware(MiddlewareMixin):
    def process_response(self, request, response):

        # Skip encryption for excluded paths
        if request.path in getattr(settings, 'MIDDLEWARE_EXCLUDED_PATHS', []):
            return response

        if response['Content-Type'] == 'application/json':
            try:
                data = response.content.decode()
                encrypted_data = EncryptionUtility.encrypt(data)
                response.content = json.dumps({
                    'statistics': encrypted_data
                }).encode()
            except Exception as e:
                return JsonResponse({'error': 'Encryption failed'}, status=500)
        return response
