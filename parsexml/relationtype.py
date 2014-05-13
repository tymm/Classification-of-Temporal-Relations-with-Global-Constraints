class RelationType:
    BEFORE = 0
    IS_INCLUDED = 1
    AFTER = 2
    INCLUDES = 3
    ENDS = 4
    SIMULTANEOUS = 5
    UNKNOWN = 6

    @classmethod
    def get_id(cls, text):
        if text == "BEFORE":
            return cls.BEFORE
        elif text == "IS_INCLUDED":
            return cls.IS_INCLUDED
        elif text == "INCLUDES":
            return cls.INCLUDES
        elif text == "AFTER":
            return cls.AFTER
        elif text == "ENDS":
            return cls.ENDS
        elif text == "SIMULTANEOUS":
            return cls.SIMULTANEOUS
        else:
            return cls.UNKNOWN
