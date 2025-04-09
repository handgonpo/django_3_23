// 북마크 기능
$(document).on("click", ".bookmark", function () {
    const feed_id = $(this).data("feed_id");
    const bookmark_text = $.trim($(this).text());
    $(this).text(bookmark_text === "bookmark" ? "bookmark_border" : "bookmark");

    axios.post("/interaction/bookmark", { //127.0.1.8000/interaction/bookmark/
        feed_id,
        bookmark_text,
    });
});

// 좋아요 기능
$(document).on("click", ".favorite", function () {
    const feed_id = $(this).data("feed_id");
    const favorite_text = $.trim($(this).text());
    const new_text = favorite_text === "favorite" ? "favorite_border" : "favorite";

    $(this).text(new_text);  // 아이콘 바꾸기

    axios.post("/interaction/like", {
        feed_id: feed_id,
        favorite_text: favorite_text,
    }).then(response => {
        const data = response.data;
        // 좋아요 UI 반영
        $(`#like_info_${feed_id}`).html(`${data.first_liker} <b>외 ${data.like_count}명</b>이 좋아합니다.`);
    }).catch(error => {
        console.error("좋아요 실패", error);
        alert("좋아요 처리에 실패했습니다.");
    });
});

// 댓글 작성
$(document).on("click", ".upload_reply", function () {
    const feed_id = $(this).data("feed_id");
    const reply_content = $(`#reply_${feed_id}`).val();

    if (!reply_content) {
        alert("댓글을 입력하세요");
        return;
    }

    axios
        .post("/interaction/reply", { //127.0.1.8000/interaction/reply/
            feed_id,
            reply_content,
        })
        .then(() => {
            $(`#reply_list_${feed_id}`).append(
                `<div class='reply-item'><b>나</b> ${reply_content}</div>`
            );
            $(`#reply_${feed_id}`).val("");
        });
});