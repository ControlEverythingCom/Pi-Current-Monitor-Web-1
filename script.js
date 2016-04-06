window.onload=function(){
    fetchValues(valuesCallback);
}
function fetchValues(callback){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            callback(JSON.parse(xhttp.responseText));
        }
    };
    xhttp.open("GET", "/CurrentMonitor.py", false);
    xhttp.send();
    return;
}
function valuesCallback(results){
    var output = "<table><thead><th>Channel</th><th>Reading</th></thead><tbody>";
    for(var i=0;i<results.length;i++){
        output+="<tr><td>Channel "+(i+1)+":</td><td>"+results[i]+"</td></tr>";
    }
    output+='</tbody></table>';
    document.getElementById('results').innerHTML = output;
    document.getElementById('header').innerText = 'Current Readings';
    window.setTimeout(function(){fetchValues(valuesCallback);}, 2000);
}

