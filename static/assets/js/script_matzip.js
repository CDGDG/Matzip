$(document).ready(function(){
    $("#matzip-list-btn").click(function(e){
        e.preventDefault();
        let $btn = $(this)
        // 현재 위치 받아오기
        if(lon){
            navigator.geolocation.getCurrentPosition(function(position){
                // 주소 얻기
                $.ajax({
                    url: `https://dapi.kakao.com/v2/local/geo/coord2address?x=${lon}&y=${lat}`,
                    type: "get",
                    headers: {"Authorization": "KakaoAK 7988f17d47883052ebc22853ffe510c4"},
                    success: function(result, status){
                        if(result.documents && status == "success"){
                            addr = result.documents[0].road_address?result.documents[0].road_address.address_name:result.documents[0].address.address_name.replace("서울", "서울특별시")
                            location.href = $btn.attr("href") + addr.split(" ").slice(0, 2).join(" ")
                        }
                    },
                })
            },function(){location.href = $(this).attr("href")})
        }
        else{
            location.href = $btn.attr("href");
        }
    })

    var loadForm = function(){
        var btn = $(this);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
                $('#modal-matzip .modal-content').html("");
            },
            success: function(data){
                if(data.login_ok){
                    $('#modal-matzip').modal('show')
                    $('#modal-matzip .modal-content').html(data.html_form);
    
                    // 닫기 버튼 활성화
                    $('.closemodal').click(function(){
                        $("#modal-matzip").modal("hide"); 
                    });
                }
                else{
                    alert("로그인 후 이용해주세요.");
                    location.href = "/login?next="+data.next;
                }
            },
        });
    };

    var saveForm = function(e){
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid) {
                    // $('#book-table tbody').html(data.html_book_list)
                    alert("저장되었습니다.")
                    $('#modal-matzip').modal('hide')
                    if(data.next){
                        location.href = data.next;
                    }
                }else{
                    console.log(data)
                    $('#modal-matzip .modal-content').html(data.html_form)

                    // 닫기 버튼 활성화
                    $('.closemodal').click(function(){
                        $("#modal-matzip").modal("hide"); 
                    });
                }
            },
            error: function(data, status){
                console.log(data, status);
            }
        })

        return false;
    }

    // Binding
    // 생성
    $('#matzip-create-btn').click(loadForm)
    $('#modal-matzip').on('submit', '.js-matzip-create-form', saveForm);
    // 수정
    $('#matzip-update-btn').click(loadForm)
    $('#modal-matzip').on('submit', '.js-matzip-update-form', saveForm);
    // 삭제
    $('#matzip-delete-btn').click(function(){
        if(confirm("삭제하시겠습니까??")){
            $('#matzip-delete-form').submit();
        }
    })
    

    // 정렬 select
    $("#matzip-order-select").change(function(){
        order_by = $(this).val();
        location.href = $(this).attr("data-url") + order_by;
    })

    // type radio
    $("[name=matzip-type]").change(function(){
        type = $(this).val();
        location.href = $(this).attr("data-url") + type;
    })
    $(`label[for=${$("[name=matzip-type]:checked").attr("id")}]`).css({"background-color": "var(--color-primary)", color:"white"})
})