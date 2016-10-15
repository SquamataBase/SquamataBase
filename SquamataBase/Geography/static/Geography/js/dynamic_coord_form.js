$(document).ready(function() {

    $('.field-coord_format').hide()
    $('.field-utm_zone').hide()
    
    function hideAll() {
        $('#id_verbatim_coordinates_0').hide();
        $('#id_verbatim_coordinates_1').hide();
        $('#id_verbatim_coordinates_2').hide();
        $('#id_verbatim_coordinates_3').hide();
        $('#id_verbatim_coordinates_4').hide();
        $('#id_verbatim_coordinates_5').hide();
        $('#id_verbatim_coordinates_6').hide();
        $('#id_verbatim_coordinates_7').hide();
        $('#id_verbatim_coordinates_8').hide();
        $('#id_verbatim_coordinates_9').hide();
    }
    
    function dms() {
        hideAll();
        $('#id_verbatim_coordinates_2').show();
        $('#id_verbatim_coordinates_3').show();
        $('#id_verbatim_coordinates_4').show();
        $('#id_verbatim_coordinates_5').show();
        $('#id_verbatim_coordinates_6').show();
        $('#id_verbatim_coordinates_7').show();
        $('#id_verbatim_coordinates_8').show();
        $('#id_verbatim_coordinates_9').show();
    }
    
    function dd() {
        hideAll();
        $('#id_verbatim_coordinates_2').show();
        $('#id_verbatim_coordinates_5').show();
        $('#id_verbatim_coordinates_6').show();
        $('#id_verbatim_coordinates_9').show();
    }
    
    function ddm() {
        hideAll();
        $('#id_verbatim_coordinates_2').show();
        $('#id_verbatim_coordinates_3').show();
        $('#id_verbatim_coordinates_5').show();
        $('#id_verbatim_coordinates_6').show();
        $('#id_verbatim_coordinates_7').show();
        $('#id_verbatim_coordinates_9').show();
    }
    
    function utm() {
        hideAll();
        $('#id_verbatim_coordinates_0').show();
        $('#id_verbatim_coordinates_1').show();
        $('#id_verbatim_coordinates_2').show();
        $('#id_verbatim_coordinates_3').show();
    }
    
    function setHemiDynamic() {
        var x = $('#id_verbatim_coordinates_6').val();
        var y = $('#id_verbatim_coordinates_2').val();
        if (x < 0) {
            $('#id_verbatim_coordinates_9').val('W')
        } else if (x >= 0) {
            $('#id_verbatim_coordinates_9').val('E')
        }
        if (y < 0) {
            $('#id_verbatim_coordinates_5').val('S')
        } else if (y >= 0) {
            $('#id_verbatim_coordinates_5').val('N')
        }
    }
    
    // if the user doesn't know about +/- signs for indicating hemisphere
    // automatically adjust sign of input when user changes select box
    function setHemiStatic() {
        var lat_h = $('#id_verbatim_coordinates_5').val();
        var lon_h = $('#id_verbatim_coordinates_9').val();
        var x = $('#id_verbatim_coordinates_6').val();
        var y = $('#id_verbatim_coordinates_2').val();
        if (x > 0 && lon_h === 'W') { 
            $('#id_verbatim_coordinates_6').val(-1 * x);
        } else if (x < 0 && lon_h === 'E') {
            $('#id_verbatim_coordinates_6').val(-1 * x)
        }
        if (y > 0 && lat_h === 'S') {
            $('#id_verbatim_coordinates_2').val(-1 * y);
        } else if (y <= 0 && lat_h === 'N') {
            $('#id_verbatim_coordinates_2').val(-1 * y);
        }
    }
    
    var w = $('#id_verbatim_coordinates_10 :selected').val();
    $('#id_coord_format').val(w);
    $('#id_utm_zone').val($('#id_verbatim_coordinates_0').val());
    
    if (w === 'DMS') {
        dms();
    } else if (w === 'DD') {
        dd();
    } else if (w === 'DDM') {
        ddm();
    } else if (w === 'UTM') {
        utm();
    }
    
    setHemiDynamic();
    
    $('#id_verbatim_coordinates_10').on('change', function() {
        var v = $('#id_verbatim_coordinates_10 :selected').val();
        $('#id_coord_format').val(v)
        if (v === 'DMS') {
            dms();
        } else if (v === 'DD') {
            dd();
        } else if (v === 'DDM') {
            ddm();
        } else if (v === 'UTM') {
            utm();
        }
        
        w = v;
    });
    
    $('.field-verbatim_coordinates > div > input').on('input', function() {
        setHemiDynamic();
    });
    
    $('#id_verbatim_coordinates_5, #id_verbatim_coordinates_9').on('change', function() {
        setHemiStatic();
    });
    
    $('#id_verbatim_coordinates_0').on('change', function() {
        $('#id_utm_zone').val($('#id_verbatim_coordinates_0').val());
    });
    
});
