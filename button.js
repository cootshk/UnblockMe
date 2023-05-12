window.onload = function () {
    document.getElementById("go").addEventListener(onclick, function() {
        let website = document.getElementById("url").value;
        window.open("/"+website+"/", "_self");
        console.log("clicked " + website);
});};
/*("click",
function() {
    let website = document.getElementById("url").value;
    open(website, "_self");
});
*/