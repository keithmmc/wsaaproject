document.addEventListener('DOMContentLoaded', function () {
    // Global Variable to store products
    let products = [];

    // Fetch and display products on page load
    function fetchProducts() {
        fetch('/product')
            .then(response => response.json())
            .then(data => {
                products = data.product;  // Store the fetched products in the global variable
                const productList = document.getElementById('product-list');
                productList.innerHTML = '<h2>Products</h2>';
                data.shoes.forEach(product => {
                    productList.innerHTML += `
                    <div class="product-item">
                        <p>ID: ${product.pid}, amount: ${product.amount}, name: ${product.name}, Price: ${product.Price}, Info: ${product.info}</p>
                        <button class="order-btn" data-id="${product.pid}">Order</button>
                        <input type="number" class="quantity-input" id="quantity_${product.pid}" placeholder="Quantity" min="1">
                    </div>
                    `;
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    // Fetch and display products on page load
    fetchProducts();
    document.getElementById('add-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productAmount = document.getElementById('product-amount').value;
        const productName = document.getElementById('product-name').value;
        const productPrice = document.getElementById('product-price').value;
        const productInfo = document.getElementById('product-info').value;
        fetch('/product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'Product': productAmount,
                'Product': productName,
                'Price': productPrice,
                'info': productInfo,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product added:', data.product);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error adding product:', error));
    });
    document.getElementById('update-product-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const productPId = document.getElementById('update-product-Pid').value;
        const productAmount = document.getElementById('update-product-amount')
        const productName = document.getElementById('update-product-name').value;
        const productPrice = document.getElementById('update-product-price').value;
        const productInfo = document.getElementById('update-product-info').value;
        fetch(`/product/${pid}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'Amount': productAmount,
                'Name': productName,
                'Price': productPrice,
                'info': productInfo,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product updated:', data.product);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error updating product:', error));
    });
    

})
