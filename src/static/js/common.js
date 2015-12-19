/**
 * Created by sam on 15-12-3.
 */
function refresh_code(img) {
    $(img).attr('src', '/verify_code?r=' + Math.random())
}
$(document).ready(function(){
    $(".shopcar-btn").click(function(){
        $("#shopcar_tip_modal").modal('show');
        if($.cookie('shopcar')){
            $.cookie('shopcar', $.cookie("shopcar") + ',' + $(this).attr("data-pid"));
        }
        else{
            $.cookie('shopcar', $(this).attr("data-pid"))
        }
    });
});

function navbar_active(index){
    $('#navbar ul li').removeClass('active');
    $('#navbar ul li').eq(index).attr('class', 'active');
}