$(document).ready(function(){
    $("#copy-code").on("click", function(){
        var game_code = $("#game-code").val();
        navigator.clipboard.writeText(game_code);
    });
});
