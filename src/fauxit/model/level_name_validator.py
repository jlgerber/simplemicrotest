import re
from fauxit.model.level import Level

class LevelNameValidator(object):
    show_re = re.compile("^[A-Z]+[A-Z0-9]*[A-Z]+$")
    sequence_re = re.compile("^[A-Z]{2}[A-Z0-9]*$")
    shot_re = re.compile("^[0-9]+[A-Z0-9]*$")

    @classmethod
    def validate(cls, name, level):
        if name is None:
            return None
        # Validate naming based on level. Return the name if
        # valid. Otherwise raise a KeyError or RuntimeError
        def valid(matchfnc,levelstr, name):
            if matchfnc(name):
                return name
            raise KeyError("{} is not a valid {} name".format(name, levelstr))

        if level == Level.show:
            return valid(cls.show_re.match,"show", name)
        elif level == Level.sequence:
            return valid(cls.sequence_re.match,"sequence", name)
        elif level == Level.shot:
            return valid(cls.shot_re.match,"shot", name)
        raise RuntimeError("Invalid level supplied: {}", str(level))

