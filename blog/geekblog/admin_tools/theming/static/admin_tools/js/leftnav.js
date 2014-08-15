jQuery(document).ready(function(){

    /* action buttons */
    var action_div = $('.actions');
    if(action_div.length == 1){
       action_div.prepend('<input type="checkbox" id="selectall" class="selectall" onclick="$(\'#action-toggle\').click()"/>全选');

       var action_btn = $('.actions .button');
       var action_select = $('.actions select[name="action"]').get(0);
       if (action_select.children.length == 2) {
           action_select.selectedIndex = 1;
           var action_text = action_select.children[1].text;
           action_btn.text(action_text);
           if (action_select.children[1].value == 'delete_selected_items') {
               action_btn.attr({'id': 'action_submit_btn', 'title': action_text});
           } else if (action_select.children[1].value == 'sync_selected_items') {
               action_btn.attr({'id': 'action_submit_btn', 'title': action_text, 'class': 'sync_btn'});
           }
       } else {
           var action_text1 = action_select.children[1].text;
           var action_text2 = action_select.children[2].text;
           action_btn.text(action_text1);
           action_btn.attr({'id': 'action_submit_btn', 'title': action_text1});
           action_btn.after('<button class="sync_btn" title="' + action_text2 + '">' + action_text2 + '</button>');
           action_select.value = 'delete_selected_items';
       }
    }

    $('.sync_btn').click(function() {
        $('.actions select[name="action"]').get(0).value = 'sync_selected_items';
        $('#action_submit_btn').click();
    });

    changelist_save_btn = $('#list_save_btn');
    if(changelist_save_btn.length == 1){
        $('.top_toolbar').prepend('<input type="submit" name="_save" class="default" value="保存" onclick="$(\'#list_save_btn\').click();" />')
    } else {
        $('.object-tools').addClass('toR')
    }

    /* set changelist filter h3 innerText */
    var filters = $('#changelist-filter h3');
    for (var i = 0; i < filters.length; i++) {
        var f = $(filters[i]);
        var selected_text = f.next().find('li.selected').text().replace(/\s/g, "");
        if (selected_text != '全部') {
            f.text(selected_text);
        }
    }

    var display_hrefs = $('.vForeignKeyRawIdAdminField').next().next();
    for (var i=0; i<display_hrefs.length; i++) {
        var href_value = $(display_hrefs[i]).attr('href');
        if (href_value != undefined && href_value.indexOf('rtn_url') == -1) {
            href_value += '?rtn_url=' + $('input[name="url"]').val().replace(/\/(\w+)\/$/, '/');
            $(display_hrefs[i]).attr('href', href_value);
        }
    }

    $('.vForeignKeyRawIdAdminField').change(function() {
        var value = $(this).val();
        if (value == "" | value == undefined) {
            $(this).next().next().find('strong').text('');
        } else {
            var display_href = $(this).next().next();
            $.getJSON('../../../get_related_lookup_info?cls_name=' + display_href.attr('cls_name') + '&v=' + value, function(data) {
                if (data == "" || data == undefined) {
                    alert("请输入正确的ID.");
                } else {
                    display_href.find('strong').text(data);
                    var href_value = display_href.attr('href').replace(/\/(\d+|obj_id_placeholder)\//, '/' + value + '/');
                    display_href.attr('href', href_value);
                }
            })
        }
    });

    $(".vIntegerField").keydown(function(event) {
        // Allow: backspace, delete, tab, escape, and enter
        if ( event.keyCode == 46 || event.keyCode == 8 || event.keyCode == 9 || event.keyCode == 27 || event.keyCode == 13 ||
             // Allow: Ctrl+A
            (event.keyCode == 65 && event.ctrlKey === true) ||
             // Allow: home, end, left, right
            (event.keyCode >= 35 && event.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        } else {
            // Ensure that it is a number and stop the keypress
            if (event.shiftKey || (event.keyCode < 48 || event.keyCode > 57) && (event.keyCode < 96 || event.keyCode > 105 )) {
                event.preventDefault();
            }
        }
    });

    jQuery('#leftnav h3, #changelist-filter h3').click(function() {
        if(jQuery(this).hasClass('open')) {
            jQuery(this).removeClass('open');
            jQuery(this).addClass('close');
            jQuery(this).next().slideUp('fast');
        } else if(jQuery(this).hasClass('close')) {
            jQuery(this).removeClass('close');
            jQuery(this).addClass('open');
            jQuery(this).next().slideDown('fast');
        } else if (jQuery(this).hasClass('no-child')) {
            return true;
        } return false;
    });
    $('#leftnav h3').click();

    // $('#footer').css('top',document.body.scrollHeight);
    var tmp = $('#leftnav .active');
    if(tmp.length==0){
        $('#leftnav h3')[0].click();
        $('#leftnav h3')[1].click();
    } else {
        tmp.parent().prev().click();
        tmp.parent().prev().parent().prev().click();
    }
});
