window.onload = () => {
  
  const image_form = document.getElementById("image");
  const btn_predict = document.getElementById("predict")
  const btn_cancel = document.getElementById("cancel")
  const btn_reset = document.getElementById("reset")
  const box = document.getElementById("box-container")
  const displayed_image = document.getElementById("image_show")
  const upload_content = document.getElementsByClassName("upload-content")

  // Click box form
  box.addEventListener("click", (e) => {
    image_form.click()
  }, false)
  
  // Display image file
  if (image_form) {
    image_form.addEventListener("change", (e) => {
      const file = image_form.files[0]
      const allowed_type = ['image/jpeg', 'image/jpg', 'image/png']
      if (!allowed_type.includes(file.type)) {
        alert("Image must be jpg, jpeg or png !")
        return;
      }
      for (let index = 0; index < upload_content.length; index++) {
        upload_content[index].style.display = 'none'    
      }
      displayed_image.src = URL.createObjectURL(file)
      displayed_image.style.display = 'block'
    })
  }
  
  // Handle Cancel
 if (btn_cancel) {
  btn_cancel.addEventListener("click", (e)=> {
    displayed_image.src = ""
    displayed_image.style.display = 'none'
    for (let index = 0; index < upload_content.length; index++) {
      upload_content[index].style.display = 'block'    
    }
  })
 }

  // Handle Predict
  if (btn_predict) {
    btn_predict.addEventListener("click", (e) => {
      if (image_form.files.length == 0) {
        alert("Image is empty!")
        return
      }
      document.getElementById("form").submit()
    })
  }

  // Handle Back
  // btn_reset.addEventListener("click", (e)=> {
  //   const footer = document.getElementsByClassName("box-footer")[0]
  //   const result = document.getElementsByClassName("box-result")[0]

  //   footer.style.display = 'flex'
  //   result.style.display = 'none'
  // })
};
