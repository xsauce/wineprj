/**
 * Created by sam on 15-11-21.
 */
$(document).ready(function () {
    $("#addr_level1").change(function () {
        var addr_l1 = $(this).val();
        var addr_level2_obj = $("#addr_level2");
        if (addr_l1 != '') {
            addr_level2_obj.empty();
            for (var i = 0; i < ship_cities[addr_l1].length; i++) {
                var addr_level2_item = ship_cities[addr_l1][i];
                addr_level2_obj.append("<option value='" + addr_level2_item + "'>" + addr_level2_item + "</option>");
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
