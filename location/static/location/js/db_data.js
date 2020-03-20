$(function () {
    $("#delete_data_button").click(function () {
        let formData = {
            circle_id: $("#circle_id").val(),
            db_table_name: $("#db_table_name").val()
        };
        $.post("db_data/delete_data", formData, function (data) {

            if (data["code"] === 0) {
                let del_count = "已删除数据" + data["delete_count"] + "条";
                let msg = "已删除数据信息：";
                for (i in data["delete_msg"]) {
                    msg += i + ":" + data["delete_msg"][i] + "  ";
                }
                alert(del_count + "\n" + msg);
                window.location.reload();
            }
            else {
                alert(data["error"])
            }
        });
    });

    $("#db_tab li:eq(0) a").tab('show');
});