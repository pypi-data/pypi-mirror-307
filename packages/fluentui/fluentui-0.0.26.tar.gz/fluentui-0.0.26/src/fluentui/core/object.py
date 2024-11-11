class ObjectMix:
    def __init__(self,
                 *args,
                 key='',
                 parent=None,
                 props: dict = None,
                 **kwargs
                 ):
        super().__init__(parent=parent, *args)
        self.setObjectName(key)
        for name, value in (props or {}).items():
            self.setProperty(name, value)
