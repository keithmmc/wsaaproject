
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

 document.getElementById('delete-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const pid = document.getElementById('delete-product-id').value;

        fetch(`/product/${pid}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product deleted:', data);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error deleting product:', error));
    });
document.getElementById('product-list').addEventListener('click', function (event) {
        if (event.target.classList.contains('order-btn')) {
        // Get product details using the stored product data
        const productId = event.target.getAttribute('data-id');
        const product = products.find(product => product.pid === parseInt(pid));
        const productAmount = product.amount;
        const productName = product.Product;
        const productPrice = product.Price;
        const productInfo = product.info;

        // Get quantity input value
        const quantityInput = document.getElementById(`quantity_${pid}`);
        const quantity = quantityInput.value ? parseInt(quantityInput.value) : 1;

        // Calculate total price
        const totalPrice = productPrice * quantity;

        // Display total price
        alert(`Product: ${productName}\nQuantity: ${quantity}\nTotal Price: €${totalPrice}`);

        // Send order request to server
        sendOrderRequest(productId, quantity, totalPrice);
    }
  });

// Function to send order request
function sendOrderRequest(productId, quantity, totalPrice) {
    // Prepare order data
    const orderData = {
        productId: productId,
        quantity: quantity,
        totalPrice: totalPrice
    };

    // Send order request to the server
    fetch('/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Order Placed:', data.order);
        })
        .catch(error => console.error('Error placing order:', error));
}

  function showCreate() {
            document.getElementById('showCreateButton').style.display = "none";
            document.getElementById('productTable').style.display = "none";
            document.getElementById('createUpdateForm').style.display = "block";

            document.getElementById('createLabel').style.display = "inline";
            document.getElementById('updateLabel').style.display = "none";

            document.getElementById('doCreateButton').style.display = "block";
            document.getElementById('doUpdateButton').style.display = "none";
        }

        function showViewAll() {
            document.getElementById('showCreateButton').style.display = "block";
            document.getElementById('productTable').style.display = "block";
            document.getElementById('createUpdateForm').style.display = "none";
        }

        function showUpdate(buttonElement) {
            document.getElementById('showCreateButton').style.display = "none";
            document.getElementById('productTable').style.display = "none";
            document.getElementById('createUpdateForm').style.display = "block";

            document.getElementById('createLabel').style.display = "none";
            document.getElementById('updateLabel').style.display = "inline";

            document.getElementById('doCreateButton').style.display = "none";
            document.getElementById('doUpdateButton').style.display = "block";

            var rowElement = buttonElement.parentNode.parentNode;
            var product = getProductFromRow(rowElement);
            populateFormWithProduct(product);
        }

        function doCreate() {
        var form = document.getElementById('createUpdateForm');
        var product = {
            amount: form.querySelector('input[amount="amount"]').value,
            name: form.querySelector('input[name="name"]').value,
            price: form.querySelector('input[name="price"]').value,
            description: form.querySelector('input[name="info"]').value
        };
        createProductAjax(product);
        }
        function doUpdate() {
        // Ask for confirmation before updating
        var confirmation = confirm("Are you sure you want to update this item?");
        
        if (confirmation) {
            var product = getProductFromForm();
            var rowElement = document.getElementById(product.id);
            updateProductAjax(product);
            setProductInRow(rowElement, product);
            clearForm();
            showViewAll();
        } else {
            // Do nothing if the user cancels the update
            console.log("Update canceled.");
    }
}
 function doDelete(r) {
            var tableElement = document.getElementById('productTable');
            var rowElement = r.parentNode.parentNode;
            var index = rowElement.rowIndex;

            // Ask for confirmation before deleting
            var confirmation = confirm("Are you sure you want to delete this item?");
            
            if (confirmation) {
                deleteProductAjax(rowElement.getAttribute("id"));
                tableElement.deleteRow(index);
        } else {
            // Do nothing if the user cancels the deletion
            console.log("Deletion canceled.");
    }
}

        
        function addProductToTable(product) {
            var tableElement = document.getElementById('productTable');
            var rowElement = tableElement.insertRow(-1);
            rowElement.setAttribute('pid', product.id);
            var cell1 = rowElement.insertCell(0);
            cell1.innerHTML = product.pid;
            var cell2 = rowElement.insertCell(1);
            cell2.innerHTML = product.amount;  
            var cell2 = rowElement.insertCell(2);
            cell2.innerHTML = product.name; 
            var cell3 = rowElement.insertCell(3);
            cell3.innerHTML = product.price;  
            var cell4 = rowElement.insertCell(4);
            cell4.innerHTML = product.info;  
            var cell5 = rowElement.insertCell(5);
            cell5.innerHTML = '<button onclick="showUpdate(this)">Update</button>';
            var cell6 = rowElement.insertCell(5);
            cell6.innerHTML = '<button onclick="doDelete(this)">Delete</button>';
        }


        function clearForm() {
            var form = document.getElementById('createUpdateForm');
            form.querySelector('input[name="amount"]').value = '';
            form.querySelector('input[name="name"]').value = '';
            form.querySelector('input[name="price"]').value = '';
            form.querySelector('input[name="info"]').value = '';
        }

 function getProductFromRow(rowElement) {
            var product = {
                pid: rowElement.getAttribute('pid'),
                amount: rowElement.cells[1].firstChild.textContent,
                name: rowElement.cells[2].firstChild.textContent,
                price: rowElement.cells[3].firstChild.textContent,
                info: rowElement.cells[4].firstChild.textContent
            };
            return product;
        }
        function setProductInRow(rowElement, product) {
            rowElement.cells[0].firstChild.textContent = product.pid;
            rowElement.cells[1].firstChild.textContent = product.amount;
            rowElement.cells[2].firstChild.textContent = product.name;
            rowElement.cells[3].firstChild.textContent = product.price;
            rowElement.cells[4].firstChild.textContent = product.info;
        }
        function populateFormWithProduct(product) {
            var form = document.getElementById('createUpdateForm');
            form.querySelector('input[name="pid"]').disabled = true;
            form.querySelector('input[name="pid"]').value = product.pid;
            form.querySelector('input[name="amount"]').value = product.amount;
            form.querySelector('input[name="name"]').value = product.name;
            form.querySelector('input[name="price"]').value = product.price;
            form.querySelector('input[name="info"]').value = product.info;
        }

        function getProductFromForm() {
            var form = document.getElementById('createUpdateForm');
            var product = {
                pid: form.querySelector('input[name="pid"]').value,
                amount: form.querySelector('input[name="amount"]').value,
                name: form.querySelector('input[name="name"]').value,
                price: form.querySelector('input[name="price"]').value,
                info: form.querySelector('input[name="info"]').value
            };
            return product;
        }
        function getAllAjax() {
            $.ajax({
                "url": "http://localhost:5000/products",
                "type": "GET",
                "dataType": "json",
                "success": function (data) {
                    console.log(data);
                    for (var i = 0; i < data.length; i++) {
                        addProductToTable(data[i]);
                    }
                },
                "error": function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }
            });
        }
        // function to send a request to create a new product on the server
        function createProductAjax(product) {
            $.ajax({
                "url": "http://localhost:5000/product",
                "type": "POST",
                "contentType": "application/json",
                "data": JSON.stringify(product),
                "dataType": "json",
                "success": function (data) {
                    addProductToTable(data);
                    clearForm();
                    showViewAll();
                },
                "error": function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }
            });
        }
        // function to send a request to update an existing product on the server
        function updateProductAjax(product) {
            $.ajax({
                "url": "http://localhost:5000/product/" + product.pid,
                "type": "PUT",
                "contentType": "application/json",
                "data": JSON.stringify(product),
                "dataType": "json",
                "success": function (data) {
                    console.log(data);
                },
                "error": function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }
            });
        }
        // function to send a request to delete a product from the server
        function deleteProductAjax(pid) {
            $.ajax({
                "url": "http://localhost:5000/product/" + pid,
                "type": "DELETE",
                "success": function (data) {
                    console.log(data);
                },
                "error": function (jqXHR, textStatus, errorThrown) {
                    console.log(textStatus, errorThrown);
                }
            });
        }
        
        $(document).ready(function () {
            getAllAjax();
        });

        function showCreate() {
            document.getElementById('showCreateButton').style.display = "none";
            document.getElementById('bandTable').style.display = "none";
            document.getElementById('createUpdateForm').style.display = "block";

            document.getElementById('createLabel').style.display = "inline";
            document.getElementById('updateLabel').style.display = "none";

            document.getElementById('doCreateButton').style.display = "block";
            document.getElementById('doUpdateButton').style.display = "none";
        }

        function showViewAll() {
            document.getElementById('showCreateButton').style.display = "block";
            document.getElementById('Table').style.display = "block";
            document.getElementById('createUpdateForm').style.display = "none";
        }

        function showUpdate(buttonElement) {
            document.getElementById('showCreateButton').style.display = "none";
            document.getElementById('bandTable').style.display = "none";
            document.getElementById('createUpdateForm').style.display = "block";

            document.getElementById('createLabel').style.display = "none";
            document.getElementById('updateLabel').style.display = "inline";

            document.getElementById('doCreateButton').style.display = "none";
            document.getElementById('doUpdateButton').style.display = "block";

            var rowElement = buttonElement.parentNode.parentNode;
            var product = getProductFromRow(rowElement);
            populateFormWithProduct(band);
        }
