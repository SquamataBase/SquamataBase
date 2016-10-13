$(document).ready(function() {
     
    var v = $('#id_taxon_context').val();
    
    $('#id_taxon').attr('data-placeholder', 'Search for ' + v + ' . . .');
    
    $('#id_taxon_context').on('change', function() {
        v = $('#id_taxon_context').val();
        $('#id_taxon').attr('data-placeholder', 'Search for ' + v + '. . .');
        $('#id_taxon').next().find('span.select2-selection__placeholder').text('Search for ' + v + ' . . .');
    });
    
    // placeholder defaults to initial value when selection is cleared unless
    // we add this hook to keep it as the currently selected reftype
    $(document).on('change', '#id_taxon', function() {
        v = $('#id_taxon_context').val();
        $('#id_taxon').attr('data-placeholder', 'Search for ' + v + ' . . .');
        $('#id_taxon').next().find('span.select2-selection__placeholder').text('Search for ' + v + ' . . .');
    });
    
});
