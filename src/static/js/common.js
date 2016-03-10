/**
 * Created by sam on 15-12-3.
 */
function refresh_code(img) {
    $(img).attr('src', '/verify_code?r=' + Math.random())
}
$(document).ready(function(){
    $(".shopcar-btn").click(function(){
        $("#shopcar_tip_modal").modal('show');
        var cookie_str = $(this).attr("data-pid") + ':1';
        if($.cookie('shopcar')){
            $.cookie('shopcar', $.cookie("shopcar") + ',' + cookie_str);
        }
        else{
            $.cookie('shopcar', cookie_str)
        }
    });
});

function navbar_active(index){
    $('#navbar ul li').removeClass('active');
    $('#navbar ul li').eq(index).attr('class', 'active');
}


function get_query_value(name)
{
     var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
     var r = window.location.search.substr(1).match(reg);
     if(r!=null)return  unescape(r[2]); return null;
}