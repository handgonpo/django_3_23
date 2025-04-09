document.addEventListener("DOMContentLoaded", () => {
    // CSRF 토큰 가져오기
    function getCSRFToken() {
        const tokenMeta = document.querySelector('meta[name="csrf-token"]');
        return tokenMeta ? tokenMeta.getAttribute("content") : "";
    }

    // Ajax 요청 시 CSRF 토큰 자동 포함
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    });

    // 가입 버튼 클릭 이벤트 바인딩
    document.getElementById("join_button").addEventListener("click", () => {
        const email = document.getElementById("input_email").value.trim();
        const name = document.getElementById("input_name").value.trim();
        const nickname = document.getElementById("input_nickname").value.trim();
        const password = document.getElementById("input_password").value.trim();

        // 필수 입력 확인
        if (!email || !name || !nickname || !password) {
            alert("모든 항목을 입력해주세요.");
            return;
        }

        // Ajax 회원가입 요청
        $.ajax({
            url: "/user/join/",
            method: "POST",
            data: {
                email: email,
                name: name,
                nickname: nickname,
                password: password
            },
            success: function () {
                alert("회원가입 성공! 로그인 페이지로 이동합니다.");
                window.location.href = "/user/login/";
            },
            error: function (xhr) {
                if (xhr.status === 400) {
                    alert("이미 등록된 이메일입니다. 다른 이메일을 사용해주세요.");
                } else if (xhr.status === 403) {
                    alert("CSRF 오류 또는 접근 권한이 없습니다.");
                } else {
                    alert("회원가입 실패! 예상치 못한 오류입니다.");
                    console.error("회원가입 에러", xhr);
                }
            }
        });
    });
});
