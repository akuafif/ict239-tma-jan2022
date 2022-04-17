// template/viewpackage.html

// datepicker objeect
instance = new dtsel.DTS('input[name="checkindate"]',  {
	dateFormat: "dd-mm-yyyy",}
);
	
document.getElementById('checkindate').value = moment().format('DD-MM-yyyy');
$('button').click(function(){
	document.getElementById("output").innerHTML = '';
	document.getElementById("error").innerHTML = '';

	var checkindate = document.getElementById('checkindate').value;
	var datearray = checkindate.split("-");
	var today = new Date();
	today.setDate(today.getDate()-1); // comparing yesterday date
	
	// checkindate.match(/^(0?[1-9]|[12][0-9]|3[01])[\-](0?[1-9]|1[012])[\/\-]\d{4}$/)
	// checks for date format with regex dd-mm-yyyy
	// if (moment(checkindate, 'DD-MM-YYYY', true).isValid()  && (checkdate > today)){
	if (moment(checkindate, 'DD-MM-YYYY', true).isValid()){
		$.ajax({
			type: 'POST',
			url: "/addbooking",
			data: JSON.stringify({
			"hotel_name": document.getElementById('hotel_name').innerHTML,
			"checkindate": checkindate
		}),
			error: function(e) {
				document.getElementById("error").innerHTML = e;
			},
			dataType: "json",
			contentType: "application/json",
			success: function(response){
				if (response['status'] === 'OK'){
					document.getElementById("output").innerHTML = response['message'];
				} else {
					document.getElementById("error").innerHTML = response['message'];
				}
			}
		});
	} else {
		document.getElementById("error").innerHTML = 'ERROR: Cannot book past date or invalid format (dd-mm-yyyy)';
	}
});