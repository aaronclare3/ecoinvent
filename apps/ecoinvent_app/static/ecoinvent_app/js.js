$(document).ready( () => {
    $('#form1').on('submit', function(event) {
        document.getElementById("d-type").classList.remove("d-none")
        var seeData = true;
        event.preventDefault();
        var formData = new FormData($('form')[0]);
        $.ajax({
            xhr : () => {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        console.log('Bytes Loaded: ' + e.loaded);
                        console.log('Total Size: ' + e.total);
                        console.log('Percentage Uploaded: ' + (e.loaded / e.total))
                        var percent = Math.round((e.loaded / e.total) * 100);
                        $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                    }
                });
                return xhr;
            },
            type : 'POST',
            url : '/xml',
            data : formData,
            processData : false,
            contentType : false,
            success : () => {
                console.log('File uploaded!');
                setTimeout(() => { window.location.reload();}, 200)
            }
        });
    });
});
