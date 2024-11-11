class enum:
    def __init__(self, *args):
        for i, name in enumerate(args):
            setattr(self, name, i)

    def __repr__(self):
         return f"<enum: {', '.join([f'{name}={getattr(self, name)}' for name in self.__dict__])}>"