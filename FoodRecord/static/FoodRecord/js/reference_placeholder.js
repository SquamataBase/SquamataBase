$(document).ready(function() {
    
    // should be same order as select box choices in models.py and forms.py
    var myplaceholder = [];
    myplaceholder['Journal article'] = 'Search for journal articles . . .'
    myplaceholder['Book'] = 'Search for books . . .'
    myplaceholder['Book chapter'] = 'Search for book chapters . . .'
     
    var v = $('#id_ref_type').val();
        
    $('#id_ref').attr('data-placeholder', myplaceholder[v]);
    
    $('#id_ref_type').on('change', function() {
        v = $('#id_ref_type').val();
        $('#id_ref').attr('data-placeholder', myplaceholder[v]);
        $('#id_ref').next().find('span.select2-selection__placeholder').text(myplaceholder[v]);
    });
    
    // placeholder defaults to initial value when selection is cleared unless
    // we add this hook to keep it as the currently selected reftype
    $(document).on('change', '#id_ref', function() {
        v = $('#id_ref_type').val();
        $('#id_ref').attr('data-placeholder', myplaceholder[v]);
        $('#id_ref').next().find('span.select2-selection__placeholder').text(myplaceholder[v]);
    });
    
});
