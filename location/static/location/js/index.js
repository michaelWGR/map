$(function () {
    $("#search").click(function () {
        var params = {
            address: $("#address").val(),
            city: $("#city").val(),
            key: $("#key").val()
        };
        $.get("search_location", params, function (data) {
            var full_address = $("#full_address");
            var res = data;
            var location1 = $("#location1"), location2 = $("#location2");
            full_address.empty();
            if (res.code === 0){
                for (i in res.full_address_list) {
                var address = $("<li></li>").text(res.full_address_list[i]);
                full_address.append(address);
                }
                if (location1.val() === "") {
                    location1.val(res.location);
                }
                else if (location2.val() === "") {
                    location2.val(res.location);
                }
                else {
                    location1.val(res.location);
                    location2.val("");
                }
            }
            else if (res.code === 1){
                full_address.append(res.error);
            }
        });
    });

    $("#search_transit").click(function () {
        var order_name = $("#order_name");
        var data = {
            location1: $("#location1").val(),
            location2: $("#location2").val(),
            key: $("#key").val(),
            order_name: order_name.val(),
            order_type: $("#order_type").val()
        };
        $.post("/search_transit_direction", data, function (data) {
            console.log(typeof(data));
            let res = data;
            let table = $("#transit_table");
            table.empty();
            if (res.code === 0) {
                let header = "<tr><th>id</th><th>站点名</th><th>" + order_name.find("option:selected").text() + "</th></tr>";
                table.append(header);
                for (t in res.transit_detail) {
                    let detail = "<tr><td>" + res.transit_detail[t].traffic_info_id + "</td><td><a href='detail/" + res.transit_detail[t].traffic_info_id + "'>" + res.transit_detail[t].traffic_info__name + "</a></td><td>" + res.transit_detail[t][$("#order_name").val()] + "</td></tr>";
                    console.log(res.transit_detail[t].traffic_info__name);
                    table.append(detail);
                }
            }
            else if (res.code === 1) {
                table.append(res.error);
            }
        });
    });
});