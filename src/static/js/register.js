/**
 * Created by sam on 15-12-3.
 */
$(document).ready(function(){
    var rp_group = $("#repeat_password_group");
    var rp_label = rp_group.find('label');
    var rp_label_text = rp_label.text();
    $("#repeat_password").keyup(function(){
        var p1 = $("#password").val();
        var p2 = $(this).val();
        if(p1 != p2){
            rp_group.addClass('has-error');
            rp_label.html('密码不一致')
        }
        else{
            rp_group.removeClass('has-error');
            rp_label.html(rp_label_text);
        }

    });
});
