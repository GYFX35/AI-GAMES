document.addEventListener('DOMContentLoaded', () => {
  const purchaseBtn = document.getElementById('purchaseBtn');

  if (purchaseBtn) {
    purchaseBtn.addEventListener('click', () => {
      console.log('Purchase button clicked');
      // Initialize the SDK first
      FBInstant.initializeAsync()
        .then(() => {
          console.log('FBInstant SDK initialized');
          // After initialization, get the catalog
          return FBInstant.payments.getCatalogAsync();
        })
        .then((catalog) => {
          console.log('Product catalog loaded:', catalog);
          // For simplicity, we'll assume the first product is the one we want to sell
          const product = catalog[0];
          console.log('Attempting to purchase product:', product.title);

          // Call the purchase method
          return FBInstant.payments.purchaseAsync({
            productID: product.productID,
            developerPayload: 'payload_for_premium_tools', // Optional payload
          });
        })
        .then((purchase) => {
          console.log('Purchase successful:', purchase);
          // Send the purchase token to the backend for verification
          return fetch('/api/verify_purchase', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              signedRequest: purchase.signedRequest,
            }),
          });
        })
        .then(response => response.json())
        .then(data => {
          console.log('Verification response from backend:', data);
          if (data.status === 'completed') {
            alert('Purchase successful and verified! Premium tools unlocked.');
            // Here you would unlock the premium features
          } else {
            alert('Purchase verification failed. Please contact support.');
          }
        })
        .catch((error) => {
          console.error('An error occurred during the purchase flow:', error);
          alert('An error occurred: ' + error.message);
        });
    });
  }
});
