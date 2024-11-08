class Alice:

    def __init__(self):
        self.__table_features = []
        self.__table_features_any = []
        self.__table_features_start = []
        self.__table_features_help = []
        self.__table_features_whatcyd = []
        self.__table_features_timeout = []

    def start(self):
        def wrapper(func):
            self.__table_features_start.append(func)
        return wrapper
    
    def timeout(self):
        def wrapper(func):
            self.__table_features_timeout.append(func)
        return wrapper
    
    def help(self):
        def wrapper(func):
            self.__table_features_help.append(func)
        return wrapper
    
    def whatcyd(self):
        def wrapper(func):
            self.__table_features_whatcyd.append(func)
        return wrapper

    def any(self):
        def wrapper(func):
            self.__table_features_any.append(func)
        return wrapper

    def command(self, *args):
        def wrapper(func):
            if not type(args[0]) == list:
                self.__table_features.append({func: [args[0]]})
            else:
                self.__table_features.append({func: args[0]})
        return wrapper

    def __get_custom_func(self, command_txt, ctx):
        for func in self.__table_features:
            for text_f in func:
                if command_txt in func[text_f]:
                    return text_f(ctx)
        return None
    
    def __rout_scene(self, ctx):
        command_txt = ' '.join(ctx['json']['request']['nlu']['tokens'])
        if not (scene := ctx['json']['state']['session'].get('s')):
            if command_txt == 'помощь' and self.__table_features_help:
                return self.__table_features_help[0](ctx)
            if command_txt == 'что ты умеешь' and self.__table_features_whatcyd:
                return self.__table_features_whatcyd[0](ctx)
            if not(custom_response := self.__get_custom_func(command_txt, ctx)):
                custom_response = self.__table_features_any[0](ctx)
            return custom_response
        if scene_custom := getattr(self, scene, None):
            return scene_custom._AddScene__route_scene(ctx, command_txt)
        raise ValueError(f'!! -> Ошибка.. Сцены "{scene}" не существует.')

    def __create_response_json(self, custom_response):
        result_response = {
        "response": {
            "text": "",
            "tts": "",
            "end_session": False,
            "directives": {}
        },
        "session_state": {
            'd': g_ctx['data']['us']
        },
        "user_state_update": g_ctx['data']['ws'],
        "application_state": g_ctx['data']['as'],
        "analytics": {},
        "version": "1.0"
        }
        if g_ctx['data']['scene']:
            result_response['session_state']['s'] = g_ctx['data']['scene']
        if custom_response.get('card', None):
            result_response["response"]['card'] = custom_response['card']
        if custom_response.get('txt', None):
            result_response["response"]['text'], result_response["response"]['tts'] = self.__get_txt_tts(custom_response)
        if custom_response.get('buttons', None):
            result_response["response"]['buttons'] = custom_response['buttons']
        return result_response
    
    def run(self, ctx, timeout=3):
        import asyncio
        global g_ctx
        g_ctx = {}
        g_ctx['json'] = ctx
        g_ctx['data'] = {
            'us': ctx['state']['session'].get('d', {}),
            'ws': ctx['state'].get('user', {}),
            'as': ctx['state'].get('application', {}),
            'scene': ctx['state']['session'].get('s', '')
        }
        async def handler():
            if not ctx['session']['message_id']:
                custom_response = self.__table_features_start[0](g_ctx)
            else:   
                custom_response = self.__rout_scene(g_ctx)
            return self.__create_response_json(custom_response)
        async def timeout_function(timeout):
            try:
                result_ok = await asyncio.wait_for(handler(), timeout)
                return result_ok
            except asyncio.TimeoutError:
                if self.__table_features_timeout:
                    return self.__table_features_timeout[0](g_ctx)
        result_response = asyncio.run(timeout_function(timeout))
        return result_response

    @staticmethod
    def __get_txt_tts(custom_response):
        if type(custom_response['txt']) == list:
            from random import choice
            custom_response = choice(custom_response['txt'])
            if type(custom_response) == str:
                return custom_response, custom_response
        return custom_response['txt'], custom_response.get('tts', custom_response['txt'])