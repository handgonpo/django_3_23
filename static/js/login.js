document.addEventListener("DOMContentLoaded", () => {
    // CSRF 토큰 가져오기
    function getCSRFToken() {
        const tokenMeta = document.querySelector('meta[name="csrf-token"]');
        return tokenMeta ? tokenMeta.getAttribute("content") : "";
    }

    // Ajax 요청에 CSRF 토큰 포함
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    });

    document.getElementById("login_button").addEventListener("click", () => {
        const email = document.getElementById("input_email").value.trim();
        const password = document.getElementById("input_password").value.trim();

        // 기본 유효성 검사
        if (!email || !password) {
            alert("이메일과 비밀번호를 모두 입력해주세요.");
            return;
        }

        $.ajax({
            url: "/user/login/",
            method: "POST",
            data: {
                email: email,
                password: password
            },
            success: function (response) {
                alert("로그인 성공!");
                window.location.href = "/";  // 세션이 제대로 설정되어야 동작함
            },
            error: function (xhr) {
                if (xhr.status === 400) {
                    alert("로그인 실패! 이메일 또는 비밀번호를 확인하세요.");
                } else if (xhr.status === 403) {
                    alert("CSRF 토큰 오류 또는 권한 문제입니다.");
                } else {
                    alert("알 수 없는 오류가 발생했습니다.");
                }
            }
        });
    });
});
