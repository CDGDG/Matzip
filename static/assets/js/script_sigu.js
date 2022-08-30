$(document).ready(function(){
    $("#region-select-btn").click(function(e){
        e.preventDefault();
        $("#modal-position").modal("show");
    })

    $("#id_si").change(function(){
        si = $(this).val()
        $(`#id_gu option.op`).addClass("d-none")
        $(`#id_gu option.op[si=${si}]`).removeClass("d-none")
    })

    $("#region-change-btn").click(function(e){
        region = $("#id_si").val() + " " + $("#id_gu").val()
        location.href = $(this).attr("data-url") + region
    })
})