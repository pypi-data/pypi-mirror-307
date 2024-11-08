class AddScene:
    def __init__(self):
        self.__table_features_any = []
        self.__table_features_help = []
        self.__table_features_whatcyd = []
        self.__table_features = []

    def any(self):
        def wrapper(func):
            self.__table_features_any.append(func)
        return wrapper
    
    def help(self):
        def wrapper(func):
            self.__table_features_help.append(func)
        return wrapper
    
    def whatcyd(self):
        def wrapper(func):
            self.__table_features_whatcyd.append(func)
        return wrapper

    def command(self, *args):
        def wrapper(func):
            self.__table_features.append({func: args[0]})
        return wrapper

    def __get_response(self, command_txt, ctx):
        if command_txt == 'помощь' and self.__table_features_help:
            return self.__table_features_help[0](ctx)
        if command_txt == 'что ты умеешь' and self.__table_features_whatcyd:
            return self.__table_features_whatcyd[0](ctx)
        for func in self.__table_features:
            for text_f in func:
                if command_txt in func[text_f]:
                    return text_f(ctx)
        return None

    def __route_scene(self, ctx, command_txt):
        if not (result_response := self.__get_response(command_txt, ctx)):
            result_response = self.__table_features_any[0](ctx)
        return result_response