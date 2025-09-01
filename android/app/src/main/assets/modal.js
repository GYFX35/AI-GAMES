// Wait for the DOM to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {

    // Get the modal element
    const modal = document.getElementById("sponsorshipModal");

    // Get the button that opens the modal
    const btn = document.getElementById("sponsorBtn");

    // Get the <span> element that closes the modal
    const span = document.getElementsByClassName("close-btn")[0];

    // When the user clicks the button, open the modal
    if (btn) {
        btn.onclick = function() {
            if (modal) {
                modal.style.display = "block";
            }
        }
    }

    // When the user clicks on <span> (x), close the modal
    if (span) {
        span.onclick = function() {
            if (modal) {
                modal.style.display = "none";
            }
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});
