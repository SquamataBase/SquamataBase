$(document).ready(function() {
    $('.field-parent_admin').hide();
    $('#id_parent_admin').val(null);
    
    // Bind on country field change
    $(':input[name$=adm0]').on('change', function() {
        
        // Clear the dependent autocompletes with the same prefix
        $(':input[name=adm1]').val(null).trigger('change');
        $(':input[name=adm2]').val(null).trigger('change');
        
        // set the parent admin
        $('#id_parent_admin').val($(this).val());
    });
    
    // Bind on state field change
    $(':input[name$=adm1]').on('change', function() {
        // Get the field prefix, ie. if this comes from a formset form
        var prefix = $(this).getFormPrefix();
        
        // Clear the dependent autocomplete with the same prefix
        $(':input[name=adm2]').val(null).trigger('change');
        
        // set the parent admin
        $('#id_parent_admin').val($(this).val());
        
        if ($('#id_parent_admin').val() === '') {
            
            $('#id_parent_admin').val($(':input[name=adm0]').val());
        }
        
    });
});