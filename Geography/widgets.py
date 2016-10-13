from django import forms


class CoordinateWidget(forms.MultiWidget):
    COORDS = (
        ('DD', 'Decimal Degrees'),
        ('DDM', 'Degrees Decimal Minutes'),
        ('DMS', 'Degrees Minutes Seconds'),
        ('UTM', 'Universal Transverse Mercator')
    )
    
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(choices=((i, i) for i in range(1, 61))),
            forms.Select(choices=(('N', 'N'), ('S', 'S'))),
            forms.TextInput(attrs={'size': 7}),
            forms.TextInput(attrs={'size': 7}),
            forms.TextInput(attrs={'size': 7}),
            forms.Select(choices=(('N', 'N'), ('S', 'S'))),
            forms.TextInput(attrs={'size': 7}), 
            forms.TextInput(attrs={'size': 7}),
            forms.TextInput(attrs={'size': 7}),
            forms.Select(choices=(('E', 'E'), ('W', 'W'))),
            forms.Select(choices=self.COORDS) 
        ]
        super(CoordinateWidget, self).__init__(widgets, attrs)
    
    def format_output(self, values):
        f = values.pop(-1)
        values.insert(0, f)
        return ' '.join(values)
    
    def decompress(self, value):
        if value:
            if value.find("''") != -1:
                lat = value.split()[0]
                lon = value.split()[1]
                deg0 = lat[0:lat.find('°')]
                min0 = lat[(lat.find('°')+1):lat.find("'")]
                sec0 = lat[(lat.find("'")+1):lat.find("''")]
                dir0 = lat[-1]
                deg1 = lon[0:lon.find('°')]
                min1 = lon[(lon.find('°')+1):lon.find("'")]
                sec1 = lon[(lon.find("'")+1):lon.find("''")]
                dir1 = lon[-1]
                return [None, None, deg0, min0, sec0,
                        dir0, deg1, min1, sec1, dir1, 'DMS']
            elif value.find("'") != -1:
                lat = value.split()[0]
                lon = value.split()[1]
                deg0 = lat[0:lat.find('°')]
                min0 = lat[(lat.find('°')+1):lat.find("'")]
                dir0 = lat[-1]
                deg1 = lon[0:lon.find('°')]
                min1 = lon[(lon.find('°')+1):lon.find("'")]
                dir1 = lon[-1]
                return [None, None, deg0, min0, None,
                        dir0, deg1, min1, None, dir1, 'DDM']
            elif value.find("°") != -1:
                lat = value.split()[0]
                lon = value.split()[1]
                deg0 = lat[0:lat.find('°')]
                dir0 = lat[-1]
                deg1 = lon[0:lon.find('°')]
                dir1 = lon[-1]
                return [None, None, deg0, None, None,
                        dir0, deg1, None, None, dir1, 'DD']
            else:
                toks = value.split()
                Z = toks[2][0:-1]
                H = toks[2][-1]
                E = toks[3][0:-1]
                N = toks[4][0:-1]
                return [Z, H, E, N, None,
                        None, None, None, None, None, 'UTM']
        else:
            return [None, None, None, None, None,
                    None, None, None, None, None, None]


class CoordinateField(forms.MultiValueField):
    widget = CoordinateWidget
    
    COORDS = (
        ('DD', 'Decimal Degrees'),
        ('DDM', 'Degrees Decimal Minutes'),
        ('DMS', 'Degrees Minutes Seconds'),
        ('UTM', 'Universal Transverse Mercator')
    )
    
    def __init__(self, *args, **kwargs):
        fields = (
            forms.ChoiceField(choices=((i, i) for i in range(1, 61))),
            forms.ChoiceField(choices=(('N', 'N'), ('S', 'S'))),
            forms.CharField(),
            forms.CharField(),
            forms.CharField(),
            forms.ChoiceField(choices=(('N', 'N'), ('S', 'S'))),
            forms.CharField(),
            forms.CharField(),
            forms.CharField(),
            forms.ChoiceField(choices=(('E', 'E'), ('W', 'W'))),
            forms.ChoiceField(choices=self.COORDS)
        )
        super(CoordinateField, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, values):
        crds = [values[2], values[3], values[4], values[6], values[7], values[8]]
        if any((f != '' for f in crds)):
            if values[10] == 'DD':
                return "{}°{} {}°{}".format(values[2], values[5], values[6], values[9])
            elif values[10] == 'DDM':
                return "{}°{}'{} {}°{}'{}".format(values[2], values[3], values[5], values[6], values[7], values[9])
            elif values[10] == 'DMS':
                return "{}°{}'{}''{} {}°{}'{}''{}".format(values[2], values[3], values[4], values[5], values[6], values[7], values[8], values[9])
            elif values[10] == 'UTM':
                return "UTM Zone {}{} {}E {}N".format(values[0], values[1], values[2], values[3])
            else:
                return None
        return None
