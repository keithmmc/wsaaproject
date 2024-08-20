<?php 

session_start();
require 'shop_dao.py';

header('Content-Type: application/json');

$request_method = $_SERVER['REQUEST_METHOD'];
$path_info = $_SERVER['PATH_INFO'] ?? '/';

//setting up routing 

switch ($request_method) {
    case "GET":
        if ($path_info == '/shirts') {
            getAll();

        } elseif (preg_match('/\/shirts\/(\d+)/', $path_info, $matches)) {
            $id = $matches[1];
            findById($id);
        }
        break;
    case 'POST';
}