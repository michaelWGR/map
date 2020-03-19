$(function () {
    $("#delete_data").click(function () {
        let formData = {
            circle_id: $("#circle_id").val(),
            db_table_name: $("#db_table_name").val()
        };
        $.post("db_data/delete_data", formData, function (data) {
            if (data["code"] === 0) {
                $("#delete_count").text("已删除数据" + data["delete_count"] + "条");
                var msg = "";
                for (i in data["delete_msg"]) {
                    msg += i + ":" + data["delete_msg"][i] + "\t";
                }
                $("#delete_msg").text("已删除数据信息：" + msg);
            }
            else {
                $("#delete_msg").text(data["error"]);
            }

        })
    });
});