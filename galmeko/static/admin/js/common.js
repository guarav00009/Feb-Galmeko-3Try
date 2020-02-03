var loc = window.location;
var base_url = window.location.href.split("?")[0];
var server_url = "" + loc.protocol + "//" + loc.host + '/';

function display_message(type, msg) {
    return $('#disp-msg').html("<div style='margin-bottom:0px;' class='alert alert-" + type + " alert-dismissible hide' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button><strong>" + type.charAt(0).toUpperCase() + type.slice(1) + "! </strong>" + msg + "</div>");
}

// Display Vehicle listing in vendor view

$(document).ready(function ($) {
    $(document).on('click', '.vehicle_listing', function () {
        $.noConflict();
        var formData = {
            'vendor_id': $('#vendor_id').val(),
            'csrfmiddlewaretoken': $('#csrf_token').val()
        }
        $('#vehicle').DataTable({
            "processing": true,
            responsive: true,
            "bRetrieve": true,
            "scrollX": false,
            "paging": true,
            "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
            "pageLength": 7,
            "ajax": {
                method: "POST",
                headers: { 'X-CSRFToken': '{{ csrf_token }}' },
                data: formData,
                "processing": true,
                "url": server_url + 'admin/get-vehicle/',
                "dataSrc": "",
                dataType: "JSON",
                cache: false
            },

            "columns": [
                { "data": 'vehicle_no' },
                { "data": 'mileage' },
                { "data": 'chassis_no' },
                { "data": 'status', className: "field-status", },
                {
                    "mRender": function (data, type, row) {
                        if (row.status_id != 3) {
                            return "<a href='javascript:void(0);' class='delete-vehicle' data-vehicle-id=" + row.id + "><i class='fa fa-trash' aria-hidden='true'></i></a>"
                        } else {
                            return "<a href='javascript:void(0);'><i class='fa fa-trash' aria-hidden='true' style='color:#353535'; ></i></a>"
                        }
                    }
                }

            ]
        });
    });
});

$(document).on('click', '.delete-vehicle', function () {
    if (confirm("Are you sure?")) {
        vehicle_id = $(this).attr("data-vehicle-id");
        var formData = {
            'id': vehicle_id,
            'csrfmiddlewaretoken': $('#csrf_token').val()
        }
        console.log(formData)
        $.ajax({
            method: "POST",
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            url: server_url + 'admin/delete_vehicle/',
            data: formData,
            dataType: "JSON",
            cache: false,
            success: data => {
                $('#disp-msg').css('display', 'block');
                if (data.status == true) {
                    $(this).closest('tr').find('.field-status').html('Deleted');
                    $(this).html("<a href='javascript:void(0);'><i class='fa fa-trash' aria-hidden='true' style='color:#353535'; ></i></a>");
                    display_message('success', data.msg);
                } else {
                    display_message('warning', data.msg);
                }
                setTimeout(function () {
                    $("#disp-msg").hide('blind', {}, 500)
                }, 3000);
            }
        });
    }
    return false;
})

//  Display Driver Listing on vendor

$(document).ready(function ($) {
    $(document).on('click', '.driver_listing', function () {
        $.noConflict();
        var formData = {
            'vendor_id': $('#vendor').val(),
            'csrfmiddlewaretoken': $('#csrf_token').val()
        }
        $('#driver').DataTable({
            "processing": true,
            responsive: true,
            "bRetrieve": true,
            "scrollX": false,
            "paging": true,
            "lengthMenu": [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
            "pageLength": 7,
            "ajax": {
                method: "POST",
                headers: { 'X-CSRFToken': '{{ csrf_token }}' },
                data: formData,
                "processing": true,
                "url": server_url + 'admin/get-driver/',
                "dataSrc": "",
                dataType: "JSON",
                cache: false
            },

            "columns": [
                { "data": 'first_name' },
                { "data": 'last_name' },
                { "data": 'email' },
                { "data": 'phone' },
                { "data": 'address' },
                { "data": 'status', className: "field-status", },
                {
                    "mRender": function (data, type, row) {
                        if (row.status_id != 3) {
                            return "<a href='javascript:void(0);' class='delete-vehicle' data-vehicle-id=" + row.id + "><i class='fa fa-trash' aria-hidden='true'></i></a>"
                        } else {
                            return "<a href='javascript:void(0);'><i class='fa fa-trash' aria-hidden='true' style='color:#353535'; ></i></a>"
                        }
                    }
                }

            ]
        });
    });
})
