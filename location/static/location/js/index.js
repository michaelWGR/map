$(function () {
    $("#search").click(function () {
        var params = {
            address: $("#address").val(),
            city: $("#city").val(),
            key: $("#key").val()
        };
        $.get("search_location", params, function (data) {
            var full_address = $("#full_address");
            var location1 = $("#location1"), location2 = $("#location2");
            full_address.empty();
            if (data.code === 0){
                for (i in data.full_address_list) {
                var address = $("<li></li>").text(data.full_address_list[i]);
                full_address.append(address);
                }
                if (location1.val() === "") {
                    location1.val(data.location);
                }
                else if (location2.val() === "") {
                    location2.val(data.location);
                }
                else {
                    location1.val(data.location);
                    location2.val("");
                }
            }
            else if (data.code === 1){
                full_address.append(data.error);
            }
        });
    });

    $("#search_transit").click(function () {
        let order_name = $("#order_name");
        var data = {
            location1: $("#location1").val(),
            location2: $("#location2").val(),
            key: $("#key").val(),
            order_name: order_name.val(),
            order_type: $("#order_type").val()
        };
        $.post("/search_transit_direction", data, function (data) {
            let table = $("#transit_table");
            let tableHeader = $("#table_header");
            let tableBody = $("#table_body");
            tableHeader.empty();
            tableBody.empty();
            console.log(data.code);
            if (data.code === 0) {
                let header = "<tr><th>id</th><th>站点名</th><th>" + order_name.find("option:selected").text() + "</th></tr>";
                tableHeader.append(header);
                console.log(header);
                for (t in data.transit_detail) {
                    let detail = "<tr><td>" + data.transit_detail[t].traffic_info_id + "</td><td><a href='detail/" + data.transit_detail[t].traffic_info_id + "'>" + data.transit_detail[t].traffic_info__name + "</a></td><td>" + data.transit_detail[t][$("#order_name").val()] + "</td></tr>";
                    console.log(data.transit_detail[t].traffic_info__name);
                    tableBody.append(detail);
                }
            }
            else if (data.code === 1) {
                table.append(data.error);
            }
        });
    });
});