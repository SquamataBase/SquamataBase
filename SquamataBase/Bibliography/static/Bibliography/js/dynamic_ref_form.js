$(document).ready(function() {

    $(".js-inline-admin-formset").css("display", "none");

    var no_sel = $("#id_ref_type").children("option:selected").text();
    var base_id = "#grouptype-group";
    var authors = "#contribution_set-group";

    $("#id_ref_type").on("change", function() {
        
        var opt_sel = $(this).children("option:selected").text().replace(" ", "").toLowerCase();
        var id = base_id.replace("grouptype", opt_sel);

        $(".js-inline-admin-formset").not(id).css("display", "none");

        if (opt_sel !== no_sel) {
            $(id).show();
            $(id).find("h2, h3").hide();
            $(authors).show();
        }
    });
    
});
