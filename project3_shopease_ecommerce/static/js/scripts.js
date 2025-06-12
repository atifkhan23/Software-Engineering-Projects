function updateCartItem(productId) {
    const quantityInput = document.querySelector(`input[name="quantity"][data-product-id="${productId}"]`);
    if (quantityInput) {
        const quantity = quantityInput.closest('form');
        quantity.submit();
    }
}