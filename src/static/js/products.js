/**
 * Created by sam on 15-12-12.
 */
navbar_active(1);
var gs = get_query_value('grape_sort');
$("#filter_list").children().each(function(){
    if($(this).html() == gs){
        $(this).addClass('active');
    }
});
$(document).ready(function () {

    $('[data-toggle="offcanvas"]').click(function () {
        $('.row-offcanvas').toggleClass('active')
    });
    
});