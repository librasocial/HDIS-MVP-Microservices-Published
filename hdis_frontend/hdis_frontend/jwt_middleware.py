class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        
    
    def process_response(self, request, response):
        access_token = request.session.get('access_token')
        refresh_token = request.session.get('refresh_token')
        print('at')
        print(access_token)
        if access_token:
            val=f'Bearer {access_token}'
            print(val)
            request.META['HTTP_AUTHORIZATION'] = val

            #request.headers['Authorization'] = f'Bearer {access_token}'

        request.META['HTTP_VENKAT'] = 'oktata'
        response = self.get_response(request)
        return response
