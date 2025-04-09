$(function () {
    let files = null;

    // 모달 열기
    $("#nav_bar_add_box").click(function () {
        $("#first_modal").addClass("show");
        $("body").css("overflow", "hidden");
    });

    // 모달 닫기
    $(document).on("click", ".modal_close", function () {
        $(this).closest(".modal_overlay").removeClass("show");
        $("body").css("overflow", "auto");
    });

    // 드래그 이벤트
    $(".img_upload_space")
        .on("dragover", function (e) {
            e.preventDefault();
        })
        .on("drop", function (e) {
            e.preventDefault();
            e.dataTransfer = e.originalEvent.dataTransfer;
            files = e.dataTransfer.files;

            if (files.length !== 1 || !files[0].type.match(/image.*/)) {
                alert("이미지 하나만 업로드해주세요.");
                return;
            }

            $("#first_modal").removeClass("show");
            $("#second_modal").addClass("show");

            $(".modal_image_area").css({
                "background-image": `url(${URL.createObjectURL(files[0])})`,
            });
        });

    // 공유하기
    $("#feed_create_button").click(function () {
        if (!files || files.length === 0) {
            alert("이미지를 먼저 업로드해주세요.");
            return;
        }

        const file = files[0];
        const content = $("#input_feed_content").val();
        const fd = new FormData();
        fd.append("file", file);
        fd.append("content", content);

        axios.post("/port/upload", fd, { //127.0.0.1:8000/port/upload/
            headers: { "Content-Type": "multipart/form-data" },
        }).then(() => {
            alert("피드가 공유되었습니다.");
            location.reload();
        });
    });
});
