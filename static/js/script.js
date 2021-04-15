// materialize sidebar 

$(document).ready(function () {
    $('.sidenav').sidenav({
        edge: "right"
    });
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('.modal').modal();
    M.updateTextFields();
});