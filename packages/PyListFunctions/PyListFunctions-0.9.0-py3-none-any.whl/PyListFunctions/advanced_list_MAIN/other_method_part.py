from .lock_part import lock_part
__all__ = ['other_method_part']


class other_method_part(lock_part):
    def __add__(self, other):
        if self.ignore_error:
            if self.no_prompt:
                return
            print("advanced_list not supported __add__ method!")
        else:
            raise NotImplementedError("advanced_list not supported the __add__ method!")
        super().__add__(other)
