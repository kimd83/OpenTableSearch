$(document).ready(function () {
    $("#button1").click(function () {
        $("#list1 > option:selected").each(function () {
            $(this).remove().appendTo("#list2");
            rearrangeList("#list2");
        });
    });

    $("#button2").click(function () {
        $("#list2 > option:selected").each(function () {
            $(this).remove().appendTo("#list1");
            rearrangeList("#list1");
        });
    });

function byValue(a, b) {
    return a.value > b.value ? 1 : -1;
};

function rearrangeList(list) {
    $(list).find("option").sort(byValue).appendTo(list);
};
    
});