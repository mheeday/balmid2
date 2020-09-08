document.addEventListener("DOMContentLoaded", (event) => {
    // Add an event listener for when the user clicks the submit button to pay
    document.getElementById("submit").addEventListener("click", (e) => {
        e.preventDefault();
        const PBFKey = "FLWPUBK_TEST-515b15ec94b52fa76b9247665ed97def-X"; // paste in the public key from your dashboard here
        const txRef = document.getElementById('txRef').value; //Generate a random id for the transaction reference
        const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const amount = document.getElementById('amount').value;
        
       

        // getpaidSetup is Rave's inline script function. it holds the payment data to pass to Rave.
    getpaidSetup({
        PBFPubKey: PBFKey,
        customer_email: email,
        amount: amount,
        customer_phone: phone,
        currency: "NGN",  // Select the currency. leaving it empty defaults to NGN
        txref: txRef, // Pass your UNIQUE TRANSACTION REFERENCE HERE.
    
        onclose: function() {},
        callback: function(response) {
            flw_ref = response.tx.flwRef;// collect flwRef returned and pass to a server page to complete status check.
            console.log("This is the response returned after a charge", response);
            if(response.tx.chargeResponse =='00' || response.tx.chargeResponse == '0') {
            // redirect to a success page
            } else {
            // redirect to a failure page.
            }
        }
      });
    });
});