$(document).ready(function() {
     
    
    $('.field-taxon_lookup_context > select').on('change', function() {

        if ($(this).children('option:selected').val() !== 'life') {
            $(this).parent().parent().siblings('.field-taxon').find('select').prop('disabled', false);   
        } else {
            $(this).parent().parent().siblings('.field-taxon').find('select').prop('disabled', true);
        }

    });

    var x = document.getElementsByClassName('field-taxon_lookup_context');
    $(x).children('select').trigger('change');

});
