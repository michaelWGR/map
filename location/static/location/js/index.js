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

    var searchTransitDirection = function (postData) {
        let order_name = $("#order_name");
        $.post("/search_transit_direction", postData, function (data) {
            let searchError = $("#search-error");
            let tableHeader = $("#table_header");
            let tableBody = $("#table_body");
            searchError.text("");
            tableHeader.empty();
            tableBody.empty();
            console.log(data.code);
            if (data.code === 0) {
                let header = "<tr><th>id</th><th>站点名</th><th>" + order_name.find("option:selected").text() + "</th></tr>";
                tableHeader.append(header);
                console.log(header);
                for (t in data.transit_detail) {
                    let detail = "<tr><td>" + data.transit_detail[t].traffic_info_id + "</td><td><a href='detail/" + data.transit_detail[t].traffic_info_id + "'>" + data.transit_detail[t].traffic_info__name + "</a></td><td>" + data.transit_detail[t][order_name.val()] + "</td></tr>";
                    console.log(data.transit_detail[t].traffic_info__name);
                    tableBody.append(detail);
                }
                // 分页导航栏
                $("#total_page").text(data["num_pages"]);
                let previous = $("#previous"), previous2 = $("#previous2"), previous1 = $("#previous1");
                let current = $("#current");
                let next = $("#next"), next1 = $("#next1"), next2 = $("#next2");
                let currentPageNum = Number(postData["page_num"]);
                current.removeClass("d-none");
                current.children("a").text(currentPageNum);
                if (data["has_previous"] === true) {
                    console.log("has previous");
                    previous.removeClass("disabled");
                    previous1.removeClass("d-none");
                    previous1.children("a").text(currentPageNum-1);
                    previous2.addClass("d-none");
                    if (data["num_pages"] === currentPageNum && currentPageNum > 2) {
                        previous2.removeClass("d-none");
                        previous2.children("a").text(currentPageNum-2);
                    }
                }
                else {
                    previous.addClass("disabled")
                    previous1.addClass("d-none");
                    previous2.addClass("d-none");
                }

                if (data["has_next"] === true) {
                    console.log("has next");
                    console.log("currentPageNum is "+currentPageNum);
                    next.removeClass("disabled");
                    next1.removeClass("d-none");
                    next1.children("a").text(currentPageNum+1);
                    next2.addClass("d-none");
                    if (currentPageNum === 1 && data["num_pages"] > 2) {
                        next2.removeClass("d-none");
                        next2.children("a").text(currentPageNum+2);
                    }
                }
                else {
                    next.addClass("disabled");
                    next1.addClass("d-none");
                    next2.addClass("d-none");
                }
            }
            else if (data.code === 1) {
                searchError.text(data.error);
            }
        });
    };
    $("#search_transit").click(function () {
        var postData = {
            location1: $("#location1").val(),
            location2: $("#location2").val(),
            key: $("#key").val(),
            order_name: $("#order_name").val(),
            order_type: $("#order_type").val(),
            page_num: "1",
            page_size: ""
        };
        searchTransitDirection(postData);
    });
    $("li.page-item").click(function () {
        var postData = {
            location1: $("#location1").val(),
            location2: $("#location2").val(),
            key: $("#key").val(),
            order_name: $("#order_name").val(),
            order_type: $("#order_type").val(),
            page_size: ""
        };
        let pageItemId = $(this).attr("id");
        let currentText = Number($(this).siblings("#current").text());
        if (pageItemId === "current" || $(this).hasClass("disabled")) {
            return
        }
        else if (pageItemId === "previous") {
            postData["page_num"] = currentText-1;
        }
        else if (pageItemId === "next") {
            console.log(currentText);
            postData["page_num"] = currentText+1;
        }
        else {
            postData["page_num"] = $(this).text();
        }
        searchTransitDirection(postData);
    });

    var deleteIcon = $("a[name='text-delete']");
    deleteIcon.click(function () {
        console.log("click delete button");
        $(this).siblings("input").val("").focus();
    });
    deleteIcon.hover(
        function () {
        $(this).css("background-color", "#cccccc");
        },
        function () {
            $(this).css("background-color", "#ffffff");
        }
    );
});