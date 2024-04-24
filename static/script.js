$(document).ready(function() {
    $('#searchForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission behavior

        const searchText = $('#celebrity').val(); // Get the input value


        $('#line-loader').show(); // Show the loader

        $.ajax({
            url: '/analyze',  // Your Flask route's endpoint
            type: 'POST',
            data: { name: searchText }, // Send the search text as data
            success: function(response) {
                 
                if (response.status === 'success') {
                    window.location.href = '/analyze';
                } else {
                    $('#result').text("An error occurred."); 
                }
            },
            error: function() { 
                $('#result').text("An error occurred.");
            },
            complete: function() { // Or use 'always' if needed
                setTimeout(function() {
                $('#line-loader').hide();  // Hide the loader
            }, 2000);
        },});
    });
});
