function myFunction() {
    // Declare variables
    let input, filter, ul, li, a, i, txtValue;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    let device_list = document.getElementById("eplan-devices");
    // li = ul.getElementsByTagName('li');
    let devices = document.querySelectorAll('#eplan-device') 


    // console.log(devices);
    // // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < devices.length; i++) {
        a = devices[i];
        
        let b = a.getElementsByTagName("h4")[0];
        console.log(b);
        txtValue = b.textContent || b.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a.style.display = "";
        } else {
            a.style.display = "none";
        }
    }
}