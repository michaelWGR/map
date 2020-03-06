$(function () {
    $("#search").click(function () {
        var params = {
            address: $("#address").val(),
            city: $("#city").val(),
            key: $("#key").val()
        };
        $.get("search_location", params, function (data) {
            var full_address = $("#full_address");
            var res = jQuery.parseJSON(data);
            full_address.empty();
            for (i in res.full_address_list) {
                var address = $("<li></li>").text(res.full_address_list[i]);
                full_address.append(address);
            }
            $("#location1").val(res.location);
            //$("#demo").text(data);
        });
        console.log(params);
    });
});