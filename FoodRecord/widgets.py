from django import forms

class MyDateWidget(forms.MultiWidget):
    
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'YYYY', 'size': 3}),
            forms.TextInput(attrs={'placeholder': 'MM', 'size': 1}),
            forms.TextInput(attrs={'placeholder': 'DD', 'size': 1})
        ]
        super(MyDateWidget, self).__init__(widgets, attrs)
    
    def format_output(self, values):
        return ' / '.join(values)
        
    def decompress(self, value):
        if value is None:
            return [None, None, None]
        values = [f for f in value.split('-')]
        try:
            return [values[0], values[1], values[2]]
        except IndexError:
            try:
                return [values[0], values[1], None]
            except IndexError:
                try:
                    return [values[0], None, None]
                except IndexError:
                    return [None, None, None]
    
class MyDateField(forms.MultiValueField):
    widget = MyDateWidget
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(),
            forms.CharField(),
            forms.CharField(),
        )
        super(MyDateField, self).__init__(fields=fields, *args, **kwargs)
    
    def compress(self, values):
        if any((f != '' for f in values)):
            return '-'.join([v for v in values if v != ''])
        return None    
        
class MyTimeWidget(forms.MultiWidget):
    
    def __init__(self, attrs=None):
        widgets = [
            forms.TextInput(attrs={'placeholder': 'HH', 'size': 1}),
            forms.TextInput(attrs={'placeholder': 'MM', 'size': 1}),
            forms.Select(choices=(('AM', 'AM'), ('PM', 'PM'))),
        ]
        super(MyTimeWidget, self).__init__(widgets, attrs)
    
    def format_output(self, values):
        return ' '.join([' : '.join([values[0], values[1]]), values[2]])
        
    def decompress(self, value):
        if value is None:
            return [None, None, 'AM']
        else:
            H = value.split(':')[0]
            M = value.split(':')[1]
            if int(H) > 11:
                return [H, M, 'PM']
            else:
                return [H, M, 'AM']
    
class MyTimeField(forms.MultiValueField):
    widget = MyTimeWidget
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(),
            forms.CharField(),
            forms.ChoiceField(choices=(('AM', 'AM'), ('PM', 'PM')))
        )
        super(MyTimeField, self).__init__(fields=fields, *args, **kwargs)
    
    def compress(self, values):
        if values[0] != '' and values[1] != '':
            return ':'.join([values[0], values[1]])
        return None
        