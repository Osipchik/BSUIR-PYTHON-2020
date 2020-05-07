$('#exampleModal').modal({
  show: true
})

function like()
{
    let like = $(this);
    let type = like.data('type');
    let pk = like.data('id');
    let action = like.data('action');
    let dislike = like.next();

    $.ajax({
        url : "/api/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            like.find("[data-count='like']").text(json.like_count);
            dislike.find("[data-count='dislike']").text(json.dislike_count);
        }
    });

    return false;
}

function dislike()
{
    let dislike = $(this);
    let type = dislike.data('type');
    let pk = dislike.data('id');
    let action = dislike.data('action');
    let like = dislike.prev();

    $.ajax({
        url : "/api/" + type +"/" + pk + "/" + action + "/",
        type : 'POST',
        data : { 'obj' : pk },

        success : function (json) {
            dislike.find("[data-count='dislike']").text(json.dislike_count);
            like.find("[data-count='like']").text(json.like_count);
        }
    });

    return false;
}

// Подключение обработчиков
$(function() {
    $('[data-action="like"]').click(like);
    $('[data-action="dislike"]').click(dislike);
});