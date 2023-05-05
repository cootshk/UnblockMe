document.getElementById("go").addEventListener("click", function() {
    let website = document.getElementById("url").value;
    open(website, "_self");
});