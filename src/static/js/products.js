/**
 * Created by sam on 15-12-12.
 */
$(document).ready(function () {
    navbar_active(1);
    $('[data-toggle="offcanvas"]').click(function () {
        $('.row-offcanvas').toggleClass('active')
    });
    
});