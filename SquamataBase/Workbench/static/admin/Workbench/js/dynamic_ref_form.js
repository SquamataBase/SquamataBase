$(document).ready(function() {

    $("#ref_set-0 > div").css("display", "none");

    var no_sel = $("select[name='ref_set-0-ref_type']").children("option:selected").text();
    var base_id = "#ref_set-0-grouptype-group";
    var authors = "#ref_set-0-contribution_set-group";

    $("select[name='ref_set-0-ref_type']").on("change", function() {
        
        var opt_sel = $(this).children("option:selected").text().replace(" ", "").toLowerCase();
        var id = base_id.replace("grouptype", opt_sel);

        $("#ref_set-0 > div").not(id).css("display", "none");

        if (opt_sel !== no_sel) {
            $(id).show();
            $(authors).show();
        }
    });
    
});