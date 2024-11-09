from ..extension import Extension


class ForwardOutputExtension(Extension):

    def __init__(self):
        self._name = 'output'
        super(ForwardOutputExtension, self).__init__()

    def _default(self, module, input, output):
        return output[0]

    def _Linear(self, module, input, output):
        return output[0]

    def _Conv(self, module, input, output):
        return output[0]



