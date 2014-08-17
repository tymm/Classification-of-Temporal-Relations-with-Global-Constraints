class RelationType:
    BEFORE = 0
    IS_INCLUDED = 1
    AFTER = 2
    INCLUDES = 3
    ENDS = 4
    ENDED_BY = 5
    IBEFORE = 6
    IAFTER = 7
    SIMULTANEOUS = 8
    BEGINS = 9
    BEGUN_BY = 10
    DURING = 11
    DURING_INV = 12
    UNKNOWN = 13
    NONE = 14

    @classmethod
    def get_string_by_id(cls, ID):
        if ID == cls.BEFORE:
            return "BEFORE"
        elif ID == cls.IS_INCLUDED:
            return "IS_INCLUDED"
        elif ID == cls.AFTER:
            return "AFTER"
        elif ID == cls.INCLUDES:
            return "INCLUDES"
        elif ID == cls.ENDS:
            return "ENDS"
        elif ID == cls.ENDED_BY:
            return "ENDED_BY"
        elif ID == cls.IBEFORE:
            return "IBEFORE"
        elif ID == cls.IAFTER:
            return "IAFTER"
        elif ID == cls.SIMULTANEOUS:
            return "SIMULTANEOUS"
        elif ID == cls.BEGINS:
            return "BEGINS"
        elif ID == cls.BEGUN_BY:
            return "BEGUN_BY"
        elif ID == cls.DURING:
            return "DURING"
        elif ID == cls.DURING_INV:
            return "DURING_INV"
        elif ID == cls.UNKNOWN:
            return "VAGUE"
        elif ID == cls.NONE:
            return "NONE"



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
        elif text == "ENDED_BY":
            return cls.ENDED_BY
        elif text == "IBEFORE":
            return cls.IBEFORE
        elif text == "IAFTER":
            return cls.IAFTER
        elif text == "BEGINS":
            return cls.BEGINS
        elif text == "BEGUN_BY":
            return cls.BEGUN_BY
        elif text == "DURING":
            return cls.DURING
        elif text == "DURING_INV":
            return cls.DURING_INV
        elif text == "SIMULTANEOUS":
            return cls.SIMULTANEOUS
        elif text == "NONE":
            return cls.NONE
        else:
            return cls.UNKNOWN

    def __iter__(self):
        return iter([self.BEFORE, self.IS_INCLUDED, self.INCLUDES, self.AFTER, self.ENDS, self.ENDED_BY, self.IBEFORE, self.IAFTER, self.BEGINS, self.BEGUN_BY, self.DURING, self.DURING_INV, self.SIMULTANEOUS, self.NONE, self.UNKNOWN])
