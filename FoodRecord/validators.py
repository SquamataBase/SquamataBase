from django.core.exceptions import ValidationError

def validate_time(value):
    hhmm = value.split(':')
    if len(hhmm) != 2:
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if len(hhmm[0]) != 2:
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if len(hhmm[1]) != 2:
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if not hhmm[0].isdigit():
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if not hhmm[1].isdigit():
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if int(hhmm[0]) > 23:
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    if int(hhmm[1]) > 59:
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    

def validate_date(value):
    ymd = value.split('-')    
    if len(ymd[0]) != 4 or not ymd[0].isdigit():
        raise ValidationError(
            '%(value)s is the wrong format', params = {'value': value})
    try:    
        if len(ymd[1]) != 2 or not ymd[1].isdigit():
            raise ValidationError(
                '%(value)s is the wrong format', params = {'value': value})
        if int(ymd[1]) > 12:
            raise ValidationError(
                '%(value)s is the wrong format', params = {'value': value})
    except IndexError:
        pass
    try:    
        if len(ymd[2]) != 2 or not ymd[2].isdigit():
            raise ValidationError(
                '%(value)s is the wrong format', params = {'value': value})
        if int(ymd[2]) > 31:
            raise ValidationError(
                '%(value)s is the wrong format', params = {'value': value})
    except IndexError:
        pass
        