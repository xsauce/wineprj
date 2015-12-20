$(function () {
    $('#photo-carousel').carousel({
        interval: 4000
    });
    $('[id^=photo-selector-]').click(function () {
        var id_selector = $(this).attr("id");
        var id = id_selector.substr(id_selector.length - 1);
        id = parseInt(id);
        $('#photo-carousel').carousel(id);
        $('[id^=photo-selector-]').removeClass('selected');
        $(this).addClass('selected');
    });
    $('#photo-carousel').on('slid', function (e) {
        var id = $('.item.active').data('slide-number');
        id = parseInt(id);
        $('[id^=photo-selector-]').removeClass('selected');
        $('[id=photo-selector-' + id + ']').addClass('selected');
    });
});