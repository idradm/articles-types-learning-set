$(function(){
    $('.save-btn').click(function() {
        console.info(this);
        console.info($(this).val());
        //ajax query
    });

    $('.watson-next').click(function() {
        $.ajax({
            url: "/next/"
        }).done(function(data){
            window.location.href = window.location.origin + data.path;
        });
    });

    $('.watson-sessions-dropdown').click(function() {
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

    function changeSession(e) {
        window.location.href = window.location.origin + '/watson/' + e.data;
    }
});
