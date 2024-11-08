from django.utils.deprecation import MiddlewareMixin
import json
from django.http import JsonResponse
from .encryption_utility import EncryptionUtility

EXCLUDED_PATHS = [
    '/admin/alerts/brandalert/get_brands/',
    '/admin/alerts/brandalert/get_address/',
    '/admin/alerts/brandalert/get_users/',
    '/admin/alerts/brandalert/get_assignee/',
    '/admin/alerts/digitalassetalert/get_digital_asset/',
    '/admin/alerts/digitalassetalert/get_digital_application/',
    '/admin/alerts/digitalassetalert/get_owned_brand_domain/',
    '/admin/alerts/digitalassetalert/get_product_brand_media/',
    '/admin/alerts/digitalassetalert/get_color_scheme/',
    '/admin/alerts/communicationchannelalert/get_users/',
    '/admin/alerts/communicationchannelalert/get_phone_number/',
    '/admin/alerts/communicationchannelalert/get_email/',
    '/admin/alerts/communicationchannelalert/get_sender_id/',
    '/admin/alerts/communicationchannelalert/get_social_media/',
    '/admin/alerts/communicationchannelalert/get_chat_application/',
    '/admin/alerts/intellectualpropertyalert/get_users/',
    '/admin/alerts/intellectualpropertyalert/get_patent/',
    '/admin/alerts/intellectualpropertyalert/get_copyright/',
    '/admin/alerts/itinfrastructurealert/get_users/',
    '/admin/alerts/itinfrastructurealert/get_server/',
    '/admin/alerts/itinfrastructurealert/get_os/',
    '/admin/alerts/itinfrastructurealert/get_firewall/',
    '/admin/alerts/itinfrastructurealert/get_on_premise_software/',
    '/admin/alerts/itinfrastructurealert/get_router_and_switch/',
    '/admin/alerts/employeealert/get_users/',
    '/admin/alerts/employeealert/get_team/',
    '/admin/alerts/supplychainalert/get_users/',
    '/admin/alerts/supplychainalert/get_vendors/',
]


class DecryptRequestMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # Skip decryption for excluded paths
        if request.path in EXCLUDED_PATHS:
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
        if request.path in EXCLUDED_PATHS:
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
