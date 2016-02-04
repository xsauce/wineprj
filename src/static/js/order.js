/**
 * Created by sam on 15-11-21.
 */
$(document).ready(function () {
    $("#addr_level1").change(function () {
        var addr_l1 = $(this).val();
        var addr_level2_obj = $("#addr_level2");
        if (addr_l1 != '') {
            addr_level2_obj.empty();
            var addr_level1 = {};
            for(var i = 0; i < ship_cities.length; i++) {
                if (ship_cities[i]['value'] == addr_l1) {
                    addr_level1 = ship_cities[i]
                }
            }
            if (addr_level1 != {}){
                for (var j = 0; j < addr_level1['children'].length; j++) {
                    var addr_level2_item = addr_level1['children'][j];
                    addr_level2_obj.append("<option value='" + addr_level2_item['value'] + "'>" + addr_level2_item['display'] + "</option>");
                }
            }
            addr_level2_obj.removeAttr('disabled');
        }
        else {
            addr_level2_obj.attr('disabled', 'disabled');
            addr_level2_obj.empty()
        }
    });
    $("#need_receipt").click(function () {
        var is_checked = $(this).is(':checked');
        if (is_checked) {
            $("#receipt_detail1").show();
            $("#receipt_detail2").show();
        }
        else {
            $("#receipt_detail1").hide();
            $("#receipt_detail2").hide();
        }
    });
});
