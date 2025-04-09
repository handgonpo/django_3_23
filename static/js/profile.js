$("#button_feed_list").click(function () {
    $("#feed_list").show();
    $("#like_feed_list, #bookmark_feed_list").hide();
    $(".profile-tab").removeClass("active");
    $(this).addClass("active");
});

$("#button_feed_like_list").click(function () {
    $("#like_feed_list").show();
    $("#feed_list, #bookmark_feed_list").hide();
    $(".profile-tab").removeClass("active");
    $(this).addClass("active");
});

$("#button_feed_bookmark_list").click(function () {
    $("#bookmark_feed_list").show();
    $("#feed_list, #like_feed_list").hide();
    $(".profile-tab").removeClass("active");
    $(this).addClass("active");
});

$("#button_profile_upload").click(function () {
    $("#input_fileupload").click();
});

// CSRF 토큰을 Axios에 자동으로 포함 403 에러 방지
axios.defaults.headers.common['X-CSRFToken'] = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');

function profile_upload() {
    const file = $("#input_fileupload")[0].files[0];
    const email = $("body").data("email");
    console.log("업로드 대상 이메일:", email);

    const fd = new FormData();
    fd.append("file", file);
    fd.append("email", email);

    axios
        .post("/user/profile/upload/", fd, { //127.0.0.1:8000/user/profile/upload/
            headers: {
                "Content-Type": "multipart/form-data",
            },
        })
        .then(() => {
            alert("프로필 이미지가 변경되었습니다.");
            location.reload();
        });
}

$(document).ready(function () {
    $(document).on("click", ".follow-toggle-btn", function (e) {
        e.preventDefault(); // 기본 submit 막기
        //console.log("클릭되니?");

        const button = $(this);  // 이 줄 먼저!
        const url = button.data("url");  // 여기서 url 변수 정의! (중요)
        const followee_id = button.data("followee-id");

        console.log("URL:", url);
        console.log("Followee ID:", followee_id);

        axios.post(url, {
            followee_id: followee_id
        }, {
            headers: {
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').content
            }
        })
        .then(response => {
            if (response.data.is_following) {
                button.text("언팔로우");
            } else {
                button.text("팔로우");
            }
            // 팔로워 수 업데이트
            if (response.data.follower_count !== undefined) {
                $(".follower-count").text(response.data.follower_count);
            }
        })
        .catch(error => {
            console.error("팔로우 실패", error);
            alert("팔로우 처리에 실패했습니다.");
        });
    });
});