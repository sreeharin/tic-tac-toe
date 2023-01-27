$(document).ready(function(){
    $("#game-code-form").toggle();
    $("#btns2").toggle();

    $("#join").on("click", function(){
        $("#game-code-form").slideDown(250)
            .queue(function(next){
                $("#btns").fadeOut();
                next();
            })
            .queue(function(){
                $("#btns2").fadeIn(1000);
                $(this).dequeue();
            });
    });

    $("#go-back").on("click", function(){
        $("#btns2").fadeOut()
            .queue(function(next){
                $("#btns").fadeIn(1000);
                next();
            }).queue(function(){
                $("#game-code-form").slideUp(250);
                $(this).dequeue();
            });

    });
});
