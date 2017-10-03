import requests
import pytz
from django.utils import timezone


class UserTimezoneMiddleware(object):
    """ Middleware to check user timezone. """
    def process_request(self, request):
        user_time_zone = request.session.get('user_time_zone', None)
        try:
            if user_time_zone is None:
                freegeoip_response = requests.get('http://freegeoip.net/json/{0}'.format(request.META.get('REMOTE_ADDR')))
                freegeoip_response_json = freegeoip_response.json()
                user_time_zone = freegeoip_response_json['time_zone']
                if user_time_zone:
                    request.session['user_time_zone'] = user_time_zone
            timezone.activate(pytz.timezone(user_time_zone))
        except:
            pass
        return None
