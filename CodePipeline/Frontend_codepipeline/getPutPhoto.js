function searchPhoto(event) {
  event.preventDefault();

  $("#imageDisplay").empty();
  var apigClient = apigClientFactory.newClient({});
  var labels = $("#label").val();
  console.log(labels)
  var data = {'q': labels};

  apigClient.searchGet(data, {}, {})
    .then((response) => {
      console.log('response', response);
      console.log('search success')
      var imagedata = response["data"];
      for (var i = 0; i < imagedata.length; i++){
        var photoURL = imagedata[i]
        if(photoURL != null){
          var newElement = 
            "<img class='img-fluid w-100' src='" + photoURL + "' alt='Failed to open image: " + photoURL + "'>" 
          $("#imageDisplay").prepend(newElement);
        }
      }
  });
}

function uploadPhoto(event) {
  event.preventDefault();

  var image = document.getElementById('image').files[0];
  var metaData = document.getElementById("customLabel").value
  var imageType = image.type;
  var fileName = image.name;
  
  $.ajax({
        url: "https://v18aocqene.execute-api.us-east-1.amazonaws.com/dev/cu6998hw2b2/"+ fileName,
        type: 'PUT',
        data: image,
        dataType: 'html',
        headers: {'Content-Type': 'multipart/form-data',
        'x-amz-meta-customLabels':metaData,
        'x-api-key':'OkEWRIHt88UDRcuCqIQT3tNA0sccAKw4tRsUZOUc'},
        processData: false,
        contentType: imageType,
        success: function (response) {
          alert("Upload Successful");
          console.log(response);
        },
        error: function(err) {
          return alert("There was an error uploading your photo: ", err.message);
        }
    });
}