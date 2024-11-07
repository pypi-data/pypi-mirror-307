from abc import ABC
import jittor as jt
class Extension(ABC):
    def _get_module_extension_hook(self,module):
        try:
            hook = getattr(self,  '_' + module.__class__.__name__)
        except AttributeError:
            hook = self._default
        return hook
    @jt.no_grad()
    def __call__(self, module, input, output):
        module_hook = self._get_module_extension_hook(module) 
        print('module_hook',module_hook) 
        if module_hook is not None:
            result = module_hook(module, input, output)
            setattr(module, self._name, result) 

    def _default(self, module, input, output):
        import pdb
        pdb.set_trace()
        raise NotImplementedError
    