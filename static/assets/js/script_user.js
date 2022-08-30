$(document).ready(function(){
    // 회원가입
    var joinForm = function(e){
        e.preventDefault();

        let form = $(this);
        $.ajax({
            url: form.attr('action'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function(data){
                if(data.form_is_valid){
                    alert("회원가입 되었습니다.")
                    location.href = "login"
                }else{
                    $('#joinfield').html(data.html_form)
                }
            },
        })
    }

    // Binding
    $('#joinform').submit(joinForm);

})