<?php
class ShopDAO {
    private $db_host = 'localhost';
    private $db_name = 'wsaa1';
    private $db_user = 'root';
    private $db_pass = 'pass';

    private function getConnection() {
        $conn = new mysqli($this->db_host, $this->db_user, $this->db_pass, $this->db_name);
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        return $conn;
    }

    public function get_cursor() {
        return $this->getConnection();
    }

    public function close_all($mycursor) {
        $mycursor->close();
    }

    // Create a new product
    public function create_product($product, $model, $price) {
        $conn = $this->getConnection();
        $stmt = $conn->prepare("INSERT INTO productdata (Product, Model, Price) VALUES (?, ?, ?)");
        $stmt->bind_param("ssd", $product, $model, $price);
        $stmt->execute();
        $product_id = $stmt->insert_id;
        $stmt->close();
        $conn->close();
        return ['id' => $product_id, 'Product' => $product, 'Model' => $model, 'Price' => $price];
    }

    // Get all products
    public function get_all_products() {
        $conn = $this->getConnection();
        $result = $conn->query("SELECT * FROM productdata");
        $products = [];
        while ($row = $result->fetch_assoc()) {
            $products[] = $row;
        }
        $conn->close();
        return $products;
    }

    // Get product by ID
    public function get_product_by_id($id) {
        $conn = $this->getConnection();
        $stmt = $conn->prepare("SELECT * FROM productdata WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();
        $product = $result->fetch_assoc();
        $stmt->close();
        $conn->close();
        return $product;
    }

    // Update a product
    public function update_product($id, $product, $model, $price) {
        $conn = $this->getConnection();
        $stmt = $conn->prepare("UPDATE productdata SET Product = ?, Model = ?, Price = ? WHERE id = ?");
        $stmt->bind_param("ssdi", $product, $model, $price, $id);
        $stmt->execute();
        $stmt->close();
        $conn->close();
        return ['id' => $id, 'Product' => $product, 'Model' => $model, 'Price' => $price];
    }

    // Delete a product
    public function delete_product($id) {
        $conn = $this->getConnection();
        $stmt = $conn->prepare("DELETE FROM productdata WHERE id = ?");
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $stmt->close();
        $conn->close();
        return true;
    }


    public function create_order($product_id, $quantity, $total_price) {
        $conn = $this->getConnection();
        $stmt = $conn->prepare("INSERT INTO orderdata (product_id, quantity, total_price) VALUES (?, ?, ?)");
        $stmt->bind_param("iid", $product_id, $quantity, $total_price);
        $stmt->execute();
        $order_id = $stmt->insert_id;
        $stmt->close();
        $conn->close();
        return ['order_id' => $order_id, 'product_id' => $product_id, 'quantity' => $quantity, 'total_price' => $total_price];
    }
}

$shop_dao = new ShopDAO();
?>
