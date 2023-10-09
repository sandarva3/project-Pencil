function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function redirect(url) {
    setTimeout(function() {
      window.location.href = url;
    }, 10000);
  }
  

const originalText = "Hang on....";
const container = document.getElementById("wait");
let index = 0;
let direction = 'forward';

function animateText() {
    if (direction === 'forward') {
        if (index < originalText.length) {
            container.innerHTML += originalText[index];
            index++;
        } else {
            direction = 'backward';
        }
    } else {
        if (index > originalText.length - 3) {
            container.innerHTML = container.innerHTML.slice(0, -1);
            index--;
        } else {
            direction = 'forward';
        }
    }
    setTimeout(animateText, 170);
}



document.addEventListener("DOMContentLoaded", (event) => {
    const form2 = document.querySelector("form[method='get']");
    form2.addEventListener("submit", function (e) {
        e.preventDefault();
        const link = document.getElementById("hidden_link").value;
        const resolution = document.getElementById("resolution").value;
        sendData(link, resolution);
    });
});


function sendData(link, resolution) {
    // Create URL parameters
    const params = new URLSearchParams({ link: link, resolution: resolution }).toString();

    // Append parameters to the URL
    const url = "" + "?" + params;
    animateText();
    // Fetch data
    fetch(url, {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                document.getElementById("msg2").textContent = data.msg2;
                document.getElementById("wait").style.display = "none";
                console.log("SUCCESSFULLY DOWNLOADED")
                const downloadLink = document.getElementById("download-link");
                downloadLink.style.display = "block";
                downloadLink.href = `download?filename=${encodeURIComponent(data.filename)}`;
                console.log("FILE NAME IS :", data.filename)
                redirect("");

            } else {
                document.getElementById("msg1").textContent = data.msg1;
                document.getElementById("wait").style.display = "none";
                console.log("FAILED TO DOWNLOAD")
            }
        })
        .catch(error => console.error("ERROR: ", error));
}
