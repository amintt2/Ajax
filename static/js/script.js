function checkUsername() {
    if (document.getElementById("codeClient").value.length > 0) {
        const xhttp = new XMLHttpRequest();
        
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                const responseData = JSON.parse(xhttp.responseText);
                if (responseData.length > 0) {
                    const clientData = responseData[0];
                    console.log(clientData);
                    alert("Client trouvé : " + clientData.nom + " " + clientData.prenom);
                } else {
                    alert("Client "+document.getElementById("codeClient").value+" non trouvé.");
                }
            }
        };

        xhttp.open("GET", "/api/client?codeClient="+document.getElementById("codeClient").value, true);
        xhttp.send();
    }
}
