$(document).ready(function(){

    var loadForm = function(e){
        e.preventDefault();
        
        var btn = $(this)
        $.ajax({
            url: btn.attr('data-url'),
            type: "get",
            dataType: 'json',
            beforeSend: function(){
                $('#modal-comment .modal-content').html("");
                $("#comment-create-form input[type=radio]").each(function(i, e){
                    $(this).attr("temp", $(this).attr("id")).attr("id", null)
                })
            },
            success: function(data){
                if(data.login_ok){
                    $('#modal-comment').modal('show')
                    $('#modal-comment .modal-content').html(data.html_form);
                    
                    // 닫기 버튼 활성화
                    $('.closemodal').click(function(){
                        $("#modal-comment").modal("hide");

                        $("#comment-create-form input[type=radio]").each(function(i, e){
                            $(this).attr("id", $(this).attr("temp")).attr("temp", null)
                        })
                    });
                    
                    setting();
                }
                else{
                    alert("로그인 후 이용해주세요.");
                    location.href = "/login?next="+data.next;
                }
            },
        })
    }


    var saveForm = function(e){
        e.preventDefault();
        var form = $(this);

        if(!$('[name=rating]').is(":checked")){
            alert("별점을 선택해주세요!");
            return false;
        }

        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.success){
                    // 댓글 불러오기
                    var object_pk = $("#object_pk").val()
                    $.ajax({
                        url: `/comment/list/${object_pk}/${1}/?orderby=-datetime`,
                        type: "get",
                        success: function(data){
                            if(data){
                                $('#comments_div').html(data.html_list)
                                setting();
                            }
                        }
                    })

                    // 입력창 초기화
                    $("#id_text").val("");
                    $("[name=rating]").prop("checked", false);
                    $("#image-preview-div").html("");
                }
            }
        })
    }
    
    var updateForm = function(e){
        e.preventDefault();

        var form = $(this);

        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    // 댓글불러오기
                    var object_pk = $("#object_pk").val()
                    $.ajax({
                        url: `/comment/list/${object_pk}/${1}/?orderby=-datetime`,
                        type: "get",
                        success: function(data){
                            if(data){
                                $('#comments_div').html(data.html_list)
                                setting();
                            }
                        }
                    })
                    // 창 닫기
                    $('.closemodal').click();

                }else{
                    alert("정확하게 입력해주세요.");
                }
            }
        })
    }
    
    var movePage = function(e){
        e.preventDefault();

        var object_pk = $("#object_pk").val()
        $.ajax({
            url: `/comment/list/${object_pk}/${$(this).attr('data-page')}/?orderby=` + $(this).attr("orderby"),
            type: "get",
            success: function(data){
                if(data){
                    $('#comments_div').html(data.html_list)
                    
                    setting();
                }
            }
        })
    }

    var deleteForm = function(){
        var delete_num = $(this).attr('delete-num')
        if(confirm("정말 댓글을 삭제하시겠습니까?")){
            $(`.comment-delete-form[delete-num=${delete_num}]`).on("submit", function(e){
                e.preventDefault();
                var form = $(this);
                $.ajax({
                    url: form.attr('action'),
                    data: form.serialize(),
                    type: form.attr('method'),
                    dataType: 'json',
                    success: function(data){
                        if(data.success){
                            alert("삭제되었습니다.")
                            // 댓글불러오기
                            var object_pk = $("#object_pk").val()
                            $.ajax({
                                url: `/comment/list/${object_pk}/${1}/`,
                                type: "get",
                                success: function(data){
                                    if(data){
                                        $('#comments_div').html(data.html_list)
                                        setting();
                                    }
                                }
                            })
                        }
                    }
                })
            })
            $(`.comment-delete-form[delete-num=${delete_num}]`).submit();
        }else{
            return;
        }
    }

    var order_select = function(){
        var object_pk = $("#object_pk").val()
        var order_by = $(this).val();
        $.ajax({
            url: `/comment/list/${object_pk}/${1}/?orderby=` + order_by,
            type: "get",
            success: function(data){
                if(data){
                    $('#comments_div').html(data.html_list)
                    
                    setting();
                }
            }
        })
    }
    
    function setting(){
        // 페이징
        $(".pagelink").off().click(movePage);
        
        // 생성
        $("#comment-create-form").off().submit(saveForm);
        // 수정
        $(".js-update-btn").off().click(loadForm);

        $("#comment-update-form").off().on('submit', updateForm);
        // 삭제
        $(".js-delete-btn").off().click(deleteForm);

        $("#comment-order-select").off().change(order_select);

        return;
    }
    setting();

    function readMultipleImage(input){
        const multipleContainer = document.getElementById("id_commentimage");
        if(input.files){
            if(input.files[0].size / 1024 / 1024 > 200){
                alert("이미지 용량 초과 (200MB)")
                return false;
            }
            const fileArr = Array.from(input.files)
            
            fileArr.forEach((file, index) => {
                const reader = new FileReader()
                reader.onload = e => {
                    $div = $("<div></div>").addClass("preview-wrapper col-lg-2 m-2 rounded-2 position-relative text-center p-0").attr("style", "height:90px;border:2px solid var(--color-primary);")
                    $deletebtn = $("<button type='button'>&times;</button>").addClass("position-absolute border-0").attr("style", "background:none;right:5px;color:red;").on("click" ,function(){
                        $(this).parent("div").remove();
                    })
                    $img = $("<img>").attr("src", e.target.result).attr("style", "object-fit:contain;height:100%;")
                    $hiddeninput = $(`<input type='hidden' name='commentimages'}>`).val(e.target.result)
                    $("#image-preview-div").append($div.append($deletebtn).append($img).append($hiddeninput))
                }
                reader.readAsDataURL(file)
            });
        }
    }
    document.getElementById("id_commentimage").addEventListener("change", e=>{
        readMultipleImage(e.target)
    });

})