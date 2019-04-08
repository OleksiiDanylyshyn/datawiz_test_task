var table_length = 100;
var start_table = 0;
var end_table = start_table + table_length;

$(document).ready(function () {
    $.ajax({
        url: '/get_products/',
        type: 'get',
        dataType: 'json',
        success: function (data) {
            editProductIncreaseTable(data);
            let pag_buttons = '';
            pagination = data.products_name_list.length / table_length;
            for (i = 0; i < pagination; i++) {
                pag_buttons += `<button style="font-size: small" class="page-link" data-page="${i}">${i + 1}</button>`;
            }
            $('#products_decrease_pagination').append(pag_buttons);
            $('.page-link').each((i, elm) => {
                $(elm).on('click', (e) => {
                    start_table = table_length * $(elm).data('page');
                    end_table = start_table + table_length;
                    $.ajax({
                        url: '/get_products/',
                        type: 'get',
                        dataType: 'json',
                        success: function (data) {
                            editProductIncreaseTable(data);
                        }
                    })
                })
            })
        }
    });
});

function editProductIncreaseTable(data) {
    $('#products_decrease_table > tbody').empty();
    let rows = '';
    for (i = start_table; i < end_table; i++) {
        if (data.products_diff_turnover_list[i] < 0) {
            rows += `
             <tr>
             <td>${data.products_name_list[i]}</td>
             <td>${data.products_diff_qty_list[i]}</td>
             <td>${data.products_diff_turnover_list[i]}</td>
             </tr>`
        }
    }
    $('#products_decrease_table > tbody').append(rows);
}