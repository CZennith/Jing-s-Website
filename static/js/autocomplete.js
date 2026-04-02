
/* done following the w3school guide on autocomplete forms */
function autocomplete_search(input, arr) {


    input.addEventListener("input", function(e) {
        var a, b, i, val = this.value;

        closeAllLists();

        a = document.createElement("DIV");
        a.setAttribute("id", this.id + " autocomplete-list");
        a.setAttribute("class", "autocomplete-items");

        this.parentNode.appendChild(a);

        var counter = 0;
        const limit = 8;

        for (i = 0; i < arr.length; i++) {

            if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
                if (counter >= limit) break;

                b = document.createElement("DIV");
                b.setAttribute("data-value",arr[i]);
                b.innerHTML = `<strong>${arr[i].substr(0, val.length)}</strong>${arr[i].substr(val.length)}`

                b.addEventListener("click", function(e) {
                    input.value = this.dataset.value;

                    closeAllLists();
                });
                a.appendChild(b)

                counter++;
            }
        }
    });
    

    function closeAllLists (elemnt) {
            /*close all autocomplete lists in the document,
        except the one passed as an argument:*/

        var x = document.getElementsByClassName("autocomplete-items");

        for (let i = 0; i < x.length; i++) {
            if (elemnt != x[i] && elemnt != input) {
                x[i].parentNode.removeChild(x[i]);
            }
        }
    }
    document.addEventListener("click", function (e) {
    closeAllLists(e.target);
    });
} 

