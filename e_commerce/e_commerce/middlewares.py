class MobileAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META['HTTP_USER_AGENT']

        if 'Mobile' in user_agent:
            print ('пользователь использует мобильный для просмотра страницы')
        # else:
        #     print ('пользователь использует компьютер для просмотра страницы')

        response = self.get_response(request)

        return response