// AJAX for posting
function catogorise_post(form) {
    $form = form
    $.ajax({
        url : $form.attr('action'), // the endpoint
        type : "POST", // http method
        data : { 
            category : $form.children().find("#id_category :selected").val(),
            second_category : $form.children().find("#id_second_category :selected").val(),
            third_category : $form.children().find("#id_third_category :selected").val(),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        }, // data sent with the post request
        // handle a successful response
        success : function(data) {
            $($form.attr('id')).val(''); // remove the value from the input
            console.log(data); // log the returned data to the console
            console.log("success"); // another sanity check
            $form.siblings('.category-field').text($form.children().find("#id_category :selected").text());
            $.notify({
                icon: data['icon'],
                message: "<b>" + data['message'] + "</b>"
            },{
                type: data['type'],
                timer: 500
            });
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    console.log(form);
};


// AJAX for posting
function export_post(form) {
    $form = form
    $.ajax({
        url : $form.attr('action'), // the endpoint
        type : "POST", // http method
        // contentType: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        data : { 
            file_format : $form.children().find("select :selected").val(),
            csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        // handle a successful response
        success : function(data) {
            console.log(data); // log the returned data to the console
            console.log("success"); // another sanity check
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
    console.log(form);
};



function ajax_download(form) {
    console.log('start');
    var $iframe,
        iframe_doc,
        iframe_html,
        csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if (($iframe = $('#download_iframe')).length === 0) {
        $iframe = $("<iframe id='download_iframe'" +
                    " style='display: none' src='about:blank'></iframe>"
                   ).appendTo("body");
    }

    iframe_doc = $iframe[0].contentWindow || $iframe[0].contentDocument;
    if (iframe_doc.document) {
        iframe_doc = iframe_doc.document;
    }

    iframe_html = "<html><head></head><body><form method='POST' action='/admin/location/post/export/?'>" 
    iframe_html += "<input type='hidden' name='csrfmiddlewaretoken' value='" + csrfmiddlewaretoken + "'>"
    iframe_html += "<input type='hidden' name='file_format' value='2'>";
    iframe_html +="</form></body></html>";
    
    console.log('doing');
    iframe_doc.open();
    iframe_doc.write(iframe_html);
    $(iframe_doc).find('form').submit();
    console.log('done');
}