/**
 * Created by jonathan on 2015-12-13.
 */
function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var form_id = $('#id_' + type + '-TOTAL_FORMS');
    var total = form_id.val();
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    newElement.find('label').each(function() {
        var newFor = $(this).attr('for').replace('-' + (total-1) + '-','-' + total + '-');
        $(this).attr('for', newFor);
    });
    total++;
    form_id.val(total);
    $(selector).after(newElement);
}
