$(document).ready(function() {
    
    var pubs = [];
    pubs["---------"] = '';
    pubs["Journal article"] = 'journalarticle-group';
    pubs["Book chapter"] = 'bookchapter-group';
    pubs["Book"] = 'book-group';
    
    var init = pubs[$('#id_ref_type :selected').text()];
    
    $('#journalarticle-group').hide();
    $('#book-group').hide();
    $('#bookchapter-group').hide();
    $('#contribution_set-group').hide();
    
    var w = '';
    
    if (init === '') {
        // do nothing
    } else {
        // handle redirect back to add/change page because of form errors
    
        $('#' + init).show();
        $('fieldset h2').hide();
        $('fieldset h3').hide();
        
        $('#contribution_set-group').show();
        $('#contribution_set-group').find('h2').show();
        
        w = init;
    }
    
    $('#id_ref_type').on('change', function() {
        var v = pubs[$('#id_ref_type :selected').text()];
        if (v === '') {
            $('#journalarticle-group').hide();
            $('#book-group').hide();
            $('#bookchapter-group').hide();
            $('#contribution_set-group').hide();
        } else {
            $('#' + w).hide();
            $('#' + v).show();
            $('fieldset h2').hide();
            $('fieldset h3').hide();
        
            $('#contribution_set-group').show();
            $('#contribution_set-group').find('h2').show();
        
            w = v;
        }
    });
    
});
