$(document).ready(() => {
    $("form").on('submit', (e) => {
        e.preventDefault();

        var formData = new FormData($('form')[0]);
        var token = '{{csrf_token}}';
        $.ajax({
            type: 'POST',
            url: '/xml',
            data: formData,
            headers: { "X-CSRFToken": token },
            processData: false,
            contentType: false,
            success: () => {
                alert("File Uploaded");
            }
        });
    });
});