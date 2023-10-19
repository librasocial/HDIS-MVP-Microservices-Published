//add Family History
var history_no = 1
function family_history() {
       var objTo = document.getElementById('family_history');
       var divtest;
       history_no++;
       divtest = document.createElement("div");
       divtest.setAttribute("class", 'col-sm form-group removeclass'+history_no);
       divtest.setAttribute("style", 'margin-top:10px');
       var new_id = "family_history" + history_no;
       divtest.innerHTML = ''
       objTo.appendChild(divtest);
   }
     function remove_pres_fields(rid) {
       var rdiv = parseInt(rid);
      $('div').remove('.'+'removeclass'+rdiv);
      }