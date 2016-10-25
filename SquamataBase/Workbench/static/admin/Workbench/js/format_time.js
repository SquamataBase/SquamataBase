$(document).ready(function() {
    
    function match_time(timeObj, qualObj) {
        var am_or_pm = $(qualObj).val();
        var hour = $(timeObj).val();
        if (hour !== "") {
            if (parseInt(hour) <= 12 && am_or_pm === "AM") {
                if (parseInt(hour) < 10) {
                    if (parseInt(hour) == 0) {
                        $(timeObj).val("00");
                    }
                    else if ($(timeObj).val().startsWith("0") == false) {
                        $(timeObj).val("0" + hour);
                    }
                }
                else if (parseInt(hour) == 12) {
                    $(timeObj).val("00");
                }
            }
            if (parseInt(hour) < 12 && am_or_pm === "PM") {
                $(timeObj).val(12 + parseInt(hour));
            }
            if (parseInt(hour) >= 12 && am_or_pm === "AM") {
                if (parseInt(hour) == 12) {
                    $(timeObj).val("00");
                } else if (parseInt(hour) == 24) {
                    $(timeObj).val("00");
                } else {
                    $(timeObj).val("0" + (parseInt(hour) - 12));
                }
            }   
        }
    }
    
    $("#id_foodrecord_set-0-start_time_2").on("change", function() {
        match_time("#id_foodrecord_set-0-start_time_0", this);
    });
    
    $("#id_foodrecord_set-0-end_time_2").on("change", function() {
        match_time("#id_foodrecord_set-0-end_time_0", this);
    });
    
    $("*").on("focus", function() {
        match_time("#id_foodrecord_set-0-start_time_0", "#id_foodrecord_set-0-start_time_2");
    });
    
    $("*").on("focus", function() {
        match_time("#id_foodrecord_set-0-end_time_0", "#id_foodrecord_set-0-end_time_2");
    });

});
