var quali_id = 1
function doctor_qualifications()
{
    var objTo = document.getElementById('doc_quali');
    var divtest;
    quali_id++;
    divtest = document.createElement("div");
    divtest.setAttribute("class", 'form-group removeclass'+quali_id);
    divtest.setAttribute("style", 'margin-top:20px; margin-left:10px width:100%')
    divtest.innerHTML = '<div class="input-group" style="margin:0px 20px 10px 0px"><span class="input-group-addon"><i class="fa fa-graduation-cap"></i></span><input type="text" class="form-control" id="doctor_degree" name="doctor_degree" placeholder="Degree Name" pattern="[A-Za-z .-]{2,50}" required></div><div class="input-group" style="margin:0px 20px 10px 0px" ><span class="input-group-addon"><i class="fa fa-graduation-cap"></i></span><input type="text" class="form-control" id="doctor_institute" name="doctor_institute" placeholder="Institute Name" pattern="[A-Za-z ,.-]{3,120}" required></div><div class="input-group" style="margin:0px 20px 10px 0px" ><span class="input-group-addon"><i class="fa fa-graduation-cap"></i></span><input type="text" class="form-control" id="doctor_qualification_year" name="doctor_qualification_year" placeholder="Year of completion" pattern="[0-9]{4}" required></div><button class="btn btn-danger" type="button" onclick="remove_doc_quali('+ quali_id +');"> <span aria-hidden="true">-</span></button>';
    objTo.appendChild(divtest);

}

function remove_doc_quali(rid)
{
    var rdiv = parseInt(rid);
    $('div').remove('.'+'removeclass'+rdiv);
}