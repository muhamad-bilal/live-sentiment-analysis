$('#searchForm').submit(function(event) {
    event.preventDefault(); 
  
    const searchText = $('#celebrity').val();
  
    $.ajax({
      url: '/analyze', 
      type: 'POST',
      data: { name: searchText }, 
      success: function(response) {
        if (response.status === 'success') {
          window.location.href = '/analyze';
        } else {
          $('#result').text("An error occurred.");
        }
      },
      error: function() { 
        $('#result').text("An error occurred.");
      } 
    });
  });
  