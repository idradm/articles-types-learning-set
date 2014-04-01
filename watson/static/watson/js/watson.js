$(function(){
    $('.watson-hover').hover(toggleHide, toggleHide);

    $('.watson-btn').click(function() {
        var that = this;
        var data = {
            "csrfmiddlewaretoken": $('.token input').val(),
            "type": $(this).val()
        };
        $.ajax({
            url: window.location.href,
            type: "POST",
            data: data
        }).success(function(e) {
            $('.watson-btn-group .watson-btn').removeClass('btn-success');
            $(that).addClass('btn-success');
        });
    });

    $('.watson-next').click(function() {
        $.ajax({
            url: "/next/"
        }).done(function(data){
            window.location.href = window.location.origin + data.path;
        });
    });

    $('.watson-sessions').click(function() {
        if(!$('.dropdown ul').children().length) {
            $.ajax({
                url: "/sessions/"
            }).done(function(data){
                var $ul = $(document.createElement('ul'));
                $ul.addClass('dropdown-menu');
                for(item in data){
                    var $li = $(document.createElement('li'));
                    var $a = $(document.createElement('a'));
                    $a.click(data[item].name, changeSession);
                    $a.html(data[item].name);
                    $li.html($a);
                    $ul.append($li);
                }
                $('.dropdown').append($ul);
            });
        }
    });

    function toggleHide(el) {
        $(el.currentTarget).children('span').toggleClass('hide');
    }

    function changeSession(e) {
        window.location.href = window.location.origin + '/watson/' + e.data;
    }
});
