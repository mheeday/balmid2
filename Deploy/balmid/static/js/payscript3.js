
    const PBFKey = "<YOUR PUBLIC KEY>"; // paste in the public key from your dashboard here
    const txRef = document.getElementById('txRef').value; //Generate a random id for the transaction reference
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const amount = document.getElementById('amount').value;
    const name = document.getElementById('name').value;

        function makePayment() {
          FlutterwaveCheckout({
            public_key: "FLWPUBK_TEST-515b15ec94b52fa76b9247665ed97def-X",
            tx_ref: txRef,
            amount: amount,
            currency: "NGN",
            payment_options: "card, mobilemoneyghana, ussd",
            redirect_url: // specified redirect URL
              "https://callbacks.piedpiper.com/flutterwave.aspx?ismobile=34",
            
            customer: {
              email: email,
              phone_number: phone,
              name: name,
            },
            callback: function (data) {
              console.log(data);
            },
            onclose: function() {
              // close modal
            },
          });
        }
